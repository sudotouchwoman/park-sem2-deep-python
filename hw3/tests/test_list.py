from typing import Callable, Iterable, List

import pytest
from faker import Faker

from utils import MyShinyList

SEQUENCE_LENGTH = 10


@pytest.fixture
def sample_data(faker: Faker) -> List[int]:
    return [faker.random_int() for _ in range(SEQUENCE_LENGTH)]


@pytest.fixture
def expected_cumsum(sample_data) -> int:
    return sum(sample_data)


def test_repr(sample_data: List[int], expected_cumsum: str):
    a = MyShinyList(sample_data)
    assert str(a) == str(sample_data) + f" (cumsum: {expected_cumsum})"

    b = MyShinyList()
    assert str(b) == "[] (cumsum: 0)"


@pytest.fixture
def bigger(sample_data) -> List[int]:
    return [x + 1 for x in sample_data]


@pytest.fixture
def smaller(sample_data) -> List[int]:
    return [x - 1 for x in sample_data]


def test_tricky_equilibrium():
    # test that custom lists with different items
    # but same sum are equal
    a = [-1, 1, -1, 1]
    b = [-2, 2, -2, 2, -2, 2]

    a_shiny = MyShinyList(a)
    b_shiny = MyShinyList(b)

    assert a == b_shiny
    assert b_shiny == a
    assert a_shiny == b
    assert b == a_shiny
    assert a_shiny == b_shiny


def test_spaceship(smaller: List[int], bigger: List[int]):
    # test name refers to the spaceship operator <=>
    # from C++ 20, which is basically a 3-in-1 comparator
    small_and_shiny = MyShinyList(smaller)
    big_and_shiny = MyShinyList(bigger)

    assert smaller == small_and_shiny
    assert small_and_shiny == smaller
    assert small_and_shiny == small_and_shiny
    assert small_and_shiny < bigger
    assert bigger > small_and_shiny
    assert small_and_shiny < big_and_shiny
    assert big_and_shiny > small_and_shiny

    assert small_and_shiny <= bigger
    assert bigger >= small_and_shiny
    assert small_and_shiny <= big_and_shiny
    assert big_and_shiny >= small_and_shiny

    empty = []
    empty_and_shiny = MyShinyList()

    assert empty == empty_and_shiny


@pytest.fixture
def assert_elementwise_equal() -> Callable:
    def comparator(x: Iterable, y: Iterable):
        assert len(x) == len(y)
        for xx, yy in zip(x, y):
            assert xx == yy

    return comparator


<<<<<<< Updated upstream
def test_basic_math(assert_elementwise_equal: Callable):
    # the lists are of different length
    a = [1, -1, 8, 5, -4]
    b = [4, 2, -5, 7]
=======
@pytest.fixture
def a() -> List[int]:
    return [1, -1, 8, 5, -4]


@pytest.fixture
def b() -> List[int]:
    return [4, 2, -5, 7]


def test_basic_math(assert_elementwise_equal: Callable, a, b):
    # the lists are of different length
