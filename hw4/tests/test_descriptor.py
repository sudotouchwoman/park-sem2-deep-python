"""
Unit-tests for type descriptors implementation

Checks are performed on required basic data types (str, int)
As well as on arbitrary set of classes

Note: under the hood, `isinstance` check is done,
thus `typed_descriptor` does not imply strict typing
"""


import pytest

from utils.descriptor import (
    Integer,
    PositiveInteger,
    String,
    typed_descriptor,
    type_hint,
)


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
def positive_int():
    return 42


@pytest.fixture
def negative_int():
    return -42


def test_positive(positive_int, negative_int):
    class SampleContainer:
        pos = PositiveInteger(positive_int)

    data = SampleContainer()
    assert type(data.pos) == int
    assert data.pos == positive_int

    with pytest.raises(ValueError) as exc_info:
        data.pos = negative_int
    assert isinstance(exc_info.value, ValueError)

    with pytest.raises(ValueError) as exc_info:
        # attempt to pass invalid initial value into descriptor
        class SampleContainer:
            pos = PositiveInteger(negative_int)

    assert isinstance(exc_info.value, ValueError)


def test_bad_assignment(positive_int, negative_int):
    # check that descriptors manage to conserve their
    # value in case of inappropriate assignment
    class SampleContainer:
        positive = PositiveInteger(positive_int)
        ordinary_integer = Integer(-1)
        ordinary_string = String("special string")

    data = SampleContainer()

    with pytest.raises(TypeError) as exc_info:
        data.positive = "this is not an integer"
    assert isinstance(exc_info.value, TypeError)
    assert data.positive == positive_int

    with pytest.raises(ValueError) as exc_info:
        data.positive = negative_int
    assert isinstance(exc_info.value, ValueError)
    assert data.positive == positive_int

    with pytest.raises(TypeError) as exc_info:
        data.ordinary_integer = "this is not an integer"
    assert isinstance(exc_info.value, TypeError)
    assert data.ordinary_integer == -1

    with pytest.raises(TypeError) as exc_info:
        data.ordinary_string = 3.1415
    assert isinstance(exc_info.value, TypeError)
    assert data.ordinary_string == "special string"


def test_assignment():
    # check that the descriptors' values can change
    # if new valid values are given
    class SampleContainer:
        positive = PositiveInteger(10)
        oridinary_integer = Integer(-50)
        ordinary_string = String("a")

    data = SampleContainer()

    assert data.positive == 10
    assert data.oridinary_integer == -50
    assert data.ordinary_string == "a"

    data.positive = 2
    data.oridinary_integer = 777
    data.ordinary_string = "b"

    assert data.positive == 2
    assert data.oridinary_integer == 777
    assert data.ordinary_string == "b"
