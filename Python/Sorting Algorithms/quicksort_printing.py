# Define your quicksort function

#Apparently my version doesnt work for codeacademy.............
  
# Define your quicksort function
def quicksort_my(list, start, end):
  print(start, end)
  if (start >= end):
    return
  print(list[start])
  quicksort_my(list, start+1,end)
  
colors = ["blue", "red", "green", "purple", "orange"]
quicksort_my(colors,0,4)

def quicksort_1(list, start, end):
  if start >= end:
    return

  print(list[start])
  start += 1
  quicksort_1(list, start, end)

colors = ["blue", "red", "green", "purple", "orange"]
quicksort_1(colors, 0, len(colors) - 1)
