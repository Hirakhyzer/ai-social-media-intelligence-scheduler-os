"""Hash-chained audit ledger for reproducible PostPilot OS runs."""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def append_record(path: str | Path, payload: dict[str, Any]) -> dict[str, Any]:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    previous_hash = _last_hash(path)
    record = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "previous_hash": previous_hash,
        "payload": payload,
    }
    record["record_hash"] = _hash_record(record)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")
    return record


def verify_log(path: str | Path) -> dict[str, int | bool | str]:
    path = Path(path)
    if not path.exists():
        return {"exists": False, "valid": True, "records": 0, "last_hash": ""}
    previous = "GENESIS"
    records = 0
    last_hash = ""
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            current_hash = record.get("record_hash", "")
            stored = dict(record)
            stored.pop("record_hash", None)
            if record.get("previous_hash") != previous or _hash_record(stored) != current_hash:
                return {"exists": True, "valid": False, "records": records, "last_hash": last_hash}
            previous = current_hash
            last_hash = current_hash
            records += 1
    return {"exists": True, "valid": True, "records": records, "last_hash": last_hash}


def _last_hash(path: Path) -> str:
    if not path.exists():
        return "GENESIS"
    last = "GENESIS"
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                last = json.loads(line).get("record_hash", "GENESIS")
    return last


def _hash_record(record: dict[str, Any]) -> str:
    blob = json.dumps(record, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()
