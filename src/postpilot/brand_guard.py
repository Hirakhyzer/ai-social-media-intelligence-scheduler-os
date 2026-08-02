"""Ethical marketing and brand-safety review gates."""

from __future__ import annotations

import re

import pandas as pd

BANNED_PATTERNS = {
    "guaranteed_outcome": r"\b(guaranteed|100%|instant riches|never fail)\b",
    "deceptive_growth": r"\b(fake followers|fake reviews|buy engagement|bot traffic)\b",
    "unsafe_claim": r"\b(cure|legal proof|certified investment advice)\b",
    "spam_language": r"\b(urgent!!!|click now!!!|limited secret loophole)\b",
}


def audit_brand_safety(drafts: pd.DataFrame, brand: pd.DataFrame | None = None) -> pd.DataFrame:
    """Audit each draft before scheduling.

    The output intentionally keeps a human approval step even for low-risk posts.
    """
    if drafts.empty:
        return pd.DataFrame()
    rows = []
    for draft in drafts.itertuples(index=False):
        text = f"{draft.hook} {draft.post_body} {draft.cta} {draft.hashtags}".lower()
        flags = []
        for name, pattern in BANNED_PATTERNS.items():
            if re.search(pattern, text, flags=re.IGNORECASE):
                flags.append(name)
        hashtag_count = str(draft.hashtags).count("#")
        if hashtag_count > 8:
            flags.append("excessive_hashtags")
        if "human before real posting" not in text:
            flags.append("missing_human_review_disclaimer")
        risk = min(1.0, 0.15 + 0.18 * len(flags) + (0.10 if hashtag_count > 5 else 0.0))
        approval_state = "blocked" if risk >= 0.72 else ("needs_review" if risk >= 0.34 else "human_review_required")
        rows.append({
            "draft_id": draft.draft_id,
            "platform": draft.platform,
            "brand_safety_risk_score": round(risk, 4),
            "approval_state": approval_state,
            "policy_flags": ",".join(flags) if flags else "none",
            "human_approval_required": True,
            "real_posting_boundary": "do_not_post_without_human_approval_and_platform_adapter_validation",
        })
    return pd.DataFrame(rows)


def brand_guard_summary(audit: pd.DataFrame) -> dict[str, int | float]:
    if audit.empty:
        return {"brand_audit_count": 0, "blocked_draft_count": 0}
    return {
        "brand_audit_count": int(len(audit)),
        "blocked_draft_count": int((audit["approval_state"] == "blocked").sum()),
        "needs_review_count": int((audit["approval_state"] == "needs_review").sum()),
        "mean_brand_safety_risk": float(audit["brand_safety_risk_score"].mean()),
    }
