

class Node:

    def __init__(self, name):
        self.name = name
        self.connected_nodes = []

    def add_connection(self, node, cost, dag=True):
        assert isinstance(node, Node)
        self.connected_nodes.append((node, cost))
        if not dag:
            if self not in [n for n, c in node.connected_nodes]:
                node.add_connection(self, -cost)

    def __repr__(self):
        return "Node: \"{}\", BF: {}".format(self.name, len(self.connected_nodes))


if __name__ == '__main__':
    n1 = Node("Node 1")
    n2 = Node("Node 2")
    n1.add_connection(n2, 3)

    print(n1)
    print(n2)
