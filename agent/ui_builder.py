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
