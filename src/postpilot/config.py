"""Configuration and filesystem helpers for PostPilot OS."""

from __future__ import annotations

import random
from pathlib import Path

import numpy as np


def set_seed(seed: int) -> None:
    """Set deterministic seeds for reproducible synthetic marketing runs."""
    random.seed(seed)
    np.random.seed(seed)


def ensure_output_dirs(output_dir: str | Path) -> dict[str, Path]:
    """Create standard output folders and return their paths."""
    root = Path(output_dir)
    paths = {
        "root": root,
        "results": root / "results",
        "reports": root / "reports",
        "figures": root / "figures",
        "audit": root / "audit",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths
