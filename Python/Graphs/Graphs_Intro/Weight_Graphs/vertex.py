class Vertex:
  def __init__(self, value):
    self.value = value
    self.edges = {}

  #Inside vertex.py, alter the .add_edge() method so it takes an additional argument of weight.
  #weight should default to the value of 0.
  
  #Replace the value of True with the value of weight passed into the method.
  def add_edge(self, vertex, weight=0):
    self.edges[vertex] = weight

  def get_edges(self):
    return list(self.edges.keys())
