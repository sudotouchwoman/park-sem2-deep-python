from collections import deque
from typing import Any, Deque, Dict, Hashable, Optional


class LRUCache:
    limit: int
    keys2idx: Dict[Hashable, int]
    idx2keys: Dict[int, Hashable]
    cache: Deque[Any]

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.cache = deque(maxlen=limit)

    def _put_on_top(self, key: Hashable, value: Any) -> None:
        self.cache.appendleft(value)
        self.keys2idx[key] = 0
        self.idx2keys[0] = key

    def __getitem__(self, key: Hashable) -> Optional[Any]:
        if key not in self.keys2idx.keys():
            raise KeyError

        idx = self.keys2idx[key]
        value = self.cache[idx]
        self.cache.remove(value)

        for i in range(idx + 1):
            # after the node is put onto the top,
            # the indices of the preceding items
            # should be updated
            # (indices of the following nodes needn't
            # # updating as their indices basically remain unaltered)
            self.keys2idx[self.idx2keys[i]] += 1

        self._put_on_top(key, value)
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if len(self.cache) == self.limit and key not in self.keys2idx.keys():
            del self.keys2idx[key]

        for i, _ in enumerate(self.cache):
            self.keys2idx[self.idx2keys[i]] += 1

        self._put_on_top(key, value)
