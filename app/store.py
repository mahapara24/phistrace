"""In-memory docket list. It clears when the process stops."""

from __future__ import annotations

import secrets
import threading
from collections import deque
from datetime import datetime

_LOCK = threading.Lock()
_ORDER: deque[str] = deque(maxlen=40)
_BY_ID: dict[str, dict[str, object]] = {}


def save(body: dict[str, object]) -> dict[str, object]:
    record = {
        "id": "PT-" + secrets.token_hex(3).upper(),
        "created": datetime.now().strftime("%d %b %Y · %H:%M"),
        **body,
    }
    with _LOCK:
        _BY_ID[str(record["id"])] = record
        _ORDER.appendleft(str(record["id"]))
        live = set(_ORDER)
        for stale in [key for key in _BY_ID if key not in live]:
            del _BY_ID[stale]
    return record


def get(report_id: str) -> dict[str, object] | None:
    with _LOCK:
        return _BY_ID.get(report_id)


def recent(limit: int = 40) -> list[dict[str, object]]:
    with _LOCK:
        return [_BY_ID[key] for key in list(_ORDER)[:limit] if key in _BY_ID]
