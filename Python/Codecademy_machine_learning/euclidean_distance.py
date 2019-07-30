#DISTANCE FORMULA
# Euclidean Distance
# Euclidean Distance is the most commonly used distance formula. To find the Euclidean distance between two points, we first calculate the squared distance between each dimension. If we add up all of these squared differences and take the square root, we’ve computed the Euclidean distance.
# Let’s take a look at the equation that represents what we just learned:
# \sqrt{(a_1-b_1)^2+(a_2-b_2)^2+\ldots+(a_n - b_n)^2} 
# The image below shows a visual of Euclidean distance being calculated:
# The Euclidean distance between two points.
# d = \sqrt{(a_1-b_1)^2+(a_2-b_2)^2}

# Instructions
# 1.
# Create a function named euclidean_distance() that takes two lists as parameters named pt1 and pt2.

# In the function, create a variable named distance, set it equal to 0, and return distance.

# In Python, a function is defined using the def keyword:

# def euclidean_distance(pt1, pt2):
#   distance = 0
#   # We will be adding code here next
#   return 0
# 2.
# After defining distance, create a for loop to loop through the dimensions of each point.

# Add the squared difference between each dimension to distance.

# Remember, in Python, you can square the variable num by using num ** 2.

# Your for loop should look like this:

# for i in range(len(pt1)):
#   distance = distance + (pt1[i] - pt2[i]) ** 2
# You can simplify it by using the += operator:

# for i in range(len(pt1)):
#   distance += (pt1[i] - pt2[i]) ** 2
# The len() method returns the number of elements in the list.

# 3.
# Outside of the for loop, take the square root of distance and return that value.

# You can get the square root of num by using num ** 0.5.

# 4.
# Print the Euclidean distance between [1, 2] and [4, 0].

# Print the Euclidean distance between [5, 4, 3] and [1, 7, 9].

# Why can’t you find the difference between [2, 3, 4] and [1, 2]?


def euclidean_distance(pt1, pt2):
  distance = 0
  if len(pt1) != len(pt2):
    raise ValueError('NON-MATCHING LIST LENGTHS')
    
  for i in range(len(pt2)):
    # print('x:\t' + str(x) + ', y:\t' + str(y) + ', distance:\t' + str(distance))
    x = pt1[i]
    y = pt2[i]
    distance += ((x - y) ** 2)
    
  #return math.sqrt(distance)
  return distance ** 0.5
  
  
  #Print the Euclidean distance between [1, 2] and [4, 0].
print('Euclidean distance between [1, 2] and [4, 0]\n\t' + str(euclidean_distance([1, 2], [4, 0])))

#Print the Euclidean distance between [5, 4, 3] and [1, 7, 9].

print('Euclidean distance between [5, 4, 3] and [1, 7, 9]\n\t' + str(euclidean_distance([5, 4, 3], [1, 7, 9])))

#Why can’t you find the difference between [2, 3, 4] and [1, 2]?

print('Euclidean distance between [1, 2] and [4, 0]\n\t' + str(euclidean_distance([2, 3, 4], [1, 2])))