from pathlib import Path

from postpilot.audit import append_record, verify_log


def test_hash_chain(tmp_path: Path):
    path = tmp_path / "audit.jsonl"
    append_record(path, {"run": 1})
    append_record(path, {"run": 2})
    result = verify_log(path)
    assert result["valid"] is True
    assert result["records"] == 2
