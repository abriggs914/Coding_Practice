from vertex import Vertex
from graph import Graph

#######################################################################################################################

graph_1_depiction = """
 
             11
   012345678901
  #############
0 #      A   F
1 #
2 #B   C   D  E
3 # G
4 #   O  H  I
 
"""
 
# create vertices
vertex_A = Vertex(6, 0, "A")
vertex_B = Vertex(0, 2, "B")
vertex_C = Vertex(4, 2, "C")
vertex_D = Vertex(8, 2, "D")
vertex_E = Vertex(11, 2, "E")
vertex_F = Vertex(10, 0, "F")
vertex_G = Vertex(1, 3, "G")
vertex_H = Vertex(6, 4, "H", True)
vertex_I = Vertex(9, 4, "I", True)
vertex_O = Vertex(3, 4, "O", True)

# create graph and set vertices
graph_1 = Graph(graph_1_depiction)

graph_1.add_vertex(vertex_A)
graph_1.add_vertex(vertex_B)
graph_1.add_vertex(vertex_C)
graph_1.add_vertex(vertex_D)
graph_1.add_vertex(vertex_E)
graph_1.add_vertex(vertex_F)
graph_1.add_vertex(vertex_G)
graph_1.add_vertex(vertex_H)
graph_1.add_vertex(vertex_I)
graph_1.add_vertex(vertex_O)

# add edges between vertices
graph_1.add_edge(vertex_A, vertex_B, 8)
graph_1.add_edge(vertex_A, vertex_C, 3)
graph_1.add_edge(vertex_A, vertex_D, 3)
graph_1.add_edge(vertex_A, vertex_E, 2)
graph_1.add_edge(vertex_C, vertex_H, 3)
graph_1.add_edge(vertex_D, vertex_H, 4)
graph_1.add_edge(vertex_D, vertex_I, 11)
graph_1.add_edge(vertex_H, vertex_O, 5)

#######################################################################################################################