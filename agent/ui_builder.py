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

from typing import Any

import json
import logging
import os

from openai import OpenAI

logger = logging.getLogger(__name__)

_REVIEW_SURFACE_ID = "expense-review"
_DEFAULT_MODEL = "gpt-4o-mini"


def _review_data_contents(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"key": "receiptName", "valueString": data.get("receiptName", "")},
        {"key": "merchant", "valueString": data.get("merchant", "")},
        {"key": "date", "valueString": data.get("date", "")},
        {"key": "amount", "valueString": data.get("amount", "")},
        {"key": "currency", "valueString": data.get("currency", "JPY")},
        {"key": "category", "valueString": data.get("category", "")},
        {"key": "paymentMethod", "valueString": data.get("paymentMethod", "")},
        {"key": "memo", "valueString": data.get("memo", "")},
    ]


def _build_review_fallback(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "beginRendering": {
                "surfaceId": _REVIEW_SURFACE_ID,
                "root": "review-root",
                "styles": {"primaryColor": "#2F5AFF", "font": "Roboto"},
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": _REVIEW_SURFACE_ID,
                "components": [
                    {
                        "id": "review-root",
                        "component": {
                            "Column": {
                                "children": {
                                    "explicitList": [
                                        "review-title",
                                        "review-receipt-label",
                                        "review-receipt",
                                        "review-merchant-label",
                                        "review-merchant",
                                        "review-date-label",
                                        "review-date",
                                        "review-amount-label",
                                        "review-amount",
                                        "review-currency-label",
                                        "review-currency",
                                        "review-category-label",
                                        "review-category",
                                        "review-payment-label",
                                        "review-payment",
                                        "review-memo-label",
                                        "review-memo",
                                        "submit-button",
                                    ]
                                }
                            }
                        },
                    },
                    {
                        "id": "review-title",
                        "component": {
                            "Text": {
                                "usageHint": "h2",
                                "text": {"literalString": "申請内容の確認"},
                            }
                        },
                    },
                    {
                        "id": "review-receipt-label",
                        "component": {"Text": {"text": {"literalString": "領収書"}}},
                    },
                    {"id": "review-receipt", "component": {"Text": {"text": {"path": "receiptName"}}}},
                    {
                        "id": "review-merchant-label",
                        "component": {"Text": {"text": {"literalString": "支払先"}}},
                    },
                    {"id": "review-merchant", "component": {"Text": {"text": {"path": "merchant"}}}},
                    {
                        "id": "review-date-label",
                        "component": {"Text": {"text": {"literalString": "日付"}}},
                    },
                    {"id": "review-date", "component": {"Text": {"text": {"path": "date"}}}},
                    {
                        "id": "review-amount-label",
                        "component": {"Text": {"text": {"literalString": "金額"}}},
                    },
                    {"id": "review-amount", "component": {"Text": {"text": {"path": "amount"}}}},
                    {
                        "id": "review-currency-label",
                        "component": {"Text": {"text": {"literalString": "通貨"}}},
                    },
                    {"id": "review-currency", "component": {"Text": {"text": {"path": "currency"}}}},
                    {
                        "id": "review-category-label",
                        "component": {"Text": {"text": {"literalString": "カテゴリ"}}},
                    },
                    {"id": "review-category", "component": {"Text": {"text": {"path": "category"}}}},
                    {
                        "id": "review-payment-label",
                        "component": {"Text": {"text": {"literalString": "支払方法"}}},
                    },
                    {"id": "review-payment", "component": {"Text": {"text": {"path": "paymentMethod"}}}},
                    {
                        "id": "review-memo-label",
                        "component": {"Text": {"text": {"literalString": "備考"}}},
                    },
                    {"id": "review-memo", "component": {"Text": {"text": {"path": "memo"}}}},
                    {
                        "id": "submit-button",
                        "component": {
                            "Button": {
                                "child": "submit-button-text",
                                "primary": True,
                                "action": {
                                    "name": "submit_expense",
                                    "context": [
                                        {"key": "receiptName", "value": {"path": "receiptName"}},
                                        {"key": "merchant", "value": {"path": "merchant"}},
                                        {"key": "date", "value": {"path": "date"}},
                                        {"key": "amount", "value": {"path": "amount"}},
                                        {"key": "currency", "value": {"path": "currency"}},
                                        {"key": "category", "value": {"path": "category"}},
                                        {"key": "paymentMethod", "value": {"path": "paymentMethod"}},
                                        {"key": "memo", "value": {"path": "memo"}},
                                    ],
                                },
                            }
                        },
                    },
                    {
                        "id": "submit-button-text",
                        "component": {"Text": {"text": {"literalString": "申請する"}}},
                    },
                ],
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": _REVIEW_SURFACE_ID,
                "path": "/",
                "contents": [
                    {"key": "receiptName", "valueString": data.get("receiptName", "")},
                    {"key": "merchant", "valueString": data.get("merchant", "")},
                    {"key": "date", "valueString": data.get("date", "")},
                    {"key": "amount", "valueString": data.get("amount", "")},
                    {"key": "currency", "valueString": data.get("currency", "JPY")},
                    {"key": "category", "valueString": data.get("category", "")},
                    {"key": "paymentMethod", "valueString": data.get("paymentMethod", "")},
                    {"key": "memo", "valueString": data.get("memo", "")},
                ],
            }
        },
    ]


