from __future__ import annotations

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).resolve().parent / "data"
ENTRIES_PATH = DATA_DIR / "entries.json"


def load_entries() -> dict[str, Any]:
    if not ENTRIES_PATH.exists():
        return {"entries": [], "layout": {}}
    payload = json.loads(ENTRIES_PATH.read_text(encoding="utf-8"))
    if isinstance(payload, list):
        return {"entries": payload, "layout": {}}
    if isinstance(payload, dict):
        return {
            "entries": payload.get("entries", []),
            "layout": payload.get("layout", {}),
        }
    return {"entries": [], "layout": {}}
