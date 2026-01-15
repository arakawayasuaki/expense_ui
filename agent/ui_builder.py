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
                                        "review-receipt",
                                        "review-merchant",
                                        "review-date",
                                        "review-amount",
                                        "review-currency",
                                        "review-category",
                                        "review-payment",
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
                    {"id": "review-receipt", "component": {"Text": {"text": {"path": "receiptName"}}}},
                    {"id": "review-merchant", "component": {"Text": {"text": {"path": "merchant"}}}},
                    {"id": "review-date", "component": {"Text": {"text": {"path": "date"}}}},
                    {"id": "review-amount", "component": {"Text": {"text": {"path": "amount"}}}},
                    {"id": "review-currency", "component": {"Text": {"text": {"path": "currency"}}}},
                    {"id": "review-category", "component": {"Text": {"text": {"path": "category"}}}},
                    {"id": "review-payment", "component": {"Text": {"text": {"path": "paymentMethod"}}}},
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


def build_ai_review(data: dict[str, Any]) -> list[dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY not set; falling back to static review UI.")
        return _build_review_fallback(data)

    client = OpenAI(api_key=api_key)
    model = os.getenv("OPENAI_MODEL", _DEFAULT_MODEL)
    prompt = {
        "role": "user",
        "content": (
            "You generate A2UI JSON messages. Build a concise review page UI for an expense report.\n"
            "Requirements:\n"
            "- Output ONLY a JSON array of A2UI messages (list of objects).\n"
            "- Use surfaceId: \"expense-review\" and root id: \"review-root\".\n"
            "- Include Text components for receiptName, merchant, date, amount, currency, category, paymentMethod, memo.\n"
            "- Include a primary Button with action name \"submit_expense\" that passes those fields via context paths.\n"
            "- Use styles primaryColor #2F5AFF and font Roboto.\n"
            f"Data:\n{json.dumps(data, ensure_ascii=False)}"
        ),
    }
    try:
        response = client.responses.create(
            model=model,
            input=[prompt],
            temperature=0.2,
        )
    except Exception as exc:
        logger.warning("OpenAI request failed; falling back. error=%s", exc)
        return _build_review_fallback(data)

    raw = response.output_text.strip()
    if raw:
        logger.info("OpenAI review UI response (truncated): %s", raw[:800])
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        logger.warning("Failed to parse AI response as JSON; falling back.")
        return _build_review_fallback(data)

    if not isinstance(parsed, list):
        logger.warning("AI response is not a list; falling back.")
        return _build_review_fallback(data)
    return parsed


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