def _ensure_review_data_model(
    messages: list[dict[str, Any]], data: dict[str, Any]
) -> list[dict[str, Any]]:
    contents = _review_data_contents(data)
    data_update = None
    for message in messages:
        update = message.get("dataModelUpdate")
        if update and update.get("surfaceId") == _REVIEW_SURFACE_ID:
            data_update = update
            break

    if not data_update:
        messages.append(
            {
                "dataModelUpdate": {
                    "surfaceId": _REVIEW_SURFACE_ID,
                    "path": "/",
                    "contents": contents,
                }
            }
        )
        return messages

    if not data_update.get("contents"):
        data_update["contents"] = contents
    return messages


def _ensure_review_components(
    messages: list[dict[str, Any]], data: dict[str, Any]
) -> list[dict[str, Any]]:
    fallback = _build_review_fallback(data)
    fallback_components: list[dict[str, Any]] = []
    fallback_order: list[str] = []
    for message in fallback:
        update = message.get("surfaceUpdate")
        if update and update.get("surfaceId") == _REVIEW_SURFACE_ID:
            fallback_components = update.get("components", [])
            for component in fallback_components:
                if component.get("id") == "review-root":
                    try:
                        fallback_order = (
                            component.get("component", {})
                            .get("Column", {})
                            .get("children", {})
                            .get("explicitList", [])
                        )
                    except AttributeError:
                        fallback_order = []
            break

    required_by_id = {
        component.get("id"): component
        for component in fallback_components
        if component.get("id")
    }

    surface_update = None
    for message in messages:
        update = message.get("surfaceUpdate")
        if update and update.get("surfaceId") == _REVIEW_SURFACE_ID:
            surface_update = update
            break

    if not surface_update:
        messages.append(
            {
                "surfaceUpdate": {
                    "surfaceId": _REVIEW_SURFACE_ID,
                    "components": list(required_by_id.values()),
                }
            }
        )
        return messages

    components = surface_update.get("components")
    if not isinstance(components, list):
        surface_update["components"] = list(required_by_id.values())
        return messages

    existing_ids = {component.get("id") for component in components}
    for component_id, component in required_by_id.items():
        if component_id not in existing_ids:
            components.append(component)

    # Ensure the explicitList includes required components in order.
    for component in components:
        if component.get("id") != "review-root":
            continue
        column = component.get("component", {}).get("Column")
        if not isinstance(column, dict):
            continue
        children = column.get("children")
        if not isinstance(children, dict):
            continue
        explicit_list = children.get("explicitList")
        if not isinstance(explicit_list, list):
            children["explicitList"] = fallback_order or list(required_by_id.keys())
            continue
        for item_id in fallback_order:
            if item_id not in explicit_list:
                explicit_list.append(item_id)
    return messages


