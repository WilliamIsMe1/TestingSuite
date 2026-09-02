from testing import *
import random


def add(x, y):
    return x + y

@test(["add_tests"])
def test1_function():
    assert_equals(add(1, 2), 3)
    assert_equals(add(13, 2), 15)
    assert_equals(add(0.1, 0.2), 0.3, tolerance=1.0e-4)


@test(["add_tests"])
def test2_function():
    assert_not_raises(add, 1, "15")


@test(["add_tests"])
def test3_function():
    assert_not_raises(add, 1, 15)


@test(["add_tests", "stress_tests"])
def test4_function():
    total = 0
    for i in range(1_000_000):
        total = add(total, i)
    assert_equals(total, sum(range(1_000_000)))


@test(["add_tests", "stress_tests"])
def test5_function():
    big1 = 10**18
    big2 = 10**18
    assert_equals(add(big1, big2), 2 * 10**18)
    assert_equals(add(10**300, 10**300), 2 * 10**300)


@test(["add_tests", "stress_tests"])
def test6_function():
    random.seed(42)
    for _ in range(1_000_000):
        a = random.uniform(-1e6, 1e6)
        b = random.uniform(-1e6, 1e6)
        assert_equals(add(a, b), a + b, tolerance=1.0e-6)


@test(["add_tests", "stress_tests"])
def test7_function():
    for _ in range(500_000):
        assert_not_raises(add, random.random(), random.random())


# test1 = UnitTest(test1_function, ["add_tests"])
# test2 = UnitTest(test2_function, ["add_tests"])
# test3 = UnitTest(test3_function, ["add_tests"])
# test4 = UnitTest(test4_function, ["add_tests", "stress_tests"])
# test5 = UnitTest(test5_function, ["add_tests", "stress_tests"])
# test6 = UnitTest(test6_function, ["add_tests", "stress_tests"])
# test7 = UnitTest(test7_function, ["add_tests", "stress_tests"])

# suite = Suite({
#    "test1": test1,
#    "test2": test2,
#    "test3": test3,
#    "test4": test4,
#    "test5": test5,
#    "test6": test6,
#    "test7": test7,
#})

#exit(suite.run_tags(["add_tests"]))

exit(Suite(import_tests("example")).run_all())