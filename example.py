from testing import *


def add(x, y):
    return x + y


def test1_function():
    assert_equals(add(1, 2), 3)
    assert_equals(add(13, 2), 15)
    assert_equals(add(0.1, 0.2), 0.3, tolerance=1.0e-4)


def test2_function():
    assert_raises(add, 1, "15")


test1 = UnitTest(test1_function)
test2 = UnitTest(test2_function)

suite = Suite({"test1": test1, "test2": test2})

suite.run(["test1", "test2"])
