#DISTANCE FORMULA
# Manhattan Distance
# Manhattan Distance is extremely similar to Euclidean distance. Rather than summing the squared difference between each dimension, we instead sum the absolute value of the difference between each dimension. It’s called Manhattan distance because it’s similar to how you might navigate when walking city blocks. If you’ve ever wondered “how many blocks will it take me to get from point A to point B”, you’ve computed the Manhattan distance.

# The equation is shown below:

# \mid a_1 - b_1 \mid + \mid a_2 - b_2 \mid + \ldots + \mid a_n - b_n \mid∣a 
# 1
# ​	 −b 
# 1
# ​	 ∣+∣a 
# 2
# ​	 −b 
# 2
# ​	 ∣+…+∣a 
# n
# ​	 −b 
# n
# ​	 ∣
# Note that Manhattan distance will always be greater than or equal to Euclidean distance. Take a look at the image below visualizing Manhattan Distance:

# The Manhattan distance between two points.

# d = \mid a_1 - b_1 \mid + \mid a_2 - b_2 \midd=∣a 
# 1
# ​	 −b 
# 1
# ​	 ∣+∣a 
# 2
# ​	 −b 
# 2
# ​	 ∣
# Instructions
# 1.
# Below euclidean_distance(), create a function called manhattan_distance() that takes two lists named pt1 and pt2 as parameters.

# In the function, create a variable named distance, set it equal to 0, and return it.

# We are creating a brand new function here.

# 2.
# After defining distance, create a for loop to loop through the dimensions of each point.

# Add the absolute value of the difference between each dimension to distance.
# DISTANCE FORMULA
# Manhattan Distance
# Manhattan Distance is extremely similar to Euclidean distance. Rather than summing the squared difference between each dimension, we instead sum the absolute value of the difference between each dimension. It’s called Manhattan distance because it’s similar to how you might navigate when walking city blocks. If you’ve ever wondered “how many blocks will it take me to get from point A to point B”, you’ve computed the Manhattan distance.

# The equation is shown below:

# \mid a_1 - b_1 \mid + \mid a_2 - b_2 \mid + \ldots + \mid a_n - b_n \mid∣a 
# 1
# ​	 −b 
# 1
# ​	 ∣+∣a 
# 2
# ​	 −b 
# 2
# ​	 ∣+…+∣a 
# n
# ​	 −b 
# n
# ​	 ∣
# Note that Manhattan distance will always be greater than or equal to Euclidean distance. Take a look at the image below visualizing Manhattan Distance:

# The Manhattan distance between two points.

# d = \mid a_1 - b_1 \mid + \mid a_2 - b_2 \midd=∣a 
# 1
# ​	 −b 
# 1
# ​	 ∣+∣a 
# 2
# ​	 −b 
# 2
# ​	 ∣
# Instructions
# 1.
# Below euclidean_distance(), create a function called manhattan_distance() that takes two lists named pt1 and pt2 as parameters.

# In the function, create a variable named distance, set it equal to 0, and return it.

# We are creating a brand new function here.

# 2.
# After defining distance, create a for loop to loop through the dimensions of each point.

# Add the absolute value of the difference between each dimension to distance.

# Remember, in Python, you can take the absolute value of num by using abs(num)

# Your loop should look almost identical to the one in euclidean_distance().

# You should add abs(pt1[i] - pt2[i]) to distance rather than the squared difference.

# 3.
# You’re done with manhattan_distance()! Go ahead and find the Manhattan distance between the same points as last time.

# Below the print statements for Euclidean distance, print the Manhattan distance between [1, 2] and [4, 0].

# Also print the Manhattan distance between [5, 4, 3] and [1, 7, 9].

def euclidean_distance(pt1, pt2):
  distance = 0
  for i in range(len(pt1)):
    distance += (pt1[i] - pt2[i]) ** 2
  return distance ** 0.5

print('\tEUCLIDEAN')
print(euclidean_distance([1, 2], [4, 0]))
print(euclidean_distance([5, 4, 3], [1, 7, 9]))

def manhattan_distance(pt1, pt2):
  distance = 0
  for i in range(len(pt2)):
    distance += abs(pt1[i] - pt2[i])
  return distance

print('\tMANHATTAN')
print(manhattan_distance([1, 2], [4, 0]))
print(manhattan_distance([5, 4, 3], [1, 7, 9]))
# Remember, in Python, you can take the absolute value of num by using abs(num)

# Your loop should look almost identical to the one in euclidean_distance().

# You should add abs(pt1[i] - pt2[i]) to distance rather than the squared difference.

# 3.
# You’re done with manhattan_distance()! Go ahead and find the Manhattan distance between the same points as last time.

# Below the print statements for Euclidean distance, print the Manhattan distance between [1, 2] and [4, 0].

# Also print the Manhattan distance between [5, 4, 3] and [1, 7, 9].