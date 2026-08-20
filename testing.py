class TestError(Exception):
    def __init__(self, message: str):
        self.message: str = message

class Suite:
    def __init__(self, tests: dict[str, UnitTest]):
        self.tests = tests
        pass

    def run_all(self):
        self.run([name for name, test in self.tests.items()])

    def run(self, tests_to_run: list[str]):
        total_tests = 0
        total_tests_passed = 0
        for name, test in self.tests.items():
            if name not in tests_to_run:
                continue
            total_tests += 1
            status, message = test.run()
            if status:
                total_tests_passed += 1
                print(f"{name} passed")
            else:
                print(f"{name} failed: {message}")
        print(f"Tests success rate: {total_tests_passed / total_tests} at {total_tests_passed}/{total_tests}")
        if total_tests_passed == total_tests:
            print("All tests passed")
        pass


class UnitTest:
    def __init__(self, test_function):
        self.test_function = test_function
        pass

    def run(self) -> tuple[bool, str]:
        try:
            self.test_function()
        except TestError as e:
            return False, e.message
        return True, "Passed."

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