>>>>>>> Stashed changes

    # copies are used to test the identity
    # i.e., the invariance of the instance
    # to operations like + or -
    a_copy = a
    b_copy = b

    a_sum = sum(a)  # 9
    b_sum = sum(b)  # 8

    a_shiny, b_shiny = map(MyShinyList, (a, b))
    a_shiny_copy, b_shiny_copy = a_shiny, b_shiny

    assert a == a_shiny
    assert b == b_shiny
    assert_elementwise_equal(a, a_shiny)
    assert_elementwise_equal(b, b_shiny)

    # check all possible
    # configurations of addition and subtraction
    c = a + b_shiny
    assert isinstance(c, MyShinyList)
    assert b_shiny is b_shiny_copy
    assert a is a_copy
    assert_elementwise_equal(b_shiny, b_shiny_copy)
    assert_elementwise_equal(a, a_copy)
    assert sum(c) == a_sum + b_sum

    c = a_shiny + b
    assert isinstance(c, MyShinyList)
    assert a_shiny is a_shiny_copy
    assert b is b_copy
    assert_elementwise_equal(a_shiny, a_shiny_copy)
    assert_elementwise_equal(b, b_copy)
    assert sum(c) == a_sum + b_sum

    c = a_shiny + b_shiny
    assert isinstance(c, MyShinyList)
    assert a_shiny is a_shiny_copy and b_shiny is b_shiny_copy
    assert a is a_copy and b is b_copy
    assert_elementwise_equal(a_shiny, a_shiny_copy)
    assert_elementwise_equal(b_shiny, b_shiny_copy)
    assert_elementwise_equal(a, a_copy)
    assert_elementwise_equal(b, b_copy)
    assert sum(c) == a_sum + b_sum

    # test subtraction (the order matters now!)
    d = a - b_shiny
    assert isinstance(d, MyShinyList)
    assert b_shiny is b_shiny_copy
    assert a is a_copy
    assert_elementwise_equal(b_shiny, b_shiny_copy)
    assert_elementwise_equal(a, a_copy)
    assert sum(d) == a_sum - b_sum

    d = a_shiny - b
    assert isinstance(d, MyShinyList)
    assert a_shiny is a_shiny_copy
    assert b is b_copy
    assert_elementwise_equal(a_shiny, a_shiny_copy)
    assert_elementwise_equal(b, b_copy)
    assert sum(d) == a_sum - b_sum

    d = a_shiny - b_shiny
    assert isinstance(d, MyShinyList)
    assert a_shiny is a_shiny_copy and b_shiny is b_shiny_copy
    assert a is a_copy and b is b_copy
    assert_elementwise_equal(a_shiny, a_shiny_copy)
    assert_elementwise_equal(b_shiny, b_shiny_copy)
    assert_elementwise_equal(a, a_copy)
    assert_elementwise_equal(b, b_copy)
    assert sum(d) == a_sum - b_sum


def test_inner_values(a, b, assert_elementwise_equal):
    a_shiny, b_shiny = map(MyShinyList, (a, b))

    def elementwise_add(x: List[int], y: List[int]) -> List[int]:
        x, y = x.copy(), y.copy()
        diff = len(y) - len(x)
        if diff > 0:
            x.extend((0 for _ in range(diff)))
        elif diff < 0:
            y.extend((0 for _ in range(abs(diff))))
        return [xx + yy for xx, yy in zip(x, y)]

    def elementwise_sub(x: List[int], y: List[int]) -> List[int]:
        x, y = x.copy(), y.copy()
        diff = len(y) - len(x)
        if diff > 0:
            x.extend((0 for _ in range(diff)))
        elif diff < 0:
            y.extend((0 for _ in range(abs(diff))))
        return [xx - yy for xx, yy in zip(x, y)]

    assert_elementwise_equal(
        a_shiny + b_shiny, elementwise_add(a_shiny, b_shiny)
    )
    assert_elementwise_equal(a + b_shiny, elementwise_add(a, b_shiny))
    assert_elementwise_equal(b_shiny + a, elementwise_add(b_shiny, a))
    assert_elementwise_equal(b + a_shiny, elementwise_add(b, a_shiny))
    assert_elementwise_equal(a_shiny + b, elementwise_add(a_shiny, b))

    assert_elementwise_equal(
        a_shiny - b_shiny, elementwise_sub(a_shiny, b_shiny)
    )
    assert_elementwise_equal(a - b_shiny, elementwise_sub(a, b_shiny))
    assert_elementwise_equal(b_shiny - a, elementwise_sub(b_shiny, a))
    assert_elementwise_equal(b - a_shiny, elementwise_sub(b, a_shiny))
    assert_elementwise_equal(a_shiny - b, elementwise_sub(a_shiny, b))
