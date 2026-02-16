import networkx as nx
import matplotlib.pyplot as plt

def load_graph(filename):
    graph = nx.Graph()
    with open(filename, "r") as f:
        for line in f:
            u, v = map(int, line.split())
            graph.add_edge(u, v)
    return graph

graph = load_graph("generated_graphs/complete_graph_10.txt")
nx.draw(graph, with_labels=True)
plt.show()
