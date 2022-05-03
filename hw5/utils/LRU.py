# from collections import deque
# from typing import Any, Deque, Dict, Hashable, Optional, Tuple


# class LRUCache:
#     limit: int
#     key2idx: Dict[Hashable, int]
#     idx2key: Dict[int, Hashable]
#     cache: Deque[Tuple[int, Any]]

#     def __init__(self, limit: int) -> None:
#         self.limit = limit
#         self.cache = deque(maxlen=limit)

#         self.key2idx: Dict[Hashable, int] = {}
#         self.idx2key: Dict[int, Hashable] = {}

#     def _put_on_top(self, key: Hashable, value: Any) -> None:
#         self.cache.appendleft((key, value))
#         self.key2idx[key] = 0
#         self.idx2key[0] = key

#     def __getitem__(self, key: Hashable) -> Optional[Any]:
#         if key not in self.key2idx.keys():
#             return None

#         idx = self.key2idx[key]
#         _, value = self.cache[idx]
#         self.cache.remove((key, value))

#         for i in range(idx):
#             # after the node is put onto the top,
#             # the indices of the preceding items
#             # should be updated
#             # (indices of the following nodes needn't
#             # # updating as their indices basically remain unaltered)
#             self.key2idx[self.idx2key[i]] += 1

#         self._put_on_top(key, value)
#         return value

#     def __setitem__(self, key: Hashable, value: Any) -> None:
#         if len(self.cache) == self.limit and key not in self.key2idx.keys():
#             last_key = self.cache[-1][0]
#             del self.key2idx[last_key]

#         for i, _ in enumerate(self.cache):
#             self.key2idx[self.idx2key[i]] += 1

#         self._put_on_top(key, value)
