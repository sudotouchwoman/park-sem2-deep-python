import pytest
from utils.meta import PrefixMeta, metaclass_factory


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


def test_PrefixMeta(faker, prefix):
    is_dunder = lambda x: x.startswith("__") and x.endswith("__")

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
