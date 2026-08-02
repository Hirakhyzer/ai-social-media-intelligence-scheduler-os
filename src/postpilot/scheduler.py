"""Post queue and schedule simulation.

This module never posts to real platforms. It creates a deterministic queue that
can later be connected to approved platform adapters with explicit credentials
and human approval checks.
"""

from __future__ import annotations

import pandas as pd


def build_schedule_queue(calendar: pd.DataFrame) -> pd.DataFrame:
    """Create a simulated post queue from the approved/reviewable calendar."""
    if calendar.empty:
        return pd.DataFrame()
    rows = []
    for idx, item in enumerate(calendar.itertuples(index=False)):
        simulated_state = "queued_for_human_approval" if item.calendar_status == "ready_for_review" else item.calendar_status
        rows.append({
            "queue_id": f"QUEUE-{idx+1:04d}",
            "draft_id": item.draft_id,
            "platform": item.platform,
            "scheduled_datetime_local": item.scheduled_datetime_local,
            "queue_state": simulated_state,
            "requires_human_approval": True,
            "real_adapter_enabled": False,
            "posting_mode": "simulation_only",
            "postpilot_boundary": "no_real_posting_from_default_pipeline",
        })
    return pd.DataFrame(rows)


def scheduler_summary(queue: pd.DataFrame) -> dict[str, int | str]:
    if queue.empty:
        return {"schedule_queue_count": 0, "real_adapter_enabled_count": 0}
    return {
        "schedule_queue_count": int(len(queue)),
        "queued_for_human_approval_count": int((queue["queue_state"] == "queued_for_human_approval").sum()),
        "real_adapter_enabled_count": int(queue["real_adapter_enabled"].sum()),
        "posting_mode": "simulation_only",
    }
