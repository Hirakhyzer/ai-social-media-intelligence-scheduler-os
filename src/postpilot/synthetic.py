"""Synthetic data generation for PostPilot OS.

The generator creates fictional trend signals, audience segments, campaign briefs,
brand rules, and performance priors. No real user data is collected.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SyntheticPostPilotConfig:
    topics: int = 42
    segments: int = 8
    campaigns: int = 6
    days: int = 21
    seed: int = 42
    start_date: str = "2026-08-05"


PLATFORMS = ["LinkedIn", "Instagram", "TikTok", "YouTube Shorts", "X", "Facebook", "Blog", "Newsletter"]
FORMATS = ["expert_post", "carousel", "short_video", "thread", "how_to", "case_study", "newsletter_note", "blog_outline"]
VERTICALS = ["AI automation", "cybersecurity", "student tech", "small business", "research tools", "productivity", "creator tools", "ethical marketing"]
INTENTS = ["awareness", "education", "conversion", "community", "retention", "launch"]


def generate_synthetic_postpilot_data(config: SyntheticPostPilotConfig) -> dict[str, pd.DataFrame]:
    """Generate fictional source data for the complete pipeline."""
    rng = np.random.default_rng(config.seed)
    start = datetime.fromisoformat(config.start_date)

    trends = []
    for idx in range(config.topics):
        vertical = VERTICALS[idx % len(VERTICALS)]
        intent = INTENTS[idx % len(INTENTS)]
        growth = float(rng.beta(2.4, 2.0))
        saturation = float(rng.beta(1.8, 3.2))
        urgency = float(rng.beta(2.0, 2.5))
        evergreen = float(rng.beta(2.6, 2.4))
        competitor_noise = float(rng.beta(2.0, 2.7))
        trends.append({
            "topic_id": f"TOPIC-{idx+1:03d}",
            "topic": f"{vertical} {intent} playbook {idx+1}",
            "vertical": vertical,
            "intent": intent,
            "source_type": rng.choice(["news", "rss", "search_snapshot", "hashtag_proxy", "competitor_public_post", "seasonal_calendar"]),
            "trend_growth_score": round(growth, 4),
            "topic_urgency_score": round(urgency, 4),
            "evergreen_score": round(evergreen, 4),
            "market_saturation_score": round(saturation, 4),
            "competitor_noise_score": round(competitor_noise, 4),
            "detected_date": (start + timedelta(days=int(rng.integers(0, config.days)))).date().isoformat(),
            "synthetic_origin": True,
        })

    segments = []
    for idx in range(config.segments):
        segments.append({
            "segment_id": f"SEG-{idx+1:02d}",
            "segment_name": rng.choice(["founders", "students", "researchers", "security_teams", "content_creators", "small_business", "developers", "marketing_ops"]),
            "primary_timezone": rng.choice(["Asia/Karachi", "Asia/Singapore", "Europe/London", "America/New_York", "America/Los_Angeles"]),
            "b2b_affinity": round(float(rng.beta(2.5, 2.0)), 4),
            "visual_content_affinity": round(float(rng.beta(2.2, 2.2)), 4),
            "short_video_affinity": round(float(rng.beta(2.0, 2.1)), 4),
            "long_form_affinity": round(float(rng.beta(2.1, 2.3)), 4),
            "email_affinity": round(float(rng.beta(2.0, 2.4)), 4),
            "privacy_sensitivity": round(float(rng.beta(2.5, 2.1)), 4),
        })

    campaigns = []
    for idx in range(config.campaigns):
        campaigns.append({
            "campaign_id": f"CMP-{idx+1:02d}",
            "campaign_name": f"{rng.choice(VERTICALS)} {rng.choice(INTENTS)} sprint",
            "goal": rng.choice(INTENTS),
            "target_segment_id": f"SEG-{int(rng.integers(1, config.segments+1)):02d}",
            "brand_tone": rng.choice(["credible", "helpful", "clear", "technical", "friendly"]),
            "posting_frequency_per_week": int(rng.integers(3, 7)),
            "human_approval_required": True,
        })

    brand = pd.DataFrame([{
        "brand_id": "BRAND-001",
        "brand_name": "Synthetic Growth Lab",
        "allowed_claim_strength": "evidence_based",
        "forbidden_tactics": "spam,fake_reviews,impersonation,deceptive_claims,political_persuasion_targeting,private_data_scraping",
        "required_review_state": "human_approved_before_real_posting",
        "tone_keywords": "credible,helpful,clear,ethical,practical",
    }])

    priors = []
    for platform in PLATFORMS:
        for hour in [8, 9, 11, 13, 15, 18, 20]:
            priors.append({
                "platform": platform,
                "hour_local": hour,
                "weekday_bonus": round(float(rng.normal(0.08, 0.04)), 4),
                "expected_engagement_prior": round(float(np.clip(rng.normal(0.055, 0.025), 0.01, 0.16)), 4),
                "format_preference": rng.choice(FORMATS),
            })

    return {
        "trends": pd.DataFrame(trends),
        "segments": pd.DataFrame(segments),
        "campaigns": pd.DataFrame(campaigns),
        "brand": brand,
        "performance_priors": pd.DataFrame(priors),
    }
