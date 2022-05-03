from typing import Tuple, Union

import pytest

from utils import LRUCache


@pytest.fixture
def invalid_limits() -> Tuple[Union[str, int, float]]:
    return "must be positive", -1, 0, 3.1415


def test_cache_creation(invalid_limits: Tuple[Union[str, int, float]]):
    for limit in invalid_limits:
        with pytest.raises(ValueError) as exc_info:
            LRUCache(limit=limit)
        assert isinstance(exc_info.value, ValueError)


def test_cache():
    # simple test from the task description
    cache = LRUCache(limit=2)
    cache["k1"] = "val1"
    cache["k2"] = "val2"

    assert cache["k3"] is None
    assert cache["k2"] == "val2"
    assert cache["k1"] == "val1"

    # when extra value is set to cache,
    # the LRU item ("k2" in this example) is kicked out
    cache["k3"] = "val3"

    assert cache["k3"] == "val3"
    assert cache["k2"] is None
    assert cache["k1"] == "val1"
