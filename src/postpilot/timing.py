"""Best-time posting recommendation engine."""

from __future__ import annotations

from datetime import datetime, timedelta

import pandas as pd

PLATFORM_HOUR_BONUS = {
    "LinkedIn": [8, 9, 10, 12, 15],
    "Instagram": [11, 13, 18, 20],
    "TikTok": [18, 20, 21],
    "YouTube Shorts": [12, 17, 19],
    "X": [8, 12, 17, 20],
    "Facebook": [10, 13, 19],
    "Blog": [9, 10, 14],
    "Newsletter": [8, 9, 11],
}


def recommend_posting_times(top_platforms: pd.DataFrame, priors: pd.DataFrame, start_date: str = "2026-08-05", horizon_days: int = 21) -> pd.DataFrame:
    """Assign recommended dates and times to topic-platform candidates."""
    if top_platforms.empty:
        return pd.DataFrame()
    start = datetime.fromisoformat(start_date)
    rows = []
    for idx, rec in enumerate(top_platforms.itertuples(index=False)):
        platform = str(rec.platform)
        day_offset = idx % max(1, horizon_days)
        date = start + timedelta(days=day_offset)
        hour, prior_score = _best_hour(platform, priors)
        urgency_bonus = min(0.12, float(getattr(rec, "platform_fit_score", 0.5)) * 0.08)
        weekday_bonus = 0.08 if date.weekday() < 5 else -0.02
        confidence = max(0.30, min(0.95, 0.48 + prior_score * 1.4 + urgency_bonus + weekday_bonus))
        rows.append({
            "topic_id": rec.topic_id,
            "topic": rec.topic,
            "platform": platform,
            "recommended_format": rec.recommended_format,
            "recommended_date": date.date().isoformat(),
            "recommended_time_local": f"{hour:02d}:00",
            "backup_time_local": f"{(hour + 2) % 24:02d}:00",
            "posting_time_confidence": round(confidence, 4),
            "timing_reason": _timing_reason(platform, hour, date.weekday(), confidence),
        })
    return pd.DataFrame(rows)


def timing_summary(times: pd.DataFrame) -> dict[str, int | float | str]:
    if times.empty:
        return {"timing_recommendation_count": 0, "mean_timing_confidence": 0.0}
    return {
        "timing_recommendation_count": int(len(times)),
        "mean_timing_confidence": float(times["posting_time_confidence"].mean()),
        "most_common_recommended_platform": str(times["platform"].mode().iloc[0]),
    }


def _best_hour(platform: str, priors: pd.DataFrame) -> tuple[int, float]:
    subset = priors[priors["platform"] == platform]
    if not subset.empty:
        row = subset.sort_values("expected_engagement_prior", ascending=False).iloc[0]
        return int(row["hour_local"]), float(row["expected_engagement_prior"])
    hours = PLATFORM_HOUR_BONUS.get(platform, [9])
    return int(hours[0]), 0.04


def _timing_reason(platform: str, hour: int, weekday: int, confidence: float) -> str:
    day_type = "weekday" if weekday < 5 else "weekend"
    confidence_label = "high" if confidence >= 0.72 else "moderate"
    return f"{platform} {day_type} slot at {hour:02d}:00 has {confidence_label} synthetic engagement confidence"
