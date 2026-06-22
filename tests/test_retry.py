from unicommerce._retry import compute_backoff


def test_backoff_attempt_zero():
    result = compute_backoff(0, base=0.5, cap=8.0)
    assert 0.5 <= result <= 0.625


def test_backoff_scales_exponentially():
    result = compute_backoff(1, base=0.5, cap=8.0)
    assert 1.0 <= result <= 1.25


def test_backoff_caps_at_max():
    result = compute_backoff(10, base=0.5, cap=8.0)
    assert 8.0 <= result <= 10.0
