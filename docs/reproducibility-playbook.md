# Reproducibility Playbook

This playbook defines how to run and report experiments from **PostPilot OS** so another researcher can inspect the workflow.

## Minimum run record

Every experiment should record:

| Field | Example |
|---|---|
| Run name | `postpilot_seed_42_topics_80_days_30` |
| Dataset type | synthetic social-media planning signals |
| Topics | `80` |
| Audience segments | `12` |
| Campaigns | `10` |
| Planning window | `30 days` |
| Random seed | `42` |
| Platforms | LinkedIn, X, Instagram, YouTube Shorts, Blog, Newsletter |
| Guardrails | spam-risk, claim-risk, sensitive targeting, fake engagement language |
| Output directory | `outputs/` |
| Boundary statement | simulation only; no real posting or platform scraping |

## Recommended command

```bash
python scripts/run_synthetic_postpilot_lab.py --topics 80 --segments 12 --campaigns 10 --days 30 --seed 42
```

## Evidence bundle

A complete run should include:

```text
outputs/results/synthetic_trend_signals.csv
outputs/results/synthetic_audience_segments.csv
outputs/results/synthetic_campaigns.csv
outputs/results/synthetic_brand_profile.csv
outputs/results/synthetic_trend_radar.csv
outputs/results/synthetic_platform_recommendations.csv
outputs/results/synthetic_best_time_recommendations.csv
outputs/results/synthetic_content_drafts.csv
outputs/results/synthetic_brand_safety_audit.csv
outputs/results/synthetic_content_calendar.csv
outputs/results/synthetic_schedule_queue.csv
outputs/results/synthetic_performance_analytics.csv
outputs/results/synthetic_ab_test_results.csv
outputs/results/synthetic_postpilot_summary.json
outputs/reports/synthetic_social_media_strategy_report.md
outputs/audit/postpilot_audit_log.jsonl
outputs/figures/
```

## Interpretation rules

- Report opportunity scores as planning signals, not guaranteed performance.
- Separate synthetic analytics from real platform analytics.
- Treat best-time recommendations as hypotheses for human review.
- Report brand-safety risk flags with final human decisions.
- Preserve the hash-chained audit log when sharing results.

## Checklist before sharing results

- [ ] Seed and configuration recorded.
- [ ] Simulation-only boundary stated.
- [ ] Platform policy assumptions documented.
- [ ] No real scraping or posting claim is made.
- [ ] Brand-safety and ethical-marketing checks included.
- [ ] Calendar, queue, analytics, and report outputs included.
- [ ] Audit log preserved.