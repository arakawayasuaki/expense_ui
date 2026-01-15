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

import base64
import logging

import click
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill
from a2ui.a2ui_extension import get_a2ui_agent_extension
from dotenv import load_dotenv
from PIL import UnidentifiedImageError
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from agent_executor import ExpenseAgentExecutor
from ocr import extract_from_base64

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@click.command()
@click.option("--host", default="localhost")
@click.option("--port", default=10002)
def main(host, port):
    capabilities = AgentCapabilities(
        streaming=False,
        extensions=[get_a2ui_agent_extension()],
    )
    skill = AgentSkill(
        id="expense_reporter",
        name="Expense Report",
        description="OCR receipts and submit expense reports.",
        tags=["expense", "receipt", "ocr"],
        examples=["Upload a receipt image and submit an expense report."],
    )

    base_url = f"http://{host}:{port}"
    agent_card = AgentCard(
        name="Expense Reporter",
        description="A2UI agent for expense reports with OCR.",
        url=base_url,
        version="1.0.0",
        default_input_modes=["text", "text/plain"],
        default_output_modes=["text", "text/plain"],
        capabilities=capabilities,
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ExpenseAgentExecutor(base_url=base_url),
        task_store=InMemoryTaskStore(),
    )
    server = A2AStarletteApplication(
        agent_card=agent_card, http_handler=request_handler
    )

    import uvicorn

    app = server.build()

    async def ocr_endpoint(request: Request) -> JSONResponse:
        try:
            payload = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON payload"}, status_code=400)

        file_base64 = payload.get("fileBase64")
        file_name = payload.get("fileName", "receipt")
        file_type = payload.get("fileType", "image/png")
        if not file_base64:
            return JSONResponse({"error": "fileBase64 is required"}, status_code=400)

        try:
            result = extract_from_base64(file_base64, file_type, file_name)
        except (base64.binascii.Error, ValueError, UnidentifiedImageError) as exc:
            return JSONResponse(
                {"error": f"Invalid receipt payload: {exc}"},
                status_code=400,
            )
        except Exception as exc:
            return JSONResponse(
                {"error": f"OCR failed: {exc}"},
                status_code=500,
            )
        return JSONResponse(
            {
                "text": result.text,
                "merchant": result.merchant,
                "date": result.date,
                "amount": result.amount,
                "currency": result.currency,
            }
        )

    app.add_route("/ocr", ocr_endpoint, methods=["POST"])
    app.add_middleware(
        CORSMiddleware,
        allow_origin_regex=r"https?://.*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()
