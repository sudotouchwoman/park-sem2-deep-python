from collections import OrderedDict
from typing import Any, Hashable, Optional

from . import LOG_MANAGER


class LRUCache:
    __slots__ = ("cache", "capacity", "log")

    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.cache = OrderedDict()
        self.log = LOG_MANAGER.get_logger(
            __name__, file="cache.log", level="DEBUG"
        )
        self.log.info(msg=f"Created LRUCache with limit {capacity}")

    def __getitem__(self, key: Hashable) -> Optional[Any]:
        self.log.info(msg=f"Accessing key: {key}")
        if key not in self.cache:
            self.log.warning(msg="Key was not found in cache")
            return None
        self.log.debug(msg="Found key, moving to the end")
        self.cache.move_to_end(key)

        value = self.cache[key]
        self.log.debug(msg=f"Got value: {value}")
        return value

    def __setitem__(self, key: Hashable, value: Any) -> None:
        self.log.info(msg="Setting new key-value pair")
        self.log.debug(msg=f"[{key} -> {value}]")

        self.cache[key] = value
        self.cache.move_to_end(key)

        if len(self.cache) > self.capacity:
            self.log.warning(msg="Cache capacity limit reached")
            self.log.debug(msg="Dropping key-value pair")
            old_key, old_value = self.cache.popitem(last=False)
            self.log.debug(msg=f"[{old_key} -> {old_value}]")

    def __repr__(self) -> str:
        self.log.debug(msg="__repr__ called")
        return f"LRUCache (capacity {self.capacity}); cache=[ " + " ".join(
            (f"[{key}->{value}]" for key, value in self.cache.items()) + "]"
        )
