from tests import graph_1
import random as rand

# A* searching algorithm using a graph structure

print(graph_1)
print(graph_1.graph_dict)

# Graph logic
# set distance cost coefficient

D_COST = 2

# arbitrary heuristic simulating manhattan distance
# works for graphs with multiple goal vertices
def heuristic(graph, vertex):
	min_h = None
	goals = graph_1.get_goals()
	for g_vertex in goals:
		dx = abs(vertex.x - g_vertex.x)
		dy = abs(vertex.y - g_vertex.y)
		d = D_COST * (dx + dy)
		if min_h is None or d < min_h:
			min_h = d
	return min_h
	
for v, path in graph_1.graph_dict.items():
	print(v, heuristic(graph_1, path))
	
def a_star(graph, start_vertex=None):
	if start_vertex is None:
		start_vertex = graph.graph_dict[rand.choice(list(graph.graph_dict.keys()))]
	
	goals = graph.get_goals()
	if not goals:
		print("No goal vertices found, unable to perform search.")
		return
	print("Searching for one of {goals}, starting at vertex {start_vertex}".format(goals=goals, start_vertex=start_vertex))
	frontier = []
	expanded = []
	total_cost = 0
	
	curr_vertex = start_vertex
	while True:
		if curr_vertex in goals:
			# found!
			break
		next = start_vertex.get_edges()
		print("next", next)
		min_cost = 0
		for v in next:
			vertex = graph.graph_dict[v]
			print("vertex", vertex,"curr_vertex.edges",curr_vertex.edges)
			cost = curr_vertex.edges[v] + heuristic(graph, vertex)
			print("vertex:", vertex, "cost", cost)
		break
	print("Total cost: {0}".format(total_cost))
	return total_cost
	
	
print(a_star(graph_1))