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

  #When a path exists, return True will exit the loop. When a path does not exist, its a major problem!
  #Well use a dictionary to track which stations weve visited. This will stop our passengers from riding around in circles.
  def find_path(self, start_vertex, end_vertex):
    start = [start_vertex]
    #Replace the commented code near start with a seen variable that begins as an empty dictionary.
    # Checkpoint 1, replace these comments:
    # Use a dictionary to track which
    # vertices we've already visited
    seen = {}
    while len(start) > 0:
      current_vertex = start.pop(0)
      #Replace the commented code after we declare current_vertex. Set the key of the current_vertex as True in our seen dictionary.
      # Checkpoint 2, replace these comments:
      # Update the `seen` variable
      # now that we've visited current_vertex
      seen[current_vertex] = True
      print("Visiting " + current_vertex)
      if current_vertex == end_vertex:
        return True
      else:
        vertex = self.graph_dict[current_vertex]
        next_vertices = vertex.get_edges()
        
        # Filter next_vertices so it only
        # includes vertices NOT IN seen
        
        #Replace the commented code before we add to the start list.
        #Change the next_vertices list, so it only includes vertices that are not in our seen dictionary.
        # Checkpoint 3, uncomment and replace the question marks:
        #next_vertices = [vertex for vertex in next_vertices ???????]
        next_vertices = [vertex for vertex in next_vertices if vertex not in seen]
        start.extend(next_vertices)
        
    return False
