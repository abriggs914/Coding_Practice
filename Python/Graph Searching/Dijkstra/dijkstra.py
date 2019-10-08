from heapq import heappop, heappush
from math import inf

"""
graph = {
        'A': [('B', 10), ('C', 3)],
        'C': [('D', 2)],
        'D': [('E', 10)],
        'E': [('A', 7)],
        'B': [('C', 3), ('D', 2)]
    }
"""

graph = {"A":[("B", 6), ("C", 4)],
		"B":[("D", 16), ("E", 8)],
		"C":[("F", 10), ("G", 18)],
		"D":[("H", 14), ("I", 10)],
		"E":[("J", 12)],
		"F":[("J", 6)],
		"G":[("J", 2)],
		"H":[("J", 24)],
		"I":[("J", 18)],
		"J":[]}


def dijkstras(graph, start):
  distances = {}
  
  for vertex in graph:
    distances[vertex] = inf
    
  distances[start] = 0
  vertices_to_explore = [(0, start)]
  
  while vertices_to_explore:
    current_distance, current_vertex = heappop(vertices_to_explore)
    
    for neighbor, edge_weight in graph[current_vertex]:
      new_distance = current_distance + edge_weight
      
      if new_distance < distances[neighbor]:
        distances[neighbor] = new_distance
        heappush(vertices_to_explore, (new_distance, neighbor))
        
  return distances
        
distances_from_d = dijkstras(graph, 'A')
print("\n\nShortest Distances: {0}".format(distances_from_d))

#from heapq import heappop, heappush
#from math import inf
#
# graph = {
#         'A': [('B', 10), ('C', 3)],
#         'C': [('D', 2)],
#         'D': [('E', 10)],
#         'E': [],
#         'B': [('C', 3), ('D', 2)]
#     }


# def dijkstras(graph, start):
#   distances = {}
#   for vertex in graph:
#     distances[vertex] = inf
#   distances[start] = 0
#   vertices_to_explore = [(0, start)]
#   # Finish dijkstras() below:
#   while vertices_to_explore:
#     current_distance, current_vertex = heappop(vertices_to_explore)
#     for neighbor, edge_weight in graph[current_vertex]:
#       new_distance = current_distance + edge_weight
#       if new_distance < distances[neighbor]:
#         distances[neighbor] = new_distance
#         heappush(vertices_to_explore, (new_distance, neighbor))
#   return distances
        
# distances_from_a = dijkstras(graph, 'A')
# print("\n\nShortest Distances: {0}".format(distances_from_a))