def build_ai_review(data: dict[str, Any]) -> list[dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; falling back to static review UI.")
        return _build_review_fallback(data)

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", _DEFAULT_MODEL)
    system_prompt = {
        "role": "system",
        "content": (
            "You output A2UI JSON only. Do not use markdown or code fences. "
            "Return a JSON array of A2UI message objects."
        ),
    }
    user_prompt = {
        "role": "user",
        "content": (
            "Create A2UI messages for an expense review page.\n"
            "Requirements:\n"
            "- Output ONLY a JSON array (no markdown, no code fences).\n"
            "- Use beginRendering, surfaceUpdate, dataModelUpdate message structure.\n"
            "- surfaceId must be \"expense-review\" and root id must be \"review-root\".\n"
            "- Use styles: primaryColor \"#2F5AFF\", font \"Roboto\".\n"
            "- Include Text components bound to receiptName, merchant, date, amount, currency, category, paymentMethod, memo.\n"
            "- Include a primary Button with action name \"submit_expense\" and context paths for those fields.\n"
            "Example shape (do not copy values, just follow structure):\n"
            "[\n"
            "  {\"beginRendering\": {\"surfaceId\": \"expense-review\", \"root\": \"review-root\", \"styles\": {\"primaryColor\": \"#2F5AFF\", \"font\": \"Roboto\"}}},\n"
            "  {\"surfaceUpdate\": {\"surfaceId\": \"expense-review\", \"components\": [\n"
            "    {\"id\": \"review-root\", \"component\": {\"Column\": {\"children\": {\"explicitList\": [\"review-title\", \"review-receipt\", \"review-merchant\", \"review-date\", \"review-amount\", \"review-currency\", \"review-category\", \"review-payment\", \"review-memo\", \"submit-button\"]}}}},\n"
            "    {\"id\": \"review-title\", \"component\": {\"Text\": {\"usageHint\": \"h2\", \"text\": {\"literalString\": \"申請内容の確認\"}}}},\n"
            "    {\"id\": \"review-receipt\", \"component\": {\"Text\": {\"text\": {\"path\": \"receiptName\"}}}},\n"
            "    {\"id\": \"submit-button\", \"component\": {\"Button\": {\"child\": \"submit-button-text\", \"primary\": true, \"action\": {\"name\": \"submit_expense\", \"context\": [{\"key\": \"receiptName\", \"value\": {\"path\": \"receiptName\"}}]}}}},\n"
            "    {\"id\": \"submit-button-text\", \"component\": {\"Text\": {\"text\": {\"literalString\": \"申請する\"}}}}\n"
            "  ]}},\n"
            "  {\"dataModelUpdate\": {\"surfaceId\": \"expense-review\", \"path\": \"/\", \"contents\": []}}\n"
            "]\n"
            f"Data:\n{json.dumps(data, ensure_ascii=False)}"
        ),
    }
    try:
        response = client.responses.create(
            model=model,
            input=[system_prompt, user_prompt],
            temperature=0.2,
        )
    except Exception as exc:
        logger.warning("OpenAI request failed; falling back. error=%s", exc)
        return _build_review_fallback(data)

    raw = response.output_text.strip()
    if raw:
        logger.info("OpenAI review UI response (truncated): %s", raw[:800])
    sanitized = raw
    if "```" in sanitized:
        sanitized = sanitized.replace("```json", "").replace("```", "").strip()
    start = sanitized.find("[")
    end = sanitized.rfind("]")
    if start != -1 and end != -1:
        sanitized = sanitized[start : end + 1]

    try:
        parsed = json.loads(sanitized)
    except json.JSONDecodeError:
        logger.warning("Failed to parse AI response as JSON; falling back.")
        return _build_review_fallback(data)

    if not isinstance(parsed, list):
        logger.warning("AI response is not a list; falling back.")
        return _build_review_fallback(data)

    if not any("beginRendering" in message for message in parsed):
        logger.warning("AI response missing beginRendering; falling back.")
        return _build_review_fallback(data)

    parsed = _ensure_review_components(parsed, data)
    return _ensure_review_data_model(parsed, data)


def build_expense_form(data: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "beginRendering": {
                "surfaceId": "expense-form",
                "root": "expense-root",
                "styles": {"primaryColor": "#2F5AFF", "font": "Roboto"},
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": "expense-form",
                "components": [
                    {
                        "id": "expense-root",
                        "component": {
                            "Column": {
                                "children": {
                                    "explicitList": [
                                        "form-title",
                                        "receipt-name",
                                        "merchant-field",
                                        "date-field",
                                        "amount-field",
                                        "currency-field",
                                        "category-field",
                                        "payment-field",
                                        "memo-field",
                                        "submit-button",
                                    ]
                                }
                            }
                        },
                    },
                    {
                        "id": "form-title",
                        "component": {
                            "Text": {
                                "usageHint": "h2",
                                "text": {"literalString": "経費申請フォーム"},
                            }
                        },
                    },
                    {
                        "id": "receipt-name",
                        "component": {"Text": {"text": {"path": "receiptName"}}},
                    },
                    {
                        "id": "merchant-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "支払先"},
                                "text": {"path": "merchant"},
                                "textFieldType": "shortText",
                            }
                        },
                    },
                    {
                        "id": "date-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "日付"},
                                "text": {"path": "date"},
                                "textFieldType": "date",
                            }
                        },
                    },
                    {
                        "id": "amount-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "金額"},
                                "text": {"path": "amount"},
                                "textFieldType": "number",
                            }
                        },
                    },
                    {
                        "id": "currency-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "通貨"},
                                "text": {"path": "currency"},
                                "textFieldType": "shortText",
                            }
                        },
                    },
                    {
                        "id": "category-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "カテゴリ"},
                                "text": {"path": "category"},
                                "textFieldType": "shortText",
                            }
                        },
                    },
                    {
                        "id": "payment-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "支払方法"},
                                "text": {"path": "paymentMethod"},
                                "textFieldType": "shortText",
                            }
                        },
                    },
                    {
                        "id": "memo-field",
                        "component": {
                            "TextField": {
                                "label": {"literalString": "備考"},
                                "text": {"path": "memo"},
                                "textFieldType": "longText",
                            }
                        },
                    },
                    {
                        "id": "submit-button",
                        "component": {
                            "Button": {
                                "child": "submit-button-text",
                                "primary": True,
                                "action": {
                                    "name": "submit_expense",
                                    "context": [
                                        {"key": "receiptName", "value": {"path": "receiptName"}},
                                        {"key": "merchant", "value": {"path": "merchant"}},
                                        {"key": "date", "value": {"path": "date"}},
                                        {"key": "amount", "value": {"path": "amount"}},
                                        {"key": "currency", "value": {"path": "currency"}},
                                        {"key": "category", "value": {"path": "category"}},
                                        {"key": "paymentMethod", "value": {"path": "paymentMethod"}},
                                        {"key": "memo", "value": {"path": "memo"}},
                                    ],
                                },
                            }
                        },
                    },
                    {
                        "id": "submit-button-text",
                        "component": {"Text": {"text": {"literalString": "申請する"}}},
                    },
                ],
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": "expense-form",
                "path": "/",
                "contents": [
                    {"key": "receiptName", "valueString": data.get("receiptName", "")},
                    {"key": "merchant", "valueString": data.get("merchant", "")},
                    {"key": "date", "valueString": data.get("date", "")},
                    {"key": "amount", "valueString": data.get("amount", "")},
                    {"key": "currency", "valueString": data.get("currency", "JPY")},
                    {"key": "category", "valueString": data.get("category", "")},
                    {"key": "paymentMethod", "valueString": data.get("paymentMethod", "")},
                    {"key": "memo", "valueString": data.get("memo", "")},
                ],
            }
        },
    ]


