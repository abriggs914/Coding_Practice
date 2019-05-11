# define binary_search()
def binary_search(sorted_list, target):
  if not sorted_list:
    return 'value not found'
  mid_idx = len(sorted_list)//2
  mid_val = sorted_list[mid_idx]
  if mid_val == target:
    return mid_idx
  if (mid_val > target):
    left_half = sorted_list[:mid_idx]
    return binary_search(left_half, target)
  else:
    right_half = sorted_list[mid_idx+1:]
    result = binary_search(right_half, target)
    if result == "value not found":
      return result
    return mid_idx + result + 1
  

# For testing:
sorted_values = [13, 14, 15, 16, 17]
print(binary_search(sorted_values, 13) ,binary_search(sorted_values, 13) == 0)
print(binary_search(sorted_values, 14) ,binary_search(sorted_values, 14) == 1)
print(binary_search(sorted_values, 15) ,binary_search(sorted_values, 15) == 2)
print(binary_search(sorted_values, 16) ,binary_search(sorted_values, 16) == 3)
print(binary_search(sorted_values, 17) ,binary_search(sorted_values, 17) == 4)
print(binary_search(sorted_values, 20) ,binary_search(sorted_values, 20) == "value not found")

