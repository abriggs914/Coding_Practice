#DIJKSTRA'S ALGORITHM: PYTHON
#Understanding Heapq
#Remember that Dijkstra’s Algorithm works like the following:
#Instantiate a dictionary that will eventually map vertices to their distance from their start vertex
#Assign the start vertex a distance of 0 in a min heap
#Assign every other vertex a distance of infinity in a min heap
#Remove the vertex with the smallest distance from the min heap and set that to the current vertex
#For the current vertex, consider all of it’s adjacent vertices and calculate the distance to them by (distance to the current vertex) + (edge weight of current vertex to adjacent vertex). If this new distance is less than its current distance, replace the distance.
#Repeat 4 and 5 until the heap is empty
#After the heap is empty, return the distances
#In order to keep track of all the distances for Dijkstra’s Algorithm, we will be using a heap! Using a heap will allow removing the minimum from the heap to be efficient. In python, there is a library called heapq which we will use to do all of our dirty work for us!
#The heapq method has two critical methods we will use in Dijkstra’s Algorithm: heappush and heappop.
#heappush will add a value to the heap and adjust the heap accordingly
#heappop will remove and return the smallest value from the heap
#Let’s say we start by initializing a heap with the following tuple inside:
#heap = [(0, 'A')]
#We can add values to this heap like this:
#heapq.heapush(heap, (1, 'B'))
#heapq.heapush(heap, (-4, 'C'))
#We can remove the smallest value in the heap like this:
#value, letter  = heapq.heappop(heap)
#value will be equal to -4, and letter will be equal to 'C'.
#You can read more about the documentation of heapq here.

#Write Import Statement here
import heapq


heap = [(0, 'A')]
heapq.heappush(heap, (1, 'B'))
heapq.heappush(heap, (-5, 'D'))
heapq.heappush(heap, (4, 'E'))
heapq.heappush(heap, (2, 'C'))

print("The smallest values in the heap in ascending order are:\n")
while heap:
  print(heapq.heappop(heap))
  