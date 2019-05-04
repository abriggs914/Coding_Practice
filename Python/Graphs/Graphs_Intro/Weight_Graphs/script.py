from graph import Graph
from vertex import Vertex

railway = Graph()

callan = Vertex('callan')
peel = Vertex('peel')
harwick = Vertex('harwick')

railway.add_vertex(callan)
railway.add_vertex(peel)
railway.add_vertex(harwick)

# Uncomment the code below when you're ready to test

railway.add_edge(callan, peel, 12)
railway.add_edge(harwick, callan, 7)
railway.add_edge(peel, harwick)

print(callan.edges)
print(harwick.edges)
print(peel.edges)
