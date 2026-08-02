import json
import subprocess
import sys
from pathlib import Path


def test_script_runs(tmp_path: Path):
    result = subprocess.run(
        [sys.executable, "scripts/run_synthetic_postpilot_lab.py", "--topics", "12", "--segments", "4", "--campaigns", "3", "--days", "7", "--seed", "5", "--output-dir", str(tmp_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    summary = json.loads(result.stdout)
    assert summary["trend_topic_count"] == 12
    assert summary["posting_mode"] == "simulation_only"
    assert (tmp_path / "results" / "synthetic_content_calendar.csv").exists()
    assert (tmp_path / "reports" / "synthetic_social_media_strategy_report.md").exists()
