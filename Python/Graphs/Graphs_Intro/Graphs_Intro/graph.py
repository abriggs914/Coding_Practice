# Bring in the Vertex class from vertex.py
from vertex import Vertex

# Define Graph below...
#In graphs.py, define a Graph class with an __init__() method that takes self and directed as arguments.
#directed should default to False.
#Set directed as a property on self and set self.graph_dict to be an empty dictionary.
class Graph:
  
  def __init__(self, directed=False):
    self.directed = directed
    self.graph_dict = {}
    
  #In graphs.py, define the .add_vertex() method on Graph. It should take self and vertex as arguments. Within the method, print Adding  + vertex.value.
  #After the print statement, modify self.graph_dict so it has a key of the vertexs value pointing to the vertex itself.
  def add_vertex(self, vertex):
    print("Adding",vertex.value)  
    self.graph_dict[vertex.value] = vertex
    
  #Within graph.py, define the .add_edge() method inside of Graph.
  #.add_edge() should take self, from_vertex, and to_vertex as arguments.
  #Print Adding edge from from_vertex.value to to_vertex.value
  #Run the code in script.py to see your code print.
  
  #In the .add_edge() method of graph.py, do the following:
  #Key into self.graph_dict with from_vertex.value
  #Call .add_edge on the dictionary value and pass to_vertex.value as an argument
  #Click over to vertex.py if you need a reminder of how the Vertex version of .add_edge() works.
  #When youre ready, run the code in script.py
  #Check the hint for a solution
  #self.graph_dict[from_vertex.value].add_edge(to_vertex.value)
  
  #In the .add_edge() method of graph.py, if the graph is not directed, do the following:
  #Key into self.graph_dict with to_vertex.value
  #Call .add_edge on the dictionary value and pass from_vertex.value as an argument
  #Run the code in script.py
  #Check the hint for a solution.
  def add_edge(self, from_vertex, to_vertex):
    print("Adding edge from",from_vertex.value,"to",to_vertex.value)
    self.graph_dict[from_vertex.value].add_edge(to_vertex.value)
    if not (self.directed):
      self.graph_dict[to_vertex.value].add_edge(from_vertex.value)
    
grand_central = Vertex("Grand Central Station")

#Uncomment the code to call .add_vertex() on the railway instance and pass grand_central as the argument.

# Uncomment this code after you've defined Graph
railway = Graph()

# Uncomment these lines after you've completed .add_vertex()
print(railway.graph_dict)
railway.add_vertex(grand_central)
print(railway.graph_dict)
