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

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import uuid4


DATA_DIR = Path(__file__).resolve().parent / "data"
CLAIMS_PATH = DATA_DIR / "claims.json"


def _ensure_storage() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    if not CLAIMS_PATH.exists():
        CLAIMS_PATH.write_text("[]", encoding="utf-8")


def load_claims() -> list[dict[str, Any]]:
    _ensure_storage()
    return json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))


def save_claims(claims: list[dict[str, Any]]) -> None:
    _ensure_storage()
    CLAIMS_PATH.write_text(
        json.dumps(claims, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def add_claim(payload: dict[str, Any]) -> dict[str, Any]:
    claims = load_claims()
    record = {
        "id": str(uuid4()),
        "createdAt": datetime.utcnow().isoformat(),
        **payload,
    }
    claims.append(record)
    save_claims(claims)
    return record


def search_claims(query: str) -> list[dict[str, Any]]:
    claims = load_claims()
    if not query:
        return claims

    lowered = query.lower()
    results = []
    for claim in claims:
        haystack = " ".join(
            str(value)
            for key, value in claim.items()
            if key not in {"id", "createdAt"}
        ).lower()
        if lowered in haystack:
            results.append(claim)
    return results
