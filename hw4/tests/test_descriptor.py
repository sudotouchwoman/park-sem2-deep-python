"""
Unit-tests for type descriptors implementation

Checks are performed on required basic data types (str, int)
As well as on arbitrary set of classes

Note: under the hood, `isinstance` check is done,
thus `typed_descriptor` does not imply strict typing
"""


import pytest

from utils.descriptor import Integer, PositiveInteger, String, typed_descriptor, type_hint


@pytest.fixture
def classes():
    return int, str, list, tuple

@pytest.fixture
def another_class():
    return set


def test_hint(classes, another_class):
    for cls in classes:
        hint = type_hint(cls)
        # no exception should occur
        instance = cls()
        another_instance = another_class()
        hint(instance)
        # hint should raise when called with instance
        # of another class
        with pytest.raises(TypeError) as exc_info:
            hint(another_instance)
        assert isinstance(exc_info.value, TypeError)


def test_default_values():
    class SampleContainer:
        integer = Integer()
        positive = PositiveInteger()
        string = String()


    data = SampleContainer()
    assert type(data.integer) is int
    assert type(data.positive) is int
    assert type(data.string) is str

    assert data.integer == int()
    assert data.positive == int()
    assert data.string == str()


def test_typed_property(classes, another_class):
    for cls in classes:
        cls_descriptor = typed_descriptor(cls)
        class SampleContainer:
            data = cls_descriptor()

        container = SampleContainer()
        assert type(container.data) is cls
        container.data = cls()

        with pytest.raises(TypeError) as exc_info:
            invalid_class_instance = another_class()
            container.data = invalid_class_instance
        assert isinstance(exc_info.value, TypeError) 


@pytest.fixture
def positive_ok():
    return 42


@pytest.fixture
def positive_invalid():
    return -42


def test_positive(positive_ok, positive_invalid):
    class SampleContainer:
        pos = PositiveInteger(positive_ok)

    data = SampleContainer()
    assert type(data.pos) == int    
    assert data.pos == positive_ok

    with pytest.raises(ValueError) as exc_info:
        data.pos = positive_invalid
    assert isinstance(exc_info.value, ValueError)

    with pytest.raises(ValueError) as exc_info:
        # attempt to pass invalid initial value into descriptor
        class SampleContainer:
            pos = PositiveInteger(positive_invalid)
    assert isinstance(exc_info.value, ValueError)
    
