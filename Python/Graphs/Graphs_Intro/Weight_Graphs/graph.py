class Graph:
  def __init__(self, directed = False):
    self.graph_dict = {}
    self.directed = directed

  def add_vertex(self, vertex):
    self.graph_dict[vertex.value] = vertex

  #Tab over to graph.py.
  #Inside Graph, alter .add_edge() so it also takes an additional argument of weight.
  #This argument should also default to 0.
  def add_edge(self, from_vertex, to_vertex, weight=0):
    self.graph_dict[from_vertex.value].add_edge(to_vertex.value, weight)
    if not self.directed:
      self.graph_dict[to_vertex.value].add_edge(from_vertex.value, weight)
