class Graph:
  def __init__(self, directed = False):
    self.graph_dict = {}
    self.directed = directed

  def add_vertex(self, vertex):
    self.graph_dict[vertex.value] = vertex

  def add_edge(self, from_vertex, to_vertex, weight = 0):
    self.graph_dict[from_vertex.value].add_edge(to_vertex.value, weight)
    if not self.directed:
      self.graph_dict[to_vertex.value].add_edge(from_vertex.value, weight)

  
  #Define .find_path() within the Graph class.
  #It takes self, start_vertex and end_vertex as arguments.
  #Print that you are searching from start_vertex to end_vertex.
  
  #Declare a start variable and assign it to a list containing start_vertex. Well use this list to keep track of the vertices as we search.
  
  #Make a while loop that runs as long as start has elements inside the list.
  #Inside of the while loop, declare a variable current_vertex and set it equal to the first element in start.
  #You should also remove that element from start or the loop wont terminate.
  #current_vertex is the string .value property of a Vertex instance held within Graph. Inside the loop, print current_vertex.
  #Tab over to script.py and run the code.
  
  #Otherwise current_vertex doesnt match, and we need to keep looking.
  #Make a new variable vertex and assign it to the vertex instance by using current_vertex to key into self.graph_dict.
  def find_path(self, start_vertex, end_vertex):
    start = [start_vertex]
    while len(start) > 0:
      current_vertex = start.pop(0)
      if (current_vertex == end_vertex):
        return True
      vertex = self.graph_dict[current_vertex]
      next_vertices = vertex.get_edges()
      start += next_vertices
      print("Visiting " + current_vertex)
      #START CODE HERE
    return False
   
