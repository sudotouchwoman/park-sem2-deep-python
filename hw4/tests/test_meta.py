'''
Unit tests for custom metaclass factory
Assertions are made on attribute access, their names and values
'''
from itertools import chain

import pytest

from utils.meta import metaclass_factory


def test_faker(faker):
    assert isinstance(faker.name(), str)


def test_meta():
    sample_metaclass = metaclass_factory()

    class SampleClass(metaclass=sample_metaclass):
        pass

    assert isinstance(sample_metaclass, type)
    assert isinstance(SampleClass, type)


@pytest.fixture
def prefix():
    return "custom_"


@pytest.fixture
def is_dunder():
    return lambda x: x.startswith("__") and x.endswith("__")


def test_PrefixMeta(faker, prefix, is_dunder):
    bases = ()
    name = "_".join(faker.name().split())
    attrs = {"".join(faker.name().split()): faker.email() for _ in range(100)}
    attrs.update({item: None for item in dir(faker)})

    sample_metaclass = metaclass_factory(transform=lambda a: prefix + a)
    SampleClass = sample_metaclass(name, bases, attrs)

    for attr in dir(SampleClass):
        assert isinstance(attr, str)
        if not is_dunder(attr):
            assert attr.startswith(prefix)
            *_, attr = attr.partition(prefix)
        assert attr in attrs.keys()


def test_attribute_access(prefix, is_dunder):
    transform = lambda a: prefix + a
    sample_metaclass = metaclass_factory(transform=transform)

    class SampleClass:
        x = 0
        y = 10
        __private = "private attribute"
        _protected = "protected attribute"

        def __init__(self) -> None:
            pass

        def some_method(self):
            return "some_value"

    original_attributes = [attr for attr in dir(SampleClass) if not is_dunder(attr)]
    magic_attributes = [attr for attr in dir(SampleClass) if is_dunder(attr)]

    class SampleClass(metaclass=sample_metaclass):
        x = 0
        y = 10
        __private = "private attribute"
        _protected = "protected attribute"

        def __init__(self) -> None:
            pass

        def some_method(self):
            return "expected_value"

    instance = SampleClass()

    for attr in chain(magic_attributes, map(transform, original_attributes)):
        assert hasattr(SampleClass, attr)
        assert hasattr(instance, attr)

    for attr in chain(original_attributes, map(transform, magic_attributes)):
        with pytest.raises(AttributeError) as exc_info:
            getattr(instance, attr)
        assert isinstance(exc_info.value, AttributeError)

    with pytest.raises(AttributeError) as exc_info:
        instance.some_method()
    assert isinstance(exc_info.value, AttributeError)

    bound_method = getattr(instance, transform("some_method"))
    assert bound_method() == "expected_value"
