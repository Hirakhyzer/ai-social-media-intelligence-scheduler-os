"""Synthetic performance analytics and learning loop."""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_performance(queue: pd.DataFrame, calendar: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Simulate post performance for research and planning."""
    if queue.empty:
        return pd.DataFrame()
    rng = np.random.default_rng(seed)
    rows = []
    by_draft = calendar.set_index("draft_id") if not calendar.empty else pd.DataFrame()
    for item in queue.itertuples(index=False):
        cal = by_draft.loc[item.draft_id] if item.draft_id in by_draft.index else None
        timing_conf = float(cal["posting_time_confidence"]) if cal is not None else 0.5
        brand_risk = float(cal["brand_safety_risk_score"]) if cal is not None else 0.2
        base = max(0.01, timing_conf * 0.08 + rng.normal(0.0, 0.01) - brand_risk * 0.02)
        impressions = int(rng.integers(800, 8000) * (0.75 + timing_conf))
        clicks = int(impressions * max(0.002, base * rng.uniform(0.25, 0.65)))
        engagements = int(impressions * max(0.004, base * rng.uniform(0.8, 1.8)))
        rows.append({
            "queue_id": item.queue_id,
            "draft_id": item.draft_id,
            "platform": item.platform,
            "simulated_impressions": impressions,
            "simulated_clicks": clicks,
            "simulated_engagements": engagements,
            "simulated_ctr": round(clicks / impressions, 5) if impressions else 0.0,
            "simulated_engagement_rate": round(engagements / impressions, 5) if impressions else 0.0,
            "learning_signal": "increase_frequency" if engagements / max(impressions, 1) >= 0.06 else "keep_testing",
        })
    return pd.DataFrame(rows)


def analytics_summary(analytics: pd.DataFrame) -> dict[str, int | float | str]:
    if analytics.empty:
        return {"analytics_record_count": 0, "mean_engagement_rate": 0.0}
    return {
        "analytics_record_count": int(len(analytics)),
        "mean_engagement_rate": float(analytics["simulated_engagement_rate"].mean()),
        "mean_ctr": float(analytics["simulated_ctr"].mean()),
        "best_simulated_platform": str(analytics.groupby("platform")["simulated_engagement_rate"].mean().sort_values(ascending=False).index[0]),
    }
