load_file_in_context("script.py")

try:
  for i in numbers_b:
    if i not in range(1000):
      fail_tests("Is `number_b` set equal to `random.sample(range(1000), 12)`?")
  if len(numbers_b) != 12:
    fail_tests("Is `number_b` set equal to `random.sample(range(1000), 12)`?")
except NameError:
  fail_tests("Is `number_b` defined?")

pass_tests()