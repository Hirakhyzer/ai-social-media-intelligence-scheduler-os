"""Trend radar and opportunity scoring.

Real adapters can be added later for RSS or approved public APIs. The default
pipeline uses synthetic trend signals for reproducible research.
"""

from __future__ import annotations

import pandas as pd


def score_trend_opportunities(trends: pd.DataFrame, segments: pd.DataFrame) -> pd.DataFrame:
    """Score topics by growth, urgency, evergreen value, saturation, and audience fit."""
    if trends.empty:
        return pd.DataFrame()
    avg_b2b = float(segments["b2b_affinity"].mean()) if not segments.empty else 0.5
    rows = []
    for trend in trends.itertuples(index=False):
        growth = float(trend.trend_growth_score)
        urgency = float(trend.topic_urgency_score)
        evergreen = float(trend.evergreen_score)
        saturation_penalty = float(trend.market_saturation_score) * 0.25
        noise_penalty = float(trend.competitor_noise_score) * 0.15
        audience_match = min(1.0, 0.45 + avg_b2b * 0.35 + evergreen * 0.20)
        opportunity = max(0.0, min(1.0, growth * 0.35 + urgency * 0.25 + evergreen * 0.20 + audience_match * 0.20 - saturation_penalty - noise_penalty))
        rows.append({
            "topic_id": trend.topic_id,
            "topic": trend.topic,
            "vertical": trend.vertical,
            "intent": trend.intent,
            "source_type": trend.source_type,
            "trend_growth_score": growth,
            "topic_urgency_score": urgency,
            "audience_match_score": round(audience_match, 4),
            "market_saturation_score": float(trend.market_saturation_score),
            "content_opportunity_score": round(opportunity, 4),
            "radar_reason": _reason(opportunity, growth, urgency, evergreen),
        })
    return pd.DataFrame(rows).sort_values("content_opportunity_score", ascending=False).reset_index(drop=True)


def radar_summary(radar: pd.DataFrame) -> dict[str, int | float | str]:
    if radar.empty:
        return {"trend_topic_count": 0, "mean_opportunity_score": 0.0, "top_topic": "none"}
    return {
        "trend_topic_count": int(len(radar)),
        "mean_opportunity_score": float(radar["content_opportunity_score"].mean()),
        "top_topic": str(radar.iloc[0]["topic"]),
        "high_opportunity_topic_count": int((radar["content_opportunity_score"] >= 0.62).sum()),
    }


def _reason(opportunity: float, growth: float, urgency: float, evergreen: float) -> str:
    if opportunity >= 0.7:
        return "strong near-term content opportunity with good audience fit"
    if growth >= 0.65:
        return "growing topic worth testing with controlled frequency"
    if urgency >= 0.65:
        return "time-sensitive topic that should be scheduled soon"
    if evergreen >= 0.65:
        return "evergreen topic suitable for educational content"
    return "moderate topic; keep in backlog or use as secondary content"
