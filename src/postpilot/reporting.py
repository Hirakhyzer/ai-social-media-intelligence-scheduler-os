"""Markdown reporting for PostPilot OS."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def write_report(path: str | Path, summary: dict, radar: pd.DataFrame, platforms: pd.DataFrame, times: pd.DataFrame, calendar: pd.DataFrame, guard: pd.DataFrame, analytics: pd.DataFrame, experiments: pd.DataFrame) -> None:
    """Write an executive social-media strategy and scheduling report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    top_radar = radar.head(10)
    top_platforms = platforms.sort_values("platform_fit_score", ascending=False).head(12)
    content = f"""# Synthetic PostPilot OS Social Media Strategy Report

## Boundary

This report is generated from synthetic marketing data. It is planning support only. It does not post to real platforms, scrape private personal data, generate fake engagement, or bypass platform rules. Human approval is required before any real publishing adapter is used.

## Run summary

| Metric | Value |
| --- | --- |
| Synthetic trend topics | {summary.get('trend_topic_count', 0)} |
| Content drafts | {summary.get('content_draft_count', 0)} |
| Calendar items | {summary.get('calendar_item_count', 0)} |
| Queue mode | {summary.get('posting_mode', 'simulation_only')} |
| Mean brand-safety risk | {summary.get('mean_brand_safety_risk', 0):.4f} |
| Mean simulated engagement rate | {summary.get('mean_engagement_rate', 0):.4f} |

## Top trend opportunities

{_table(top_radar[['topic_id', 'topic', 'intent', 'content_opportunity_score', 'radar_reason']])}

## Strongest platform recommendations

{_table(top_platforms[['topic_id', 'platform', 'platform_fit_score', 'recommended_format', 'platform_reason']])}

## Next posting schedule

{_table(calendar.head(15)[['scheduled_datetime_local', 'platform', 'post_title', 'calendar_status', 'approval_state']])}

## Brand-safety audit

{_table(guard.head(15))}

## Synthetic analytics

{_table(analytics.head(15))}

## Experiment simulator

{_table(experiments.head(12))}

## Recommended next steps

1. Review all items marked `needs_review` or `blocked`.
2. Approve only posts that match brand policy and platform rules.
3. Export the calendar to a real scheduling tool only after human approval.
4. Use analytics as a planning signal, not as proof of real-world performance.
"""
    path.write_text(content, encoding="utf-8")


def _table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "No records."
    return frame.to_markdown(index=False)