def build_confirmation(record: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "beginRendering": {
                "surfaceId": "expense-confirm",
                "root": "confirm-card",
                "styles": {"primaryColor": "#2F5AFF", "font": "Roboto"},
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": "expense-confirm",
                "components": [
                    {"id": "confirm-card", "component": {"Card": {"child": "confirm-column"}}},
                    {
                        "id": "confirm-column",
                        "component": {
                            "Column": {
                                "children": {
                                    "explicitList": [
                                        "confirm-title",
                                        "confirm-receipt",
                                        "confirm-merchant",
                                        "confirm-date",
                                        "confirm-amount",
                                        "confirm-category",
                                        "confirm-payment",
                                        "confirm-memo",
                                        "confirm-back",
                                    ]
                                }
                            }
                        },
                    },
                    {
                        "id": "confirm-title",
                        "component": {
                            "Text": {
                                "usageHint": "h2",
                                "text": {"literalString": "申請が完了しました"},
                            }
                        },
                    },
                    {"id": "confirm-receipt", "component": {"Text": {"text": {"path": "receiptName"}}}},
                    {"id": "confirm-merchant", "component": {"Text": {"text": {"path": "merchant"}}}},
                    {"id": "confirm-date", "component": {"Text": {"text": {"path": "date"}}}},
                    {"id": "confirm-amount", "component": {"Text": {"text": {"path": "amountDisplay"}}}},
                    {"id": "confirm-category", "component": {"Text": {"text": {"path": "category"}}}},
                    {"id": "confirm-payment", "component": {"Text": {"text": {"path": "paymentMethod"}}}},
                    {"id": "confirm-memo", "component": {"Text": {"text": {"path": "memo"}}}},
                    {
                        "id": "confirm-back",
                        "component": {
                            "Button": {
                                "child": "confirm-back-text",
                                "action": {"name": "back_to_top"},
                            }
                        },
                    },
                    {
                        "id": "confirm-back-text",
                        "component": {"Text": {"text": {"literalString": "TOPに戻る"}}},
                    },
                ],
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": "expense-confirm",
                "path": "/",
                "contents": [
                    {"key": "receiptName", "valueString": record.get("receiptName", "")},
                    {"key": "merchant", "valueString": record.get("merchant", "")},
                    {"key": "date", "valueString": record.get("date", "")},
                    {
                        "key": "amountDisplay",
                        "valueString": f"{record.get('amount', '')} {record.get('currency', '')}",
                    },
                    {"key": "category", "valueString": record.get("category", "")},
                    {"key": "paymentMethod", "valueString": record.get("paymentMethod", "")},
                    {"key": "memo", "valueString": record.get("memo", "")},
                ],
            }
        },
    ]


