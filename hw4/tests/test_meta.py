import pytest
from utils.meta import PrefixMeta, make_custom_metaclass

class SampleClass(metaclass=PrefixMeta):
    def __init__(self) -> None:
        pass
