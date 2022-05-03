from utils import LRUCache


def test_cache():
    cache = LRUCache(limit=2)
    cache["k1"] = "val1"
    cache["k2"] = "val2"

    assert cache["k3"] is None
    assert cache["k2"] == "val2"
    assert cache["k1"] == "val1"

    cache["k3"] = "val3"

    assert cache["k3"] == "val3"
    assert cache["k2"] is None
    assert cache["k1"] == "val1"