def build_search_results(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    items = []
    for idx, claim in enumerate(results, start=1):
        items.append(
            {
                "key": f"item{idx}",
                "valueMap": [
                    {"key": "merchant", "valueString": claim.get("merchant", "")},
                    {"key": "date", "valueString": claim.get("date", "")},
                    {
                        "key": "amountDisplay",
                        "valueString": f"{claim.get('amount', '')} {claim.get('currency', '')}",
                    },
                    {"key": "category", "valueString": claim.get("category", "")},
                    {"key": "memo", "valueString": claim.get("memo", "")},
                    {"key": "receiptName", "valueString": claim.get("receiptName", "")},
                ],
            }
        )

    return [
        {
            "beginRendering": {
                "surfaceId": "expense-search",
                "root": "results-root",
                "styles": {"primaryColor": "#2F5AFF", "font": "Roboto"},
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": "expense-search",
                "components": [
                    {
                        "id": "results-root",
                        "component": {
                            "Column": {
                                "children": {"explicitList": ["results-title", "results-list"]}
                            }
                        },
                    },
                    {
                        "id": "results-title",
                        "component": {
                            "Text": {
                                "usageHint": "h2",
                                "text": {"literalString": "検索結果"},
                            }
                        },
                    },
                    {
                        "id": "results-list",
                        "component": {
                            "List": {
                                "direction": "vertical",
                                "children": {
                                    "template": {
                                        "dataBinding": "/items",
                                        "componentId": "result-card-template",
                                    }
                                },
                            }
                        },
                    },
                    {
                        "id": "result-card-template",
                        "component": {"Card": {"child": "result-card-column"}},
                    },
                    {
                        "id": "result-card-column",
                        "component": {
                            "Column": {
                                "children": {
                                    "explicitList": [
                                        "result-merchant",
                                        "result-date",
                                        "result-amount",
                                        "result-category",
                                        "result-memo",
                                        "result-receipt",
                                    ]
                                }
                            }
                        },
                    },
                    {"id": "result-merchant", "component": {"Text": {"text": {"path": "merchant"}}}},
                    {"id": "result-date", "component": {"Text": {"text": {"path": "date"}}}},
                    {"id": "result-amount", "component": {"Text": {"text": {"path": "amountDisplay"}}}},
                    {"id": "result-category", "component": {"Text": {"text": {"path": "category"}}}},
                    {"id": "result-memo", "component": {"Text": {"text": {"path": "memo"}}}},
                    {"id": "result-receipt", "component": {"Text": {"text": {"path": "receiptName"}}}},
                ],
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": "expense-search",
                "path": "/",
                "contents": [
                    {"key": "items", "valueMap": items},
                ],
            }
        },
    ]


def build_entries_screen(
    entries: list[dict[str, Any]], layout: dict[str, Any]
) -> list[dict[str, Any]]:
    if not isinstance(layout, dict):
        layout = {}
    mode = str(layout.get("mode", "list")).lower()
    show_fields = layout.get(
        "showFields", ["title", "date", "amount", "currency", "memo"]
    )
    if isinstance(show_fields, str):
        show_fields = [show_fields]
    show_fields = [str(field) for field in show_fields]
    theme = str(layout.get("theme", "default")).lower()
    themes = {
        "default": {"primaryColor": "#2F5AFF", "font": "Roboto"},
        "forest": {"primaryColor": "#1F7A5C", "font": "Roboto"},
        "sunset": {"primaryColor": "#D95032", "font": "Roboto"},
    }
    styles = themes.get(theme, themes["default"])
    surface_id = f"entries-{mode}-{'-'.join(show_fields) or 'none'}"
    items = []
    for idx, entry in enumerate(entries, start=1):
        amount_display = f"{entry.get('amount', '')} {entry.get('currency', '')}".strip()
        item_map = []
        if "title" in show_fields:
            item_map.append({"key": "title", "valueString": entry.get("title", "")})
        if "date" in show_fields:
            item_map.append({"key": "date", "valueString": entry.get("date", "")})
        if "amount" in show_fields or "currency" in show_fields:
            item_map.append({"key": "amountDisplay", "valueString": amount_display})
        if "memo" in show_fields:
            item_map.append({"key": "memo", "valueString": entry.get("memo", "")})
        items.append(
            {
                "key": f"entry{idx}",
                "valueMap": item_map,
            }
        )

    field_components = []
    explicit_list = []
    if "title" in show_fields:
        field_components.append(
            {"id": "entry-title", "component": {"Text": {"text": {"path": "title"}}}}
        )
        explicit_list.append("entry-title")
    if "date" in show_fields:
        field_components.append(
            {"id": "entry-date", "component": {"Text": {"text": {"path": "date"}}}}
        )
        explicit_list.append("entry-date")
    if "amount" in show_fields or "currency" in show_fields:
        field_components.append(
            {
                "id": "entry-amount",
                "component": {"Text": {"text": {"path": "amountDisplay"}}},
            }
        )
        explicit_list.append("entry-amount")
    if "memo" in show_fields:
        field_components.append(
            {"id": "entry-memo", "component": {"Text": {"text": {"path": "memo"}}}}
        )
        explicit_list.append("entry-memo")

    return [
        {
            "beginRendering": {
                "surfaceId": surface_id,
                "root": "entries-root",
                "styles": styles,
            }
        },
        {
            "surfaceUpdate": {
                "surfaceId": surface_id,
                "components": [
                    {
                        "id": "entries-root",
                        "component": {
                            "Column": {
                                "children": {
                                    "explicitList": [
                                        "entries-title",
                                        "entries-mode",
                                        "entries-list",
                                    ]
                                }
                            }
                        },
                    },
                    {
                        "id": "entries-title",
                        "component": {
                            "Text": {
                                "usageHint": "h2",
                                "text": {"literalString": "経費エントリー一覧"},
                            }
                        },
                    },
                    {
                        "id": "entries-mode",
                        "component": {
                            "Text": {
                                "text": {
                                    "literalString": (
                                        f"表示モード: {mode.upper()} / "
                                        f"テーマ: {theme.upper()} / "
                                        f"fields: {', '.join(show_fields) or 'none'}"
                                    )
                                }
                            }
                        },
                    },
                    {
                        "id": "entries-list",
                        "component": {
                            "List": {
                                "direction": "horizontal" if mode == "grid" else "vertical",
                                "children": {
                                    "template": {
                                        "dataBinding": "/items",
                                        "componentId": "entry-card-template",
                                    }
                                },
                            }
                        },
                    },
                    {
                        "id": "entry-card-template",
                        "component": {"Card": {"child": "entry-card-column"}},
                    },
                    {
                        "id": "entry-card-column",
                        "component": {
                            "Column": {
                                "children": {"explicitList": explicit_list}
                            }
                        },
                    },
                    *field_components,
                ],
            }
        },
        {
            "dataModelUpdate": {
                "surfaceId": surface_id,
                "path": "/",
                "contents": [
                    {"key": "items", "valueMap": items},
                ],
            }
        },
    ]
