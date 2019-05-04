# import random number generator
from random import randrange
# import heap class
from min_heap import MinHeap 

# make an instance of MinHeap
min_heap = MinHeap()

# populate min_heap with random numbers
random_nums = [randrange(1, 101) for n in range(6)]
for el in random_nums:
  min_heap.add(el)


# test it out, is the minimum number at index 1?
print(min_heap.heap_list)

#------------------------------------------------------------------------------------------------------------------------------------

# make an instance of MinHeap
min_heap = MinHeap()

# add elements
min_heap.add(7)
min_heap.add(12)
min_heap.add(42)

# remove minimum element
print(min_heap.retrieve_min())

#------------------------------------------------------------------------------------------------------------------------------------

# make an instance of MinHeap
min_heap = MinHeap()

# set internal list for testing purposes...
min_heap.heap_list = [None, 10, 13, 21, 61, 22, 23, 99]
min_heap.count = 7

print("The smaller child of index 1 is: ")
smaller_child_of_idx_1 = min_heap.get_smaller_child_idx(1)
smaller_child_element = min_heap.heap_list[smaller_child_of_idx_1]
print(smaller_child_element)

print("The smaller child of index 2 is: ")
smaller_child_of_idx_2 = min_heap.get_smaller_child_idx(2)
smaller_child_element = min_heap.heap_list[smaller_child_of_idx_2]
print(smaller_child_element)

print("The smaller child of index 3 is: ")
smaller_child_of_idx_3 = min_heap.get_smaller_child_idx(3)
smaller_child_element = min_heap.heap_list[smaller_child_of_idx_3]
print(smaller_child_element)