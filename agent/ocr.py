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

import base64
import io
import re
from dataclasses import dataclass
from typing import Iterable

from pdf2image import convert_from_bytes
from PIL import Image
import pytesseract


@dataclass
class OcrResult:
    receipt_name: str
    text: str
    merchant: str
    date: str
    amount: str
    currency: str


def _strip_data_url(data: str) -> str:
    if data.startswith("data:"):
        return data.split(",", 1)[1]
    return data


def _images_from_bytes(file_bytes: bytes, file_type: str) -> Iterable[Image.Image]:
    if file_type.lower().endswith("pdf"):
        return convert_from_bytes(file_bytes)
    image = Image.open(io.BytesIO(file_bytes))
    return [image]


def _detect_currency(text: str) -> str:
    if "USD" in text or "$" in text:
        return "USD"
    if "EUR" in text or "€" in text:
        return "EUR"
    if "¥" in text or "￥" in text:
        return "JPY"
    return "JPY"


def _extract_date(text: str) -> str:
    patterns = [
        r"\b(20\d{2}[/-]\d{1,2}[/-]\d{1,2})\b",
        r"\b(20\d{2}\.\d{1,2}\.\d{1,2})\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).replace(".", "/")
    return ""


def _extract_amount(text: str) -> str:
    matches = re.findall(r"(?:¥|￥|\$|€)?\s?([\d,]+(?:\.\d{1,2})?)", text)
    amounts = []
    for raw in matches:
        normalized = raw.replace(",", "")
        try:
            amounts.append(float(normalized))
        except ValueError:
            continue
    if not amounts:
        return ""
    return f"{max(amounts):.2f}"


def _extract_merchant(text: str) -> str:
    for line in text.splitlines():
        cleaned = line.strip()
        if not cleaned:
            continue
        if re.fullmatch(r"[\d\W]+", cleaned):
            continue
        return cleaned
    return ""


def extract_from_base64(
    file_base64: str, file_type: str, receipt_name: str
) -> OcrResult:
    decoded = base64.b64decode(_strip_data_url(file_base64))
    images = _images_from_bytes(decoded, file_type)
    text_parts = []
    for image in images:
        text_parts.append(pytesseract.image_to_string(image))
    text = "\n".join([part.strip() for part in text_parts if part.strip()])

    merchant = _extract_merchant(text)
    date = _extract_date(text)
    amount = _extract_amount(text)
    currency = _detect_currency(text)

    return OcrResult(
        receipt_name=receipt_name,
        text=text,
        merchant=merchant,
        date=date,
        amount=amount,
        currency=currency,
    )
