"""Run PostPilot OS: the synthetic AI social media intelligence scheduler.

The command uses synthetic trend, audience, campaign, platform, and engagement
signals. It demonstrates trend radar scoring, platform selection, best-time
recommendations, content draft generation, brand-safety review, calendar
construction, schedule queue simulation, analytics, experiments, figures, and a
hash-chained audit log.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from postpilot.analytics import analytics_summary
from postpilot.audit import append_record, verify_log
from postpilot.brand_guard import brand_guard_summary
from postpilot.calendar import calendar_summary
from postpilot.config import ensure_output_dirs, set_seed
from postpilot.content import content_summary
from postpilot.experiments import experiments_summary
from postpilot.kernel import run_postpilot_kernel
from postpilot.platform import platform_summary
from postpilot.radar import radar_summary
from postpilot.reporting import write_report
from postpilot.scheduler import scheduler_summary
from postpilot.synthetic import SyntheticPostPilotConfig
from postpilot.timing import timing_summary
from postpilot.visualization import (
    plot_best_times,
    plot_brand_safety,
    plot_calendar_density,
    plot_engagement_forecast,
    plot_platform_fit,
    plot_trend_opportunities,
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a synthetic AI social media intelligence and scheduler OS lab.")
    parser.add_argument("--topics", type=int, default=42)
    parser.add_argument("--segments", type=int, default=8)
    parser.add_argument("--campaigns", type=int, default=6)
    parser.add_argument("--days", type=int, default=21)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--start-date", default="2026-08-05")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()

    set_seed(args.seed)
    outputs = ensure_output_dirs(args.output_dir)
    run = run_postpilot_kernel(SyntheticPostPilotConfig(
        topics=args.topics,
        segments=args.segments,
        campaigns=args.campaigns,
        days=args.days,
        seed=args.seed,
        start_date=args.start_date,
    ))

    summary = {
        "seed": args.seed,
        "start_date": args.start_date,
        "synthetic_topic_count": int(len(run.data["trends"])),
        "synthetic_segment_count": int(len(run.data["segments"])),
        "synthetic_campaign_count": int(len(run.data["campaigns"])),
        "data_origin": "synthetic fictional marketing, audience, trend, campaign, and engagement signals",
        "decision_boundary": "planning and schedule simulation only; no spam, fake engagement, private data scraping, or real posting without human approval",
    }
    summary.update(radar_summary(run.radar))
    summary.update(platform_summary(run.platforms))
    summary.update(timing_summary(run.times))
    summary.update(content_summary(run.drafts))
    summary.update(brand_guard_summary(run.brand_audit))
    summary.update(calendar_summary(run.calendar))
    summary.update(scheduler_summary(run.queue))
    summary.update(analytics_summary(run.analytics))
    summary.update(experiments_summary(run.experiments))

    run.data["trends"].to_csv(outputs["results"] / "synthetic_trend_signals.csv", index=False)
    run.data["segments"].to_csv(outputs["results"] / "synthetic_audience_segments.csv", index=False)
    run.data["campaigns"].to_csv(outputs["results"] / "synthetic_campaigns.csv", index=False)
    run.data["brand"].to_csv(outputs["results"] / "synthetic_brand_profile.csv", index=False)
    run.radar.to_csv(outputs["results"] / "synthetic_trend_radar.csv", index=False)
    run.platforms.to_csv(outputs["results"] / "synthetic_platform_recommendations.csv", index=False)
    run.times.to_csv(outputs["results"] / "synthetic_best_time_recommendations.csv", index=False)
    run.drafts.to_csv(outputs["results"] / "synthetic_content_drafts.csv", index=False)
    run.brand_audit.to_csv(outputs["results"] / "synthetic_brand_safety_audit.csv", index=False)
    run.calendar.to_csv(outputs["results"] / "synthetic_content_calendar.csv", index=False)
    run.queue.to_csv(outputs["results"] / "synthetic_schedule_queue.csv", index=False)
    run.analytics.to_csv(outputs["results"] / "synthetic_performance_analytics.csv", index=False)
    run.experiments.to_csv(outputs["results"] / "synthetic_ab_test_results.csv", index=False)

    audit_path = outputs["audit"] / "postpilot_audit_log.jsonl"
    append_record(audit_path, {**summary, "boundary": "ethical synthetic social media planning and schedule simulation only"})
    summary["audit_log"] = verify_log(audit_path)
    (outputs["results"] / "synthetic_postpilot_summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    write_report(outputs["reports"] / "synthetic_social_media_strategy_report.md", summary, run.radar, run.platforms, run.times, run.calendar, run.brand_audit, run.analytics, run.experiments)
    plot_trend_opportunities(run.radar, outputs["figures"] / "trend_opportunity_scores.png")
    plot_platform_fit(run.platforms, outputs["figures"] / "platform_fit_scores.png")
    plot_best_times(run.times, outputs["figures"] / "best_posting_times.png")
    plot_calendar_density(run.calendar, outputs["figures"] / "content_calendar_density.png")
    plot_brand_safety(run.brand_audit, outputs["figures"] / "brand_safety_risk.png")
    plot_engagement_forecast(run.analytics, outputs["figures"] / "engagement_forecast.png")

    print(json.dumps(summary, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    main()
