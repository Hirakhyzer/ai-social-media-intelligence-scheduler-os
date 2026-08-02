"""Matplotlib figures for PostPilot OS outputs."""

from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def _save(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def plot_trend_opportunities(radar: pd.DataFrame, path: str | Path) -> None:
    top = radar.head(12).iloc[::-1]
    plt.figure(figsize=(9, 5))
    plt.barh(top["topic_id"], top["content_opportunity_score"])
    plt.xlabel("Opportunity score")
    plt.title("Top synthetic trend opportunities")
    _save(path)


def plot_platform_fit(platforms: pd.DataFrame, path: str | Path) -> None:
    top = platforms.groupby("platform")["platform_fit_score"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    plt.barh(top.index, top.values)
    plt.xlabel("Mean platform fit")
    plt.title("Platform fit scores")
    _save(path)


def plot_best_times(times: pd.DataFrame, path: str | Path) -> None:
    counts = times.groupby(["platform", "recommended_time_local"]).size().reset_index(name="count")
    labels = counts["platform"] + " " + counts["recommended_time_local"]
    plt.figure(figsize=(10, 5))
    plt.bar(labels, counts["count"])
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Scheduled items")
    plt.title("Recommended posting times")
    _save(path)


def plot_calendar_density(calendar: pd.DataFrame, path: str | Path) -> None:
    counts = calendar.groupby("recommended_date").size()
    plt.figure(figsize=(10, 5))
    plt.plot(counts.index, counts.values, marker="o")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Posts")
    plt.title("Content calendar density")
    _save(path)


def plot_brand_safety(guard: pd.DataFrame, path: str | Path) -> None:
    plt.figure(figsize=(8, 5))
    plt.hist(guard["brand_safety_risk_score"], bins=10)
    plt.xlabel("Brand safety risk")
    plt.ylabel("Drafts")
    plt.title("Brand safety risk distribution")
    _save(path)


def plot_engagement_forecast(analytics: pd.DataFrame, path: str | Path) -> None:
    means = analytics.groupby("platform")["simulated_engagement_rate"].mean().sort_values()
    plt.figure(figsize=(8, 5))
    plt.barh(means.index, means.values)
    plt.xlabel("Simulated engagement rate")
    plt.title("Synthetic engagement forecast")
    _save(path)
