from postpilot.synthetic import SyntheticPostPilotConfig, generate_synthetic_postpilot_data


def test_synthetic_shapes():
    data = generate_synthetic_postpilot_data(SyntheticPostPilotConfig(topics=10, segments=3, campaigns=2, seed=7))
    assert len(data["trends"]) == 10
    assert len(data["segments"]) == 3
    assert len(data["campaigns"]) == 2
    assert data["trends"]["synthetic_origin"].all()
