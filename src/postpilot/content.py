"""Content draft generation for human-reviewed social scheduling."""

from __future__ import annotations

import pandas as pd


def generate_content_drafts(schedule_times: pd.DataFrame, campaigns: pd.DataFrame) -> pd.DataFrame:
    """Generate deterministic draft copy, hooks, CTA, and asset briefs."""
    if schedule_times.empty:
        return pd.DataFrame()
    campaign_cycle = campaigns.to_dict("records") if not campaigns.empty else []
    rows = []
    for idx, item in enumerate(schedule_times.itertuples(index=False)):
        campaign = campaign_cycle[idx % len(campaign_cycle)] if campaign_cycle else {"campaign_id": "CMP-00", "campaign_name": "general content", "goal": "education", "brand_tone": "credible"}
        hook = _hook(str(item.platform), str(item.topic))
        body = _body(str(item.platform), str(item.topic), str(campaign.get("brand_tone", "credible")))
        rows.append({
            "draft_id": f"DRAFT-{idx+1:04d}",
            "topic_id": item.topic_id,
            "campaign_id": campaign.get("campaign_id", "CMP-00"),
            "campaign_name": campaign.get("campaign_name", "general content"),
            "platform": item.platform,
            "recommended_format": item.recommended_format,
            "post_title": f"{item.topic} — {item.recommended_format}",
            "hook": hook,
            "post_body": body,
            "cta": _cta(str(campaign.get("goal", "education"))),
            "asset_needed": _asset(item.recommended_format, item.platform),
            "hashtags": _hashtags(item.topic),
            "draft_status": "drafted_for_human_review",
        })
    return pd.DataFrame(rows)


def content_summary(drafts: pd.DataFrame) -> dict[str, int | str]:
    if drafts.empty:
        return {"content_draft_count": 0, "primary_content_platform": "none"}
    return {
        "content_draft_count": int(len(drafts)),
        "primary_content_platform": str(drafts["platform"].mode().iloc[0]),
        "human_review_queue_count": int((drafts["draft_status"] == "drafted_for_human_review").sum()),
    }


def _hook(platform: str, topic: str) -> str:
    if platform in {"LinkedIn", "Blog", "Newsletter"}:
        return f"Most teams miss the planning layer behind {topic}."
    if platform in {"TikTok", "YouTube Shorts", "Instagram"}:
        return f"Here is the quick version of {topic}."
    return f"A practical note on {topic}."


def _body(platform: str, topic: str, tone: str) -> str:
    return (
        f"A {tone} post about {topic}. It explains the problem, gives one practical framework, "
        "and asks the audience to review the checklist before applying it. This draft is synthetic "
        "and must be approved by a human before real posting."
    )


def _cta(goal: str) -> str:
    return {
        "awareness": "Save this checklist for your next planning session.",
        "education": "Comment with the part you want expanded.",
        "conversion": "Review the demo checklist before choosing a tool.",
        "community": "Share one lesson from your own workflow.",
        "retention": "Send this to your team before the next campaign review.",
        "launch": "Join the waitlist after reading the limitations.",
    }.get(goal, "Review this with your team before using it.")


def _asset(fmt: str, platform: str) -> str:
    if "carousel" in fmt:
        return "5-slide carousel outline"
    if "video" in fmt or platform in {"TikTok", "YouTube Shorts"}:
        return "short video script and thumbnail concept"
    if "blog" in fmt:
        return "long-form article outline"
    return "single post graphic optional"


def _hashtags(topic: str) -> str:
    words = [w for w in topic.lower().replace("/", " ").split() if len(w) > 3][:4]
    return ",".join(f"#{w}" for w in words)
