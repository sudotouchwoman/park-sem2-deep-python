"""
Module contains typed descriptor templates and also several
descriptors for common types: Integers, Positive integers and Strings

One can inherit from `Descriptor` in order to perofrm more
specific and complicated checks on values
"""


def type_hint(expected_type):
    def hint(value):
        if isinstance(value, expected_type): return
        raise TypeError(f"Invalid type: expected {expected_type}, got {type(value)}")

    return hint


def typed_descriptor(expected_type: type):
    """
    Create typed descriptor template for a given type

    Args:

    + `expected_type`: class to ensure the instances of
    """
    if type(expected_type) is not type:
        raise TypeError(f"Expected a class, got {type(expected_type)}")

    # first empty (self) argument is required to bind as a method
    # original version of this function is left in the outer score
    # as a quick helper
    def make_type_hint(expected_type):
        def hint(_, value):
            if isinstance(value, expected_type): return
            raise TypeError(f"Invalid type: expected {expected_type}, got {type(value)}")

        return hint

    class Descriptor:
        """
        Descriptor class is a thin wrapper
        over the original value, ensuring the type inside __set__/__init__ call

        Note that for more complicated descriptors,
        one should also override the constructor and validate the inputs
        """
        __value: expected_type
        __type_hint = make_type_hint(expected_type)

        def __init__(self, default_value=expected_type()) -> None:
            self.__type_hint(default_value)
            self.__value = default_value

        def __get__(self, obj, type=None):
            return self.__value

        def __set__(self, obj, newvalue):
            self.__type_hint(newvalue)
            self.__value = newvalue

    return Descriptor


class String(typed_descriptor(str)):
    """
    String descriptor
    """


class Integer(typed_descriptor(int)):
    """
    Integer descriptor
    """


class PositiveInteger(Integer):
    """
    Positive integer descriptor
    """
    @staticmethod
    def __value_hint(newvalue):
        if newvalue >= 0: return
        raise ValueError(f"Integer provided must be positive, got {newvalue}")


    # note the overriden __init__ and __call__ methods
    def __set__(self, obj, newvalue):
        super().__set__(obj, newvalue)
        PositiveInteger.__value_hint(newvalue)


    def __init__(self, default_value=0) -> None:
        super().__init__(default_value)
        PositiveInteger.__value_hint(default_value)
