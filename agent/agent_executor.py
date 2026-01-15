# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import logging
from typing import Any

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import DataPart, Part, Task, TaskState, TextPart, UnsupportedOperationError
from a2a.utils import new_agent_parts_message, new_agent_text_message, new_task
from a2a.utils.errors import ServerError
from a2ui.a2ui_extension import create_a2ui_part, try_activate_a2ui_extension

from ocr import extract_from_base64
from storage import add_claim, search_claims
from ui_builder import build_confirmation, build_expense_form, build_search_results

logger = logging.getLogger(__name__)


class ExpenseAgentExecutor(AgentExecutor):
    """Expense reporting AgentExecutor."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        action_name = None
        action_context: dict[str, Any] = {}
        text_input = ""

        use_ui = try_activate_a2ui_extension(context)
        logger.info(f"--- Client requested extensions: {context.requested_extensions} ---")
        logger.info(f"--- A2UI extension active: {use_ui} ---")

        if context.message and context.message.parts:
            for part in context.message.parts:
                if isinstance(part.root, DataPart):
                    data = part.root.data
                    if isinstance(data, dict) and "userAction" in data:
                        event = data["userAction"]
                        action_name = (
                            event.get("actionName")
                            or event.get("name")
                            or event.get("action")
                        )
                        action_context = event.get("context", {}) or {}
                    elif isinstance(data, dict):
                        action_name = data.get("actionName") or data.get("action")
                        action_context = data.get("context", {}) or {}
                elif isinstance(part.root, TextPart):
                    text_input = part.root.text

        task = context.current_task
        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)

        updater = TaskUpdater(event_queue, task.id, task.context_id)

        if not use_ui:
            await updater.update_status(
                TaskState.completed,
                new_agent_text_message(
                    "A2UI対応クライアントから接続してください。", task.context_id, task.id
                ),
                final=True,
            )
            return

        messages: list[dict[str, Any]] | None = None
        final_state = TaskState.input_required

        if action_name == "upload_receipt":
            file_base64 = action_context.get("fileBase64")
            file_name = action_context.get("fileName", "receipt")
            file_type = action_context.get("fileType", "image/png")
            if not file_base64:
                await updater.update_status(
                    TaskState.completed,
                    new_agent_text_message(
                        "アップロードデータが見つかりませんでした。", task.context_id, task.id
                    ),
                    final=True,
                )
                return
            ocr_result = extract_from_base64(file_base64, file_type, file_name)
            form_data = {
                "receiptName": ocr_result.receipt_name,
                "merchant": ocr_result.merchant,
                "date": ocr_result.date,
                "amount": ocr_result.amount,
                "currency": ocr_result.currency,
                "category": "",
                "paymentMethod": "",
                "memo": "",
            }
            messages = build_expense_form(form_data)
        elif action_name == "submit_expense":
            payload = {
                "receiptName": action_context.get("receiptName", ""),
                "merchant": action_context.get("merchant", ""),
                "date": action_context.get("date", ""),
                "amount": action_context.get("amount", ""),
                "currency": action_context.get("currency", ""),
                "category": action_context.get("category", ""),
                "paymentMethod": action_context.get("paymentMethod", ""),
                "memo": action_context.get("memo", ""),
            }
            record = add_claim(payload)
            messages = build_confirmation(record)
            final_state = TaskState.completed
        elif action_name == "search_expense":
            query = action_context.get("query", "")
            results = search_claims(query)
            messages = build_search_results(results)
        else:
            if text_input:
                await updater.update_status(
                    TaskState.completed,
                    new_agent_text_message(
                        "アップロードまたは検索を行ってください。", task.context_id, task.id
                    ),
                    final=True,
                )
                return

        if not messages:
            await updater.update_status(
                TaskState.completed,
                new_agent_text_message(
                    "処理対象が見つかりませんでした。", task.context_id, task.id
                ),
                final=True,
            )
            return

        parts = [create_a2ui_part(message) for message in messages]
        await updater.update_status(
            final_state,
            new_agent_parts_message(parts, task.context_id, task.id),
            final=(final_state == TaskState.completed),
        )

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
