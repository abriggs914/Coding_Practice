#Inside of vertex.py, define a Vertex class. Within the Vertex class, define an __init__() method that takes self and value. Set self.value equal to value and self.edges equal to an empty dictionary.
class Vertex:
  
  def __init__(self, value):
    self.value = value
    self.edges = {} 
    

  # define .add_edge() here
  #Within Vertex, define the method .add_edge() that takes self, and vertex as arguments. The vertex argument will be the .value of another instance of Vertex.
  #In the body, print Adding edge to  + vertex.
  #Use the vertex as a key within self.edges and set it to True.
  def add_edge(self, vertex):
    print("Adding edge to",vertex)
    self.edges[vertex] = True
    
  #Define a .get_edges() method on Vertex which takes in self and returns a list of the keys of the .edges dictionary.
  #.get_edges() is a convenience method which gives us a list of the names of the vertices connected to self.
  def get_edges(self):
    return list(self.edges.keys())
  
#Outside the Vertex class, make an instance of Vertex with the argument "Cronk" and assign it to the variable station.

station = Vertex("Cronk")

grand_central = Vertex('Grand Central Station')
forty_second_street = Vertex('42nd Street Station')

print(grand_central.get_edges())

# call .add_edge() below here
#Use .add_edge() to assign forty_second_street.value as an edge of grand_central.
grand_central.add_edge(forty_second_street.value)

print(grand_central.get_edges())
