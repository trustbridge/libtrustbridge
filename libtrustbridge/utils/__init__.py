import random


def get_retry_time(attempt, base=8, max_retry=100):
    """exponential back off with jitter"""
    if attempt <= 1:
        return 0
    delay = min(base * 2 ** attempt, max_retry)
    jitter = random.uniform(0, delay / 2)
    return int(delay / 2 + jitter)
