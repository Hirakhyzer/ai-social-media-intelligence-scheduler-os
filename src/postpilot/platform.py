"""Platform fit scoring for social and owned channels."""

from __future__ import annotations

import pandas as pd

PLATFORM_RULES = {
    "LinkedIn": {"b2b": 0.95, "visual": 0.45, "short_video": 0.45, "long_form": 0.75, "email": 0.30, "max_posts_per_week": 5, "best_formats": "expert_post,carousel,case_study"},
    "Instagram": {"b2b": 0.35, "visual": 0.95, "short_video": 0.75, "long_form": 0.25, "email": 0.10, "max_posts_per_week": 7, "best_formats": "carousel,reel,story"},
    "TikTok": {"b2b": 0.25, "visual": 0.80, "short_video": 0.98, "long_form": 0.10, "email": 0.05, "max_posts_per_week": 10, "best_formats": "short_video,hook,series"},
    "YouTube Shorts": {"b2b": 0.45, "visual": 0.75, "short_video": 0.90, "long_form": 0.25, "email": 0.05, "max_posts_per_week": 6, "best_formats": "short_tutorial,demo,explainer"},
    "X": {"b2b": 0.70, "visual": 0.35, "short_video": 0.35, "long_form": 0.50, "email": 0.10, "max_posts_per_week": 12, "best_formats": "thread,news_reaction,quick_take"},
    "Facebook": {"b2b": 0.30, "visual": 0.55, "short_video": 0.45, "long_form": 0.35, "email": 0.15, "max_posts_per_week": 5, "best_formats": "community_post,event,story"},
    "Blog": {"b2b": 0.80, "visual": 0.20, "short_video": 0.05, "long_form": 0.98, "email": 0.40, "max_posts_per_week": 3, "best_formats": "blog_outline,seo_article,guide"},
    "Newsletter": {"b2b": 0.70, "visual": 0.25, "short_video": 0.05, "long_form": 0.80, "email": 0.98, "max_posts_per_week": 3, "best_formats": "newsletter_note,roundup,launch_note"},
}


def recommend_platforms(radar: pd.DataFrame, segments: pd.DataFrame) -> pd.DataFrame:
    """Recommend platforms for each topic using audience affinity and platform rules."""
    if radar.empty:
        return pd.DataFrame()
    affinity = _segment_affinity(segments)
    rows = []
    for topic in radar.itertuples(index=False):
        for platform, rules in PLATFORM_RULES.items():
            platform_fit = (
                affinity["b2b"] * rules["b2b"] * 0.28
                + affinity["visual"] * rules["visual"] * 0.20
                + affinity["short_video"] * rules["short_video"] * 0.18
                + affinity["long_form"] * rules["long_form"] * 0.18
                + affinity["email"] * rules["email"] * 0.08
                + float(topic.content_opportunity_score) * 0.08
            )
            score = max(0.0, min(1.0, platform_fit))
            rows.append({
                "topic_id": topic.topic_id,
                "topic": topic.topic,
                "platform": platform,
                "platform_fit_score": round(score, 4),
                "recommended_format": str(rules["best_formats"]).split(",")[0],
                "max_posts_per_week": int(rules["max_posts_per_week"]),
                "platform_reason": _platform_reason(platform, score),
            })
    return pd.DataFrame(rows).sort_values(["topic_id", "platform_fit_score"], ascending=[True, False]).reset_index(drop=True)


def top_platform_per_topic(platforms: pd.DataFrame) -> pd.DataFrame:
    if platforms.empty:
        return platforms
    return platforms.sort_values("platform_fit_score", ascending=False).groupby("topic_id", as_index=False).head(1).reset_index(drop=True)


def platform_summary(platforms: pd.DataFrame) -> dict[str, int | str | float]:
    if platforms.empty:
        return {"platform_recommendation_count": 0, "top_platform_overall": "none"}
    top = top_platform_per_topic(platforms)
    return {
        "platform_recommendation_count": int(len(platforms)),
        "scheduled_candidate_count": int(len(top)),
        "top_platform_overall": str(top["platform"].mode().iloc[0]),
        "mean_platform_fit_score": float(top["platform_fit_score"].mean()),
    }


def _segment_affinity(segments: pd.DataFrame) -> dict[str, float]:
    if segments.empty:
        return {"b2b": 0.5, "visual": 0.5, "short_video": 0.5, "long_form": 0.5, "email": 0.5}
    return {
        "b2b": float(segments["b2b_affinity"].mean()),
        "visual": float(segments["visual_content_affinity"].mean()),
        "short_video": float(segments["short_video_affinity"].mean()),
        "long_form": float(segments["long_form_affinity"].mean()),
        "email": float(segments["email_affinity"].mean()),
    }


def _platform_reason(platform: str, score: float) -> str:
    if score >= 0.70:
        return f"{platform} is a strong fit for this audience, topic, and format"
    if score >= 0.50:
        return f"{platform} is a testable fit with moderate expected engagement"
    return f"{platform} is lower priority; use only if campaign coverage is needed"
