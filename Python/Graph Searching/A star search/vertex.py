class Vertex:
	def __init__(self, x, y, value, is_goal=False, heurisitic_val=0):
		self.x = x
		self.y = y
		self.value = value
		self.edges = {}
		self.is_goal = is_goal
		self.heurisitic_val = heurisitic_val

	#Inside vertex.py, alter the .add_edge() method so it takes an additional argument of weight.
	#weight should default to the value of 0.
  
	#Replace the value of True with the value of weight passed into the method.
	def add_edge(self, vertex, weight=0):
		self.edges[vertex] = weight

	def get_edges(self):
		return list(self.edges.keys())
		
	def __repr__(self):
		#return str(self.value) + " at {" + str(self.x) + "," + str(self.y) + "}"
		return "{name} at ({x}, {y})".format(name=self.value, x=self.x, y=self.y)
