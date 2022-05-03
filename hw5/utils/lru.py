from typing import Any, Dict, Hashable, Optional


class LRUCache:
    def __init__(self, limit: int) -> None:
        self.limit: int = limit
        self.timestamp = 0
        self.cache: Dict[Hashable, Any] = {}
        self.lru: Dict[Hashable, int] = {}

    def __getitem__(self, key: Hashable) -> Optional[Any]:
        if key in self.cache:
            self.lru[key] = self.timestamp
            self.timestamp += 1
            return self.cache[key]
        return None

    def __setitem__(self, key: Hashable, value: Any) -> None:
        if len(self.cache) >= self.limit:
            oldest_key = min(self.lru.keys(), key=lambda k: self.lru[k])
            self.cache.pop(oldest_key)
            self.lru.pop(oldest_key)
        self.cache[key] = value
        self.lru[key] = self.timestamp
        self.timestamp += 1
