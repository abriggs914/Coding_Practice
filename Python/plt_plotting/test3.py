load_file_in_context("script.py")

try:
  if numbers_a != range(13):
    fail_tests("Is `number_a` set equal to `range(13)`?")
except NameError:
  fail_tests("Is `number_a` defined?")

pass_tests()