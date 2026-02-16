from itertools import product

def brute_force_coloring(graph, num_colors):
    n = len(graph)
    for combination in product(range(num_colors), repeat=n):
        if is_valid_coloring(graph, combination):
            return list(combination)
    return "No solution found."

def is_valid_coloring(graph, colors):
    """
    Check if a color assignment is valid for a graph.
    """
    for node in graph:
        for neighbor in graph[node]:
            if colors[node] == colors[neighbor]: 
                return False
    return True

def is_valid(graph, colors, node, color):
    for neighbor in graph[node]:
        if colors[neighbor] == color:
            return False
    return True

def backtracking(graph, colors, node, num_colors):
    if node == len(graph):
        return True
    for color in range(num_colors):
        if is_valid(graph, colors, node, color):
            colors[node] = color
            if backtracking(graph, colors, node + 1, num_colors):
                return True
            colors[node] = -1
    return False

def run_backtracking(graph, num_colors):
    colors = [-1] * len(graph)
    if backtracking(graph, colors, 0, num_colors):
        return colors
    else:
        return "No solution found."

def greedy_coloring(graph):
    n = len(graph)
    colors = [-1] * n
    for node in range(n):
        used_colors = {colors[neighbor] for neighbor in graph[node] if colors[neighbor] != -1}
        for color in range(n):
            if color not in used_colors:
                colors[node] = color
                break
    return colors

def degree_sorted_coloring(graph):
    n = len(graph)
    nodes = sorted(graph.keys(), key=lambda x: -len(graph[x]))
    colors = [-1] * n
    for node in nodes:
        used_colors = {colors[neighbor] for neighbor in graph[node] if colors[neighbor] != -1}
        for color in range(n):
            if color not in used_colors:
                colors[node] = color
                break
    return colors

def dsatur_coloring(graph):
    n = len(graph)
    colors = [-1] * n
    saturation = [0] * n
    degrees = [len(graph[node]) for node in range(n)]

    while -1 in colors:
        max_saturation = max(saturation[node] for node in range(n) if colors[node] == -1)
        candidates = [node for node in range(n) if colors[node] == -1 and saturation[node] == max_saturation]
        selected_node = max(candidates, key=lambda x: degrees[x])

        used_colors = {colors[neighbor] for neighbor in graph[selected_node] if colors[neighbor] != -1}
        for color in range(n):
            if color not in used_colors:
                colors[selected_node] = color
                break

        for neighbor in graph[selected_node]:
            if colors[neighbor] == -1:
                saturation[neighbor] += 1

    return colors
