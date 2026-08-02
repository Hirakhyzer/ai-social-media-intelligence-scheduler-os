"""PostPilot OS kernel orchestration layer."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from .analytics import simulate_performance
from .brand_guard import audit_brand_safety
from .calendar import build_content_calendar
from .content import generate_content_drafts
from .experiments import simulate_ab_tests
from .platform import recommend_platforms, top_platform_per_topic
from .radar import score_trend_opportunities
from .scheduler import build_schedule_queue
from .synthetic import SyntheticPostPilotConfig, generate_synthetic_postpilot_data
from .timing import recommend_posting_times


@dataclass(frozen=True)
class PostPilotRun:
    data: dict[str, pd.DataFrame]
    radar: pd.DataFrame
    platforms: pd.DataFrame
    top_platforms: pd.DataFrame
    times: pd.DataFrame
    drafts: pd.DataFrame
    brand_audit: pd.DataFrame
    calendar: pd.DataFrame
    queue: pd.DataFrame
    analytics: pd.DataFrame
    experiments: pd.DataFrame


def run_postpilot_kernel(config: SyntheticPostPilotConfig) -> PostPilotRun:
    """Run the full synthetic OS pipeline from trend discovery to schedule queue."""
    data = generate_synthetic_postpilot_data(config)
    radar = score_trend_opportunities(data["trends"], data["segments"])
    platforms = recommend_platforms(radar, data["segments"])
    top_platforms = top_platform_per_topic(platforms)
    times = recommend_posting_times(top_platforms, data["performance_priors"], start_date=config.start_date, horizon_days=config.days)
    drafts = generate_content_drafts(times, data["campaigns"])
    brand_audit = audit_brand_safety(drafts, data["brand"])
    calendar = build_content_calendar(drafts, times, brand_audit)
    queue = build_schedule_queue(calendar)
    analytics = simulate_performance(queue, calendar, seed=config.seed)
    experiments = simulate_ab_tests(calendar, seed=config.seed)
    return PostPilotRun(data, radar, platforms, top_platforms, times, drafts, brand_audit, calendar, queue, analytics, experiments)
