"""
Metaclass factory implementation
"""


from typing import Any, Callable, Dict, Protocol, Tuple


class AttributeMapper(Protocol):
    """
    Signature for functions to be used as argument
    in `metaclass_factory`

    This is a base class which merely performs identity mapping
    """

    @staticmethod
    def __call__(attr_name: str, attr_value: Any) -> Tuple[str, Any]:
        raise NotImplementedError


def is_dunder_method(attr_name):
    return attr_name.startswith("__") and attr_name.endswith("__")


def attribute_mapping_factory(
    name_transform: Callable, value_transform: Callable, skip_dunder=True
) -> AttributeMapper:
    """
    Simple factory to ease the creation of attribute mappers
    The output mapper can be passed as a `mapping` parameter
    to the `metaclass_factory`
    """

    def transform(attr_name: str, attr_value: Any) -> Tuple[str, Any]:
        if skip_dunder and is_dunder_method(attr_name):
            return attr_name, attr_value
        return name_transform(attr_name), value_transform(attr_value)

    return transform


def metaclass_factory(mapping: AttributeMapper = None):
    """
    Create new custom metaclass which performs provided
    mapping of class attributes

    Args:

    + `mapping`: function supporting `AttributeMapper` protocol
    which will be used to substitute the names and values
    of class/instance attributes by the metaclass

    Returns:

    + `Meta`, metaclass instance which would perform
    provided modification of arguments whenever class/instance
    is defined

    No error checks are performed during mapping, but in order
    to avoid possible misuse, one is encouraged to use the wrapper,
    `attribute_mapping_factory`, in order to embed functions into
    appropriate format

    By default, no changes are done to the attributes and their names
    """

    # the simplest (empty) mapping possible
    # as a default
    if mapping is None:

        def mapping(x, y):
            return x, y

    class Meta(type):
        def __new__(cls, name: str, bases: Any, attrs: Dict[str, Any]):
            custom_attrs = {
                key: value
                for key, value in map(mapping, attrs.keys(), attrs.values())
            }

            new_class = super().__new__(cls, name, bases, custom_attrs)

            def meta_setattr(obj, attr_name, value):
                attr_name, value = mapping(attr_name, value)
                obj.__dict__[attr_name] = value

            new_class.__setattr__ = meta_setattr
            return new_class

    return Meta


# Note, how
# this perticular metaclass
# can be created that simple
# using the factory!
def prefix_mapping(attr_name, attr_value):
    if is_dunder_method(attr_name):
        return attr_name, attr_value
    return f"custom_{attr_name}", attr_value


PrefixMeta = metaclass_factory(mapping=prefix_mapping)
