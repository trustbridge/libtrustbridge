import random

import pytest

from libtrustbridge.utils import get_retry_time


@pytest.mark.parametrize('attempt,expected_delay', [
    (0, 0), (1, 0), (2, 25), (3, 51), (4, 102), (5, 204), (6, 409), (7, 798), (8, 798)
])
def test_get_retry_time__should_return_that_exponentially_increasing_delay_with_random_jitter(attempt, expected_delay):
    random.seed(300)
    assert get_retry_time(attempt, max_retry=1000) == expected_delay
