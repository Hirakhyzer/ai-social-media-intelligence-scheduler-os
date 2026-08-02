"""Content calendar builder."""

from __future__ import annotations

import pandas as pd


def build_content_calendar(drafts: pd.DataFrame, times: pd.DataFrame, guard: pd.DataFrame) -> pd.DataFrame:
    """Combine drafts, timing recommendations, and brand guard output into one calendar."""
    if drafts.empty:
        return pd.DataFrame()
    calendar = drafts.merge(times[["topic_id", "recommended_date", "recommended_time_local", "backup_time_local", "posting_time_confidence", "timing_reason"]], on="topic_id", how="left")
    calendar = calendar.merge(guard, on=["draft_id", "platform"], how="left")
    calendar["calendar_status"] = calendar["approval_state"].map({
        "human_review_required": "ready_for_review",
        "needs_review": "needs_review",
        "blocked": "blocked",
    }).fillna("needs_review")
    calendar["scheduled_datetime_local"] = calendar["recommended_date"].astype(str) + " " + calendar["recommended_time_local"].astype(str)
    calendar["owner"] = "human_marketing_reviewer"
    return calendar.sort_values(["recommended_date", "recommended_time_local", "platform"]).reset_index(drop=True)


def calendar_summary(calendar: pd.DataFrame) -> dict[str, int | str]:
    if calendar.empty:
        return {"calendar_item_count": 0, "ready_for_review_count": 0}
    return {
        "calendar_item_count": int(len(calendar)),
        "ready_for_review_count": int((calendar["calendar_status"] == "ready_for_review").sum()),
        "blocked_calendar_item_count": int((calendar["calendar_status"] == "blocked").sum()),
        "first_scheduled_slot": str(calendar.iloc[0]["scheduled_datetime_local"]),
    }
