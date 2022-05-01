from copy import deepcopy
from functools import reduce
from typing import List, Tuple, Union

SupportsList = Union[List, "MyShinyList"]

__all__ = ["MyShinyList"]


class MyShinyList(list):
    @staticmethod
    def _cumsum(list_instance: SupportsList) -> int:
        return reduce(lambda x, y: x + y, list_instance, 0)

    def _zero_pad_sequence(self, other: SupportsList) -> Tuple[list, list]:
        copy_self = deepcopy(self)
        copy_other = deepcopy(other)

        length_diff = len(self) - len(other)
        padding = (0 for _ in range(abs(length_diff)))

        if length_diff < 0:
            copy_self.extend(padding)
        if length_diff > 0:
            copy_other.extend(padding)

        return copy_self, copy_other

    def __add__(self, other: SupportsList) -> "MyShinyList":
        copy_self, copy_other = self._zero_pad_sequence(other)
        return MyShinyList((x + y for x, y in zip(copy_self, copy_other)))

    def __sub__(self, other: SupportsList) -> "MyShinyList":
        copy_self, copy_other = MyShinyList._zero_pad_sequence(self, other)
        return MyShinyList((x - y for x, y in zip(copy_self, copy_other)))

    def __radd__(self, other: SupportsList) -> "MyShinyList":
        return self.__add__(other)

    def __rsub__(self, other: SupportsList) -> "MyShinyList":
        copy_self, copy_other = MyShinyList._zero_pad_sequence(self, other)
        return MyShinyList((x - y for x, y in zip(copy_other, copy_self)))

    def __str__(self) -> str:
        return super().__str__() + f" (cumsum: {self._cumsum(self)})"

    def __le__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) <= 0

    def __lt__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) < 0

    def __ge__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) >= 0

    def __gt__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) > 0

    def __eq__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) == 0

    def __ne__(self, other: SupportsList) -> bool:
        return self._cumsum(self) - self._cumsum(other) != 0
