from postpilot.brand_guard import audit_brand_safety
from postpilot.calendar import build_content_calendar
from postpilot.content import generate_content_drafts
from postpilot.platform import recommend_platforms, top_platform_per_topic
from postpilot.radar import score_trend_opportunities
from postpilot.scheduler import build_schedule_queue
from postpilot.synthetic import SyntheticPostPilotConfig, generate_synthetic_postpilot_data
from postpilot.timing import recommend_posting_times


def test_pipeline_modules_create_queue():
    data = generate_synthetic_postpilot_data(SyntheticPostPilotConfig(topics=8, segments=3, campaigns=2, seed=11))
    radar = score_trend_opportunities(data["trends"], data["segments"])
    platforms = recommend_platforms(radar, data["segments"])
    top = top_platform_per_topic(platforms)
    times = recommend_posting_times(top, data["performance_priors"])
    drafts = generate_content_drafts(times, data["campaigns"])
    guard = audit_brand_safety(drafts, data["brand"])
    calendar = build_content_calendar(drafts, times, guard)
    queue = build_schedule_queue(calendar)
    assert len(top) == len(radar)
    assert len(queue) == len(calendar)
    assert queue["real_adapter_enabled"].sum() == 0
    assert calendar["human_approval_required"].all()
