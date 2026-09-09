# TestingSuite

A test suite system created for python as a learning project, whilst also being production worthy.

## Featured Capabilities

- Imported Tests
- An assortion of assertions
- Time measurement
- Easy test creation

## Usage
```python
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

exit(Suite(import_tests("example")).run_all()) # run_all returns an exit code
```
