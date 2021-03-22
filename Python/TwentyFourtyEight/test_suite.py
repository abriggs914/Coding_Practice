import shutil
import pprint
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
		div = "".join(["-" for i in range(w//2 - len(work_above)//2)])
		print(div + work_below + div)
		result = func(*args)
		print(div + work_above + div)
		is_desired_result = (result == desired_answer)
		
		args_str = pad_centre("args:\t\t" + str(args).rjust(longest_test, " "), w) + "\n"
		desired_str = pad_centre("desired:\t" + str(desired_answer).rjust(longest_test, " "), w) + "\n"
		result_str = pad_centre("got:\t\t" + str(result).rjust(longest_test, " "), w) + "\n"
		
		print(args_str + desired_str + result_str + pad_centre("correct:\t" + str(is_desired_result).rjust(longest_test, " "), w) + "\n" + pad_centre(border, w))
		
		print("result t:(" + str(type(result)) + "): " + str(result))
		print("desired_answer: t:(" + str(type(desired_answer)) + ")" + str(desired_answer))
		print("result == desired_answer: t(" + str(type((result == desired_answer))) + ")" + str(result == desired_answer))
		print("is_desired_result: " + str(is_desired_result))
		# if type(is)
		# if type(is_desired_result) == 
		if not is_desired_result:
			failed_tests.append(name)
		else:
			passed_tests.append(name)
	
	num_failed = len(failed_tests)
	# wprint("\n\tFailed Tests\t" + str(num_failed) + " / " + str(num_tests) + "\n-\t" + "\n-\t".join(test for test in failed_tests) + "\n")
	print("\n\t-- Passed Tests --\t" + str(num_tests - num_failed) + " / " + str(num_tests) + "\n\t-\t" + "\n\t-\t".join(test for test in passed_tests) + "\n")
	return failed_tests
	
	
def run_multiple_tests(tests_to_run):
	w = get_terminal_columns()
	border = "".join(["#" for i in range(w)])
	failed_tests = {}
	num_tests = 0
	num_failed = 0
	print(border)
	for test in tests_to_run:
		func, test_set = test
		num_tests += len(test_set)
		test_results = run_tests(func, test_set)
		if test_results:
			failed_tests[str(func)] = test_results
			num_failed += len(test_results)
		
	print("\n\t-- Failed Tests --\t" + str(num_failed) + " / " + str(num_tests))
	for func, failed_test_results in failed_tests.items():
		print("\t-\t"+ "\n\t-\t".join(test_name for test_name in failed_test_results) + "\n")
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
	run_multiple_tests(tests_to_run)


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

if __name__ == "__main__":
	do_test()