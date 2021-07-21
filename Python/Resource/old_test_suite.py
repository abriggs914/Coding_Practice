import shutil
import pprint
import inspect
from utility import *


def get_terminal_columns():
    return shutil.get_terminal_size().columns


def run_tests(func, test_set):
    w = get_terminal_columns()
    hw = int(w * 0.75)
    border = "".join(["#" for i in range(hw)])
    # print(border)
    failed_tests = []
    passed_tests = []
    longest_name = max([len(name) for name in test_set])
    longest_test = max([len(str(test_list)) for test_list in test_set.values() if test_list])
    print("\n\n" + pad_centre("Testing: " + str(func), w) + "\n")
    num_tests = len(test_set)
    for name, test_args in test_set.items():

        test_name = "\n" + pad_centre(name.ljust(longest_name, " "), w) + "\n"
        print(pad_centre(border, w) + "\n" + test_name)

        args = test_args[0]
        desired_answer = test_args[1]
        work_below = "-v- WORK -v-"
        work_above = "-^- WORK -^-"
        div = "".join(["-" for i in range(w // 2 - len(work_above) // 2)])
        print(div + work_below + div)
        result = func(*args)
        print(div + work_above + div)
        is_desired_result = (result == desired_answer)

        args_str = pad_centre("args:\t\t" + str(args).rjust(longest_test, " "), w) + "\n"
        desired_str = pad_centre("desired:\t" + str(desired_answer).rjust(longest_test, " "), w) + "\n"
        result_str = pad_centre("got:\t\t" + str(result).rjust(longest_test, " "), w) + "\n"

        print(args_str + desired_str + result_str + pad_centre(
            "correct:\t" + str(is_desired_result).rjust(longest_test, " "), w) + "\n" + pad_centre(border, w))

        # print("result t:(" + str(type(result)) + "): " + str(result))
        # print("desired_answer: t:(" + str(type(desired_answer)) + ")" + str(desired_answer))
        # print("result == desired_answer: t(" + str(type((result == desired_answer))) + ")" + str(result == desired_answer))
        # print("is_desired_result: " + str(is_desired_result))

        if not is_desired_result:
            failed_tests.append(name)
        else:
            passed_tests.append(name)

    num_failed = len(failed_tests)
    # wprint("\n\tFailed Tests\t" + str(num_failed) + " / " + str(num_tests) + "\n-\t" + "\n-\t".join(test for test in failed_tests) + "\n")
    return passed_tests, failed_tests


def run_multiple_tests(tests_to_run):
    w = get_terminal_columns()
    border = "".join(["#" for i in range(w)])
    passed_tests = {}
    failed_tests = {}
    num_tests = 0
    num_passed = 0
    num_failed = 0
    print(border)
    for test in tests_to_run:
        func, test_set = test
        num_tests += len(test_set)
        test_results_passed, test_results_failed = run_tests(func, test_set)
        name = func.__name__ + " - line " + str(int(str(inspect.findsource(func)).split()[-1][
                                                    :-1]) + 1)  # str(inspect.getframeinfo(inspect.stack()[1][0]).lineno)
        if name not in failed_tests:
            failed_tests[name] = []
        if name not in passed_tests:
            passed_tests[name] = []
        print("\n{}<\n{}\n>\n".format(name, test_results_failed))
        if test_results_failed:
            # print("inspect.stack()(" + str(len(inspect.stack())) + "):\n\t", "\n\t".join(list(map(str, inspect.stack()))))
            # name = func.__name__ + " - line " + str(int(str(inspect.findsource(func)).split()[-1][:-1]) + 1)  # str(inspect.getframeinfo(inspect.stack()[1][0]).lineno)
            failed_tests[name] += test_results_failed
            num_failed += len(test_results_failed)
        if test_results_passed:
            passed_tests[name] += test_results_passed
            num_passed += len(test_results_passed)

    print("\n<\n{}\n>\n".format(failed_tests))

    print("\n\t-- Passed Tests --\t" + str(num_passed) + " / " + str(num_tests))
    for func, passed_test_results in passed_tests.items():
        print("\t\t-\t" + func + "\n\t\t\t>\t" + "\n\t\t\t>\t".join(
            test_name for test_name in passed_test_results) + "\n")

    print("\n\t-- Failed Tests --\t" + str(num_failed) + " / " + str(num_tests))
    for func, failed_test_results in failed_tests.items():
        # print("failed_test_results:", failed_test_results)
        print("\t\t-\t" + func + "\n\t\t\t>\t" + "\n\t\t\t>\t".join(
            test_name for test_name in failed_test_results) + "\n")
    print(border)


# for test in failed_test_results:
# wprint("failed_test_results:", failed_test_results, "test:", test)
# wprint("\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")


# run_tests(greatest_diff, greatest_diff_test_set)
# run_tests(remaining_list, remaining_list_test_set)
# run_tests(outside_indices, outside_indices_test_set)
# run_tests(cut_puzzle, cut_puzzle_test_set)
# run_tests(pad_puzzle, pad_puzzle_test_set)
# run_tests(remaining_spaces, remaining_spaces_test_set)
# run_tests(np_count, np_count_test_set)
# run_tests(invert_puzzle, invert_puzzle_test_set)
# run_tests(check_puzzle_is_solved, check_puzzle_is_solved_test_set)
# run_tests(ensure_list, ensure_list_test_set)
# run_tests(n_combinations, n_combinations_test_set)


# example:
def do_test():
    def add(a, b):
        print("Doing work")
        return a + b

    add_test_set = {
        "test_1, Add 5 and 6": [
            [
                5,
                6
            ],
            12
        ],
        "test_2, Add 8 and 6": [
            [
                8,
                6
            ],
            14
        ],

    }
    tests_to_run = [(add, add_test_set)]
    run_multiple_tests(tests_to_run + [
        (lambda x: x, {"test": [["arg"], "arg"]})  # simplest usage I could think of.
    ])


# tests_to_run = [
# (greatest_diff, greatest_diff_test_set),
# (remaining_list, remaining_list_test_set),
# (outside_indices, outside_indices_test_set),
# (cut_puzzle, cut_puzzle_test_set),
# (pad_puzzle, pad_puzzle_test_set),
# (pad_puzzle, pad_puzzle_test_set),
# (remaining_spaces, remaining_spaces_test_set),
# (np_count, np_count_test_set),
# (invert_puzzle, invert_puzzle_test_set),
# (check_puzzle_is_solved, check_puzzle_is_solved_test_set),
# (ensure_list, ensure_list_test_set),
# (permutations, permutations_test_set),
# (n_combinations, n_combinations_test_set)
# ]
# run_multiple_tests(tests_to_run)

# class TestDriver:
# 	class FuncDriver:
#
# 	def __init__(self, name=None, func=None):
# 		self.name = name if name is not None else "Un-named"
# 		self.func = func if func is not None else print
# 		self.test_sets = []
# 	def
#
# if __name__ == "__main__":
# 	do_test()

if __name__ == "__main__":
    def func_def():
        pass


    class TestSuite:
        """Class used to run a batch of tests on functions"""

        def __init__(
                self,
                test_func=None,
                tests=None,
                name="Untitled Test Suite"
        ):
            self.tests = {}
            self.test_order = []

            if not isinstance(test_func, type(func_def)):
                test_func = None
            # list of un-labeled tests or dict of labeled tests.
            if not isinstance(tests, list) and not isinstance(tests, tuple) and not isinstance(tests, dict):
                tests = {}
            print("tests:", tests)
            if isinstance(tests, list) or isinstance(tests, tuple):
                for tst in tests:
                    print("tst:", tst)
                    if (not isinstance(tst, list) and not isinstance(tst, tuple)) or len(tst) != 2:
                        if isinstance(tst, dict):
                            raise TypeError(
                                "Dictionary value: \"{}\" cannot be converted into a valid test.\nRemove encapsulating list and refactor to a single dictionary.".format(
                                    tst))
                        raise TypeError("Values: \"{}\" cannot be converted into a valid test.".format(tst))
                    if not isinstance(tst[0], tuple) and not isinstance(tst[0], list):
                        tst = [[tst[0]], tst[1]]
                    # raise ValueError("new_tst:", tst)
                    self.add_test(self.new_test_key(), tst)
                # self.tests.update({self.new_test_key(): tst})

            self.test_func = test_func
            # self.tests = tests
            self.name = name

        # self.test_batches = {}
        #
        # for func, test_sets in zip(test_funcs, tests):
        # 	self.test_batches[func] = test_sets

        def set_func(self, func, clear_tests=False):
            if not isinstance(func, type(func_def)):
                raise ValueError("Function value \"{}\" is not a valid function definition".format(func))
            self.test_func = func
            if clear_tests:
                self.clear_tests()

        def clear_func(self):
            self.test_func = None

        def get_test(self, idx):
            return self.tests[self.test_order[idx]]

        def clear_tests(self):
            self.tests.clear()

        def add_test(self, key, tst):
            self.tests.update({key: tst})
            self.test_order.append(key)

        def new_test_key(self):
            def new_test_key_rec(key):
                if key not in self.tests:
                    return key
                else:
                    return new_test_key_rec(key + " ")

            return new_test_key_rec("Test {}".format(len(self.tests) + 1))

        def execute(self, start=None, end=None):
            if self.test_func is None:
                print("Please first initialize a function to test.")
                return
            if not self.tests:
                print("Please first create tests for your function.")
                return

            start = start if start is not None else 0
            end = end if end is not None else len(self.tests)
            start, end = minmax(start, end)
            start = max(0, start)
            end = max(0, end)
            l = end - start
            keys = self.test_order[start: end]
            # tests_to_run = list(zip([self.test_func for i in range(l)], {k: self.tests[k] for k in keys}))
            tests_to_run = []
            for k in keys:
                tests_to_run.append((self.test_func, {k: self.tests[k]}))
            print("==Tests:\n\n", "\n".join(list(map(str, tests_to_run))), "\n\n", tests_to_run)
            run_multiple_tests(tests_to_run)

        def __repr__(self):
            keys = ["test_func", "tests", "name"]
            vals = [getattr(self, key) for key in keys]
            max_key = max([len(key) for key in keys])
            max_val = max([lenstr(val) for val in vals])
            res = dict(zip([key.ljust(max_key) for key in keys], [str(val).rjust(max_val) for val in vals]))
            return dict_print(res, "self")


    oya = str()
    oyb = list()
    oyc = dict()
    oyd = int()
    oye = float()
    oyf = object()
    oyg = func_def

    tya = type(oya)
    tyb = type(oyb)
    tyc = type(oyc)
    tyd = type(oyd)
    tye = type(oye)
    tyf = type(oyf)
    tfg = type(oyg)

    TS1 = TestSuite()
    print("TS1 after creation:\n\n", TS1)
    TS2 = TestSuite(test_func=[lambda x: x], tests={"test": [["arg"], "arg"]})
    print("TS2 after creation:\n\n", TS2)

    TS3 = TestSuite(test_func=[lambda x: x, lambda x: str(x) + " 1"], tests={"test": [["arg"], "arg"]})
    print("TS3 after creation:\n\n", TS3)

    TS4 = TestSuite(test_func=[lambda x: x, lambda x: str(x) + " 1"], tests=((["arg"], "arg"), (("same"), "same")))
    print("TS4 after creation:\n\n", TS4)
    TS4.execute()
    TS4.set_func(lambda x: x)
    TS4.execute()
    TS4.set_func(lambda x: x + "1")
    TS4.execute()
