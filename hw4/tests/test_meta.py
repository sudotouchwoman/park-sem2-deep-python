"""
Unit tests for custom metaclass factory
Assertions are made on attribute access, their names and values
"""
import pytest

from utils.meta import (
    metaclass_factory,
    is_dunder_method,
    attribute_mapping_factory,
)


def test_faker(faker):
    assert isinstance(faker.name(), str)


def test_meta():
    # basic test for metaclass factory (type checks)
    # when called without argument, factory
    # creates metaclass which does practically nothing
    # (it does not modify attributes in any way)
    sample_metaclass = metaclass_factory()

    class SampleClass(metaclass=sample_metaclass):
        pass

    assert isinstance(sample_metaclass, type)
    assert isinstance(SampleClass, type)


def test_is_dunder_method():
    # helper function to detect attributes that are unlikely to
    # be user-specific, thus usually should not be modified
    # by metaclass
    dunder_attributes = ("__new__", "__init__", "__call__")
    arbitrary_attributes = ("__private", "logger", "x", "y__", "z_")

    assert all(map(is_dunder_method, dunder_attributes))
    assert all(map(lambda x: not is_dunder_method(x), arbitrary_attributes))


def test_mapping_factory(faker):
    identity_mapping = attribute_mapping_factory(
        lambda x: x, lambda y: y, skip_dunder=True
    )
    attr_name, attr_avlue = faker.name(), faker.email()
    assert attr_name, attr_avlue == identity_mapping(attr_name, attr_avlue)


@pytest.fixture
def prefix():
    return "custom_"


@pytest.fixture
def add_prefix():
    def _add_prefix(prefix):
        return attribute_mapping_factory(
            # add provided prefix to attribute name
            # do not modify the value and names of dunder
            # methods/attributes
            lambda a: prefix + a,
            lambda v: v,
            skip_dunder=True,
        )

    return _add_prefix


def test_PrefixMeta(faker, prefix, add_prefix):
    """
    Test the required PrefixMeta metaclass
    which adds `custom_` prefix to each non-dunder attribute
    """

    # create some dummy data:
    # class attributes and their names
    bases = ()
    name = "_".join(faker.name().split())
    attrs = {"".join(faker.name().split()): faker.email() for _ in range(100)}
    attrs.update({item: None for item in dir(faker)})

    sample_metaclass = metaclass_factory(mapping=add_prefix(prefix))
    SampleClass = sample_metaclass(name, bases, attrs)

    # check all the attributes of new class
    # if it is not magic (dunder),
    # it should start with specified prefix
    for attr in dir(SampleClass):
        assert isinstance(attr, str)
        if not is_dunder_method(attr):
            assert attr.startswith(prefix)
            *_, attr = attr.partition(prefix)
        assert attr in attrs.keys()


def test_attribute_setting(prefix, add_prefix):
    """
    Ensure that the attributes set in `__init__` or
    anywhere else at the scope of instance are mapped
    correctly
    """

    sample_metaclass = metaclass_factory(mapping=add_prefix(prefix))

    class SampleClass(metaclass=sample_metaclass):
        x = 5
        _z = "value"
        __y = "private"
        __some_dunder_attribute__ = "some value"

        def __init__(self) -> None:
            self.instance_attr = "instance value"

    # this test is more manual but checks all of the
    # possible caveats
    instance = SampleClass()
    assert hasattr(SampleClass, prefix + "_SampleClass__y")
    assert not hasattr(SampleClass, "_Sampleclass_y")

    assert getattr(SampleClass, "__some_dunder_attribute__") == "some value"
    assert getattr(instance, "__some_dunder_attribute__") == "some value"

    # test for instance-scope attributes
    # and `__setattr__`
    assert getattr(instance, prefix + "instance_attr") == "instance value"

    # new attribute should be also dynamically renamed
    instance.new_attribute = 5
    assert not hasattr(instance, "new_attribute")
    assert getattr(instance, prefix + "new_attribute") == 5

    instance.f = lambda: "hello from f"

    assert not hasattr(instance, "f")
    assert getattr(instance, prefix + "f")() == "hello from f"

    # and at last
    for attribute in (a for a in dir(instance) if not is_dunder_method(a)):
        assert isinstance(attribute, str)
        assert attribute.startswith(prefix)
