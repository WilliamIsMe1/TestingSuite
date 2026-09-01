from typing import Callable
from time import time
from os import get_terminal_size


class TestError(Exception):
    def __init__(self, message: str):
        self.message: str = message


class UnitTest:
    def __init__(self, test_function: Callable, tags: list[str]):
        self.test_function = test_function
        self.tags: list[str] = tags or []
        pass

    def run(self) -> tuple[bool, str, float]:
        start_time = time()

        try:
            self.test_function()
            end_time = time()
        except TestError as e:
            end_time = time()
            return False, e.message, end_time - start_time

        return True, "Passed.", end_time - start_time


class Suite:
    def __init__(self, tests: dict[str, UnitTest]):
        self.tests = tests
        self.tags: dict[str, list[str]] = {}

        for name, test in self.tests.items():
            for tag in test.tags:
                tag_list = self.tags.setdefault(tag, [])
                if name not in tag_list:
                    tag_list.append(name)

    def run_all(self) -> int:
        return self.run([name for name, test in self.tests.items()])

    def run_tags(self, tags: list[str]) -> int: # Bug already exists: repeating tests
        if len(tags) == 1:
            print(f"Running test tag {tags[0]}", flush=True)
        else:
            print(f"Running test tags {', '.join(tags)}", flush=True)

        tests_to_run: list[str] = []
        for tag in tags:
            for name in self.tags[tag]:
                if name in tests_to_run:
                    continue
                tests_to_run.append(name)

        return self.run(tests_to_run)

    def run(self, tests_to_run: list[str]) -> int:
        red = "\x1b[31m"
        green = "\x1b[32m"
        reset = "\x1b[0m"
        bold = "\x1b[1m"
        test_count = 0
        total_tests_passed = 0
        total_elapsed = 0

        for name, test in self.tests.items():
            if name not in tests_to_run:
                continue
            test_count += 1
        if test_count == 0:
            print(f"{bold}{red}Cannot run zero tests!", flush=True)
            return 1
        print(f"Running {test_count} tests", flush=True)

        test_number = 0
        for name, test in self.tests.items():
            status, message, elapsed = test.run()
            total_elapsed += elapsed
            if name not in tests_to_run:
                continue

            if status:
                total_tests_passed += 1
                print(f"{reset}[{int(100*test_number/test_count)}%] {bold}{green}{name} passed in {elapsed:.4g} seconds", flush=True)
            else:
                print(f"{reset}[{int(100*test_number/test_count)}%] {bold}{red}{name} failed: {message} in {elapsed:.4g} seconds", flush=True)
            test_number += 1
        terminal_size = 120
        try:
            terminal_size = get_terminal_size().columns
        except OSError:
            pass
        print(reset + "-" * terminal_size)
        print(f"{reset}[{int(100*test_number/test_count)}%] Tests success rate: {int((total_tests_passed / test_count)*100)}% at {total_tests_passed}/{test_count}")
        print(f"{reset}Total elapsed time: {total_elapsed:.4g} seconds")

        if total_tests_passed == test_count:
            print(f"{reset}All tests passed", flush=True)
            return 0
        return 1


def assert_equals(a, b, message: str = "Expected {a}, but got {b}", tolerance: float = 0.0):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if abs(a - b) > tolerance:
            raise TestError(message.format(a=a, b=b))
        return

    if not (a == b):
        raise TestError(message.format(a=a, b=b))


def assert_not_equals(result, unwanted, message: str = "Expected {result} to not be equal to {unwanted}", tolerance: float = 0.0):
    if isinstance(result, (int, float)) and isinstance(unwanted, (int, float)):
        if abs(result - unwanted) <= tolerance:
            raise TestError(message.format(result=result, unwanted=unwanted))
        return

    if result == unwanted:
        raise TestError(message.format(result=result, unwanted=unwanted))


def assert_greater_than(a: (float | int), b: (float | int)):
    if a <= b:
        raise TestError(f"{a} should be greater than {b}")


def assert_less_than(a: (float | int), b: (float | int)):
    if a >= b:
        raise TestError(f"{a} should be less than {b}")


def assert_greater_than_equal(a: (float | int), b: (float | int)):
    if a < b:
        raise TestError(f"{a} should be greater than or equal to {b}")


def assert_less_than_equal(a: (float | int), b: (float | int)):
    if a > b:
        raise TestError(f"{a} should be less than or equal to {b}")


def assert_raises(a: Callable, *args):
    try:
        a(*args)
    except Exception:
        return
    raise TestError(f"{a} didn't raise an exception")


def assert_not_raises(a: Callable, *args):
    try:
        a(*args)
    except Exception as e:
        raise TestError(f"{a} raised an exception: {e}")


import importlib


# TODO Learn importlib
def import_tests(module_name: str) -> dict[str, UnitTest]:
    module = importlib.import_module(module_name)


    pass