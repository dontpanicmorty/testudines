import random

import pytest

from solution import backoff_delays


def test_no_jitter_doubles_then_caps():
    assert backoff_delays(6) == [0.5, 1.0, 2.0, 4.0, 8.0, 8.0]


def test_custom_base_and_cap():
    assert backoff_delays(4, base=1, cap=3) == [1, 2, 3, 3]


def test_zero_or_negative_retries():
    assert backoff_delays(0) == []
    assert backoff_delays(-2) == []


def test_jitter_within_ceiling_and_reproducible():
    ceilings = backoff_delays(6)
    a = backoff_delays(6, rng=random.Random(7))
    b = backoff_delays(6, rng=random.Random(7))
    assert a == b, "same seed must give same delays"
    assert len(a) == 6
    assert all(0 <= d <= c for d, c in zip(a, ceilings)), f"{a} vs ceilings {ceilings}"
    assert a != ceilings


def test_jitter_matches_full_jitter_formula():
    rng = random.Random(3)
    expected_rng = random.Random(3)
    expected = [expected_rng.uniform(0, c) for c in [0.5, 1.0, 2.0]]
    assert backoff_delays(3, rng=rng) == pytest.approx(expected)


def test_negative_inputs_rejected():
    with pytest.raises(ValueError):
        backoff_delays(3, base=-1)
    with pytest.raises(ValueError):
        backoff_delays(3, cap=-1)
