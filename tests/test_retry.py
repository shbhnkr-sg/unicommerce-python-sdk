from unicommerce._retry import compute_backoff


def test_backoff_attempt_zero():
    result = compute_backoff(0, base=0.5, cap=8.0)
    assert 0.5 <= result <= 0.5 * 1.25


def test_backoff_attempt_one():
    result = compute_backoff(1, base=0.5, cap=8.0)
    assert 1.0 <= result <= 1.0 * 1.25


def test_backoff_attempt_four_hits_cap():
    result = compute_backoff(4, base=0.5, cap=8.0)
    assert 8.0 <= result <= 8.0 * 1.25


def test_backoff_never_exceeds_cap_plus_jitter():
    for attempt in range(10):
        result = compute_backoff(attempt, base=0.5, cap=8.0)
        assert result <= 8.0 * 1.25


def test_backoff_custom_params():
    result = compute_backoff(2, base=1.0, cap=10.0)
    assert 4.0 <= result <= 4.0 * 1.25
