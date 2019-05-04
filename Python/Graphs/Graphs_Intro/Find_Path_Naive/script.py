from graph import Graph
from vertex import Vertex

no_path_exists = True


directed_railway = Graph(True)

callan_station = Vertex('callan')
peel_station = Vertex('peel')
ulfstead_station = Vertex('ulfstead')
harwick_station = Vertex('harwick')

directed_railway.add_vertex(callan_station)
directed_railway.add_vertex(peel_station)
directed_railway.add_vertex(harwick_station)
directed_railway.add_vertex(ulfstead_station)

directed_railway.add_edge(harwick_station, peel_station)
directed_railway.add_edge(peel_station, callan_station)


path_exists = directed_railway.find_path('harwick', 'harwick')
print(path_exists)

#Uncomment for final checkpoint

print("\n\n\nFinding path from harwick to callan\n")
new_path_exists = directed_railway.find_path('harwick', 'callan')
print(new_path_exists)
print("\n\nTrying to find path from harwick to ulfstead\n")
no_path_exists = directed_railway.find_path('harwick', 'ulfstead')
print(no_path_exists)

