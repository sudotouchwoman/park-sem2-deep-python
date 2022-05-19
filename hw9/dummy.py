import sys

from utils import LOG_MANAGER
from utils.LRU import LRUCache


def main():
    try:
        if sys.argv[1] == "-s":
            LOG_MANAGER.stream_logs()
    except IndexError:
        pass

    cache = LRUCache(3)
    # fill the cache with some values
    cache["string-key"] = "string-value"
    cache[5] = -10

    # try to access key which is not present
    _ = cache["non-existent-key"]

    # cast to str to check the contents
    _ = str(cache)

    # any hashable structure can be used to store things
    cache[(-1, 8)] = [0, "can", "store", "lists"]

    # accessing/updating key makes them MRU
    _ = cache["string-key"]
    _ = str(cache)

    cache[(-1, 8)][0] = "also"
    _ = str(cache)

    cache["string-key"] = "another-string"
    _ = str(cache)

    # adding values exceeding capacity limit
    # would drop LRU items
    cache[2 + 2] = 5000
    cache["entries"] = "are kicked from the dict"

    _ = str(cache)

    cache[("bc", "total num")] = f"of items is {cache.capacity}"

    _ = cache["entries"]

    _ = str(cache)


if __name__ == "__main__":
    main()
