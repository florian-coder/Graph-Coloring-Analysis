def read_graph_from_file(file_path):
    graph = {}
    with open(file_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                u, v = map(int, parts)
                if u not in graph:
                    graph[u] = []
                if v not in graph:
                    graph[v] = []
                graph[u].append(v)
                graph[v].append(u)

    for node in range(max(graph.keys()) + 1):
        if node not in graph:
            graph[node] = []

    return graph
