
#  Simple binary searching
#  O(logn)

def binary_search(lst, target):
  print("searching for",target,"in",lst)
  def mid(lower, upper):
    return int((upper - lower) / 2) + lower
  s = len(lst)
  lower = 0
  upper = s - 1
  m = mid(lower, upper)
  while lower < upper and m not in [lower, upper]:
    if lst[m] == target:
      break
    elif lst[m] > target:
      upper = m
    elif lst[m] < target:
      lower = m
    m = mid(lower, upper)	
    #print(lower, m, upper)
  if lst[m] != target:
    m = -1
  return m	


print("Binary searching")
lst1 = [0,1,2,3,4,5,6,7,8,9,10,11,12]
print(binary_search(lst1, 0) == 0)  
print(binary_search(lst1, 1) == 1)  
print(binary_search(lst1, 2) == 2)  
print(binary_search(lst1, 3) == 3)  
print(binary_search(lst1, 4) == 4)  
print(binary_search(lst1, 5) == 5)  
print(binary_search(lst1, 6) == 6)  
print(binary_search(lst1, 7) == 7)  
print(binary_search(lst1, 8) == 8)  
print(binary_search(lst1, 9) == 9)  
print(binary_search(lst1, 10) == 10)  
print(binary_search(lst1, 11) == 11)  
print(binary_search(lst1, 18) == -1)  
print(binary_search(lst1, -1) == -1)
print(binary_search(lst1, 99) == -1)