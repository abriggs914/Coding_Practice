from utility import *


class Node:

    def __init__(self, id_num, name):
        self.id_num = id_num
        self.name = name
        self.connected_nodes = []

    def add_connection(self, node, cost, dag=True, ret_cost="negative"):
        assert isinstance(node, Node)
        valid = ["negative", "inverse", "same"]
        if not isinstance(ret_cost, list):
            ret_cost = [ret_cost]
        new_rc = []
        for rc in ret_cost:
            if rc.lower() not in valid:
                rc = "negative"
            new_rc.append(rc)
        ret_cost = new_rc
        self.connected_nodes.append((node, cost))
        if not dag:
            if self not in [n for n, c in node.connected_nodes]:
                if "negative" in ret_cost:
                    cost = -cost
                if "inverse" in ret_cost:
                    cost = 1 / cost

                node.add_connection(self, cost)

    def __eq__(self, other):
        return isinstance(other, Node) and self.id_num == other.id_num

    def __lt__(self, other):
        return isinstance(other, Node) and self.id_num < other.id_num

    def __key(self):
        return tuple(v for k, v in sorted(self.__dict__.items()))

    def __repr__(self):
        return "Node: \"{}\", BF: {}".format(self.name, len(self.connected_nodes))


class Graph:

    def __init__(self):
        self.nodes = []

    def __getitem__(self, key):
        for n in self.nodes:
            if n == key:
                return key

    def add_node(self, id_num, name=None):
        if name is None:
            assert isinstance(id_num, Node)
            n = id_num
        else:
            assert isnumber(id_num) and isinstance(name, str)
            n = Node(id_num, name)
        self.nodes.append(n)

    def convert(self, start, end):
        def helper(nodes_to_check, target, path, checked):
            print("nodes_to_check: {}, target: {}, path: {}, checked: {}".format(nodes_to_check, target, path, checked))
            to_add = []
            for n in nodes_to_check:
                print("n: ", n)
                if n == target:
                    print("Found target")
                    return path + [target]
                else:
                    if n not in checked:
                        to_add = to_add + [n for n, c in n.connected_nodes]
            print("to_add: ", to_add)
            return path + helper(to_add, target, path, checked + nodes_to_check)
        path = helper([start], end, [], [])
        print("Calculated Path:", path)

    def bfs(self, graph, start_vertex, target_value):
        path = [start_vertex]
        vertex_and_path = [start_vertex, path]
        bfs_queue = [vertex_and_path]
        visited = set()
        while bfs_queue:
            current_vertex, path = bfs_queue.pop(0)
            visited.add(current_vertex)
            for neighbor in graph[current_vertex]:
                if neighbor not in visited:
                    if neighbor is target_value:
                        return path + [neighbor]
                    else:
                        bfs_queue.append([neighbor, path + [neighbor]])



if __name__ == '__main__':
    n1 = Node(1, "Node 1")
    n2 = Node(2, "Node 2")
    n3 = Node(3, "Node 3")
    n1.add_connection(n2, 3, 0, ["negative", "inverse"])
    n2.add_connection(n3, 8)
    g = Graph()
    g.add_node(n1)
    g.add_node(n2)
    g.add_node(n3)

    print(n1)
    print(n2)

    g.convert(n1, n2)
    g.convert(n1, n3)
