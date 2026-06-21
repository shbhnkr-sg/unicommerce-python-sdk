import random


def compute_backoff(attempt: int, base: float = 0.5, cap: float = 8.0) -> float:
    delay = min(cap, base * (2 ** attempt))
    jitter = random.uniform(0, delay * 0.25)
    return delay + jitter
