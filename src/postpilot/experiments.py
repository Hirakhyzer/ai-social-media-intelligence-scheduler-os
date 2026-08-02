"""A/B test simulation for content and schedule variants."""

from __future__ import annotations

import numpy as np
import pandas as pd


def simulate_ab_tests(calendar: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """Create synthetic A/B test records for top calendar items."""
    if calendar.empty:
        return pd.DataFrame()
    rng = np.random.default_rng(seed + 17)
    rows = []
    for idx, item in enumerate(calendar.head(12).itertuples(index=False)):
        baseline = float(rng.uniform(0.025, 0.075))
        variant = max(0.001, baseline + float(rng.normal(0.008, 0.012)))
        lift = (variant - baseline) / baseline
        rows.append({
            "experiment_id": f"EXP-{idx+1:03d}",
            "draft_id": item.draft_id,
            "platform": item.platform,
            "test_variable": rng.choice(["hook", "posting_time", "cta", "format"]),
            "control_engagement_rate": round(baseline, 5),
            "variant_engagement_rate": round(variant, 5),
            "relative_lift": round(lift, 4),
            "confidence_proxy": round(float(np.clip(0.50 + abs(lift) * 0.9, 0.50, 0.95)), 4),
            "decision": "promote_variant" if lift > 0.08 else "keep_testing",
        })
    return pd.DataFrame(rows)


def experiments_summary(experiments: pd.DataFrame) -> dict[str, int | float]:
    if experiments.empty:
        return {"experiment_count": 0, "promoted_variant_count": 0}
    return {
        "experiment_count": int(len(experiments)),
        "promoted_variant_count": int((experiments["decision"] == "promote_variant").sum()),
        "mean_relative_lift": float(experiments["relative_lift"].mean()),
    }
