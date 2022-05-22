import sys
import cProfile
import pstats

from lru import LRUCache
from utils import tag_factory, slotted_tag_factory


CACHE_LIMIT = 30
NUM_ENTRIES = 5_000


def cache_stress_test(num_entries: int, cache_capacity: int) -> None:
    cache = LRUCache(cache_capacity)

    key = "sussy-tag"
    try:
        value = (
            slotted_tag_factory(key)
            if sys.argv[1] == "-s"
            else tag_factory(key)
        )
    except IndexError:
        value = tag_factory(key)

    keys = (
        f"{key}-{entry}"
        for entry in range(cache_capacity * num_entries)
    )
    values = (
        value
        for _ in range(cache_capacity * num_entries)
    )

    def cache_lookup(key, value):
        cache[key]
        cache[key] = value

    tuple(map(cache_lookup, keys, values))


if __name__ == "__main__":
    pr = cProfile.Profile()
    pr.enable()

    cache_stress_test(NUM_ENTRIES, CACHE_LIMIT)

    pr.disable()

    ps = pstats.Stats(pr, stream=sys.stdout).sort_stats().print_stats()
