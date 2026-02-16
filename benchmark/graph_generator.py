import networkx as nx
import random
import os

def save_graph(graph, directory, filename, seed):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, filename), "w") as f:
        f.write(f"# Seed: {seed}\n")
        f.write(f"{graph.number_of_nodes()} {graph.number_of_edges()}\n")
        for edge in graph.edges():
            f.write(f"{edge[0]} {edge[1]}\n")

def validate_generated_graph(graph, size, is_tree=False, is_bipartite=False):
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()

    if not (1 <= num_nodes <= size):
        return False
    if not (1 <= num_edges <= num_nodes * (num_nodes - 1) // 2):
        return False

    for node in graph.nodes():
        if node < 0 or node >= size:
            return False

    for u, v in graph.edges():
        if u < 0 or u >= size or v < 0 or v >= size:
            return False

    if is_tree and not nx.is_tree(graph):
        return False

    if is_bipartite and not nx.is_bipartite(graph):
        return False

    return True

def generate_and_validate(graph_generator, size, is_tree=False, is_bipartite=False, retries=100):
    """
    Generate a valid graph using the provided function.
    Retry multiple times to find a valid graph.
    """
    for _ in range(retries):
        seed = random.randint(0, int(1e6))
        graph = graph_generator(seed)
        if validate_generated_graph(graph, size, is_tree, is_bipartite):
            return graph, seed
    raise ValueError(f"Could not generate a valid graph after {retries} attempts.")

def generate_sparse_graph(size, seed):
    random.seed(seed)
    return nx.gnm_random_graph(size, random.randint(1, size * 2), seed=seed)

def generate_dense_graph(size, seed):
    random.seed(seed)
    return nx.gnp_random_graph(size, 0.8, seed=seed)

def generate_tree_graph(size, seed):
    random.seed(seed)
    return nx.random_tree(size, seed=seed)

def generate_bipartite_graph(m, n, seed, edge_prob=0.8):
    random.seed(seed)
    edges = []
    for i in range(m):
        for j in range(n):
            if random.random() < edge_prob:
                edges.append((i, m + j))
    graph = nx.Graph()
    graph.add_nodes_from(range(m + n))
    graph.add_edges_from(edges)
    return graph

def generate_complete_graph(size, seed):
    random.seed(seed)
    return nx.complete_graph(size)

def generate_unique_seed(base_seed, category_offset, test_index, params):
    """
    Create a unique seed for each test.
    - base_seed: Global seed for the main category.
    - category_offset: Unique offset for the subcategory (e.g., SMALL_SPARSE).
    - test_index: Index of the current test.
    - params: A dict or tuple with graph parameters (e.g., number of nodes, edges).
    """
    param_hash = hash(tuple(params)) % int(1e6)
    return (base_seed + category_offset + test_index + param_hash) % int(1e6)

def generate_brute_force_tests():
    base_seed = 12345
    base_dir = "generated_graphs/BRUTE_FORCE"
    small_sizes = [5, 6, 7]

    for size in small_sizes:
        for i in range(10):
            seed = generate_unique_seed(base_seed, 1000, i, (size, "sparse"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_sparse_graph(size, seed),
                size
            )
            save_graph(graph, os.path.join(base_dir, "SMALL_SPARSE"), f"small_sparse_{size}_{i}.txt", used_seed)

        for i in range(10):
            seed = generate_unique_seed(base_seed, 3000, i, (size, "tree"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_tree_graph(size, seed),
                size,
                is_tree=True
            )
            save_graph(graph, os.path.join(base_dir, "TREES"), f"tree_{size}_{i}.txt", used_seed)

def generate_backtracking_tests():
    base_seed = 54321
    base_dir = "generated_graphs/BACKTRACKING"
    sizes = [10, 15, 18]

    for size in sizes:
        for i in range(10):
            seed = generate_unique_seed(base_seed, 1000, i, (size, "sparse"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_sparse_graph(size, seed),
                size
            )
            save_graph(graph, os.path.join(base_dir, "SPARSE"), f"sparse_{size}_{i}.txt", used_seed)

        for i in range(10):
            seed = generate_unique_seed(base_seed, 2000, i, (size, "bipartite"))
            m, n = size // 2, size - size // 2
            graph, used_seed = generate_and_validate(
                lambda seed: generate_bipartite_graph(m, n, seed, edge_prob=0.5),
                size,
                is_bipartite=True
            )
            save_graph(graph, os.path.join(base_dir, "BIPARTITE"), f"bipartite_{m}_{n}_{i}.txt", used_seed)

        for i in range(10):
            seed = generate_unique_seed(base_seed, 3000, i, (size, "tree"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_tree_graph(size, seed),
                size,
                is_tree=True
            )
            save_graph(graph, os.path.join(base_dir, "TREES"), f"tree_{size}_{i}.txt", used_seed)
        
        hard_dir = os.path.join(base_dir, "HARD_TESTS")
        sizes_hard = [10, 15]
        for size in sizes_hard:
            for i in range(5):
                seed = generate_unique_seed(base_seed, 5000, i, (size, "dense_cliques"))
                graph, used_seed = generate_and_validate(
                    lambda seed: nx.complete_graph(size),
                    size
                )
                save_graph(graph, hard_dir, f"dense_cliques_{size}_{i}.txt", used_seed)

def generate_greedy_tests():
    base_seed = 67890
    base_dir = "generated_graphs/GREEDY"
    sizes = [10, 15, 18, 20]

    for size in sizes:
        for i in range(10):
            seed = generate_unique_seed(base_seed, 1000, i, (size, "tree"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_tree_graph(size, seed),
                size,
                is_tree=True
            )
            save_graph(graph, os.path.join(base_dir, "PLANAR"), f"planar_{size}_{i}.txt", used_seed)

    hard_dir = os.path.join(base_dir, "HARD_TESTS")
    sizes_hard = [20, 30]
    for size in sizes_hard:
        for i in range(5):
            seed = generate_unique_seed(base_seed, 5000, i, (size, "chained_cliques"))
            graph, used_seed = generate_and_validate(
                lambda seed: nx.disjoint_union_all([nx.complete_graph(5) for _ in range(size // 5)]),
                size
            )
            save_graph(graph, hard_dir, f"chained_cliques_{size}_{i}.txt", used_seed)

def generate_star_with_noise(size, seed):
    random.seed(seed)
    G = nx.star_graph(size - 1)
    for _ in range(size // 3):
        u = random.randint(0, size - 1)
        v = random.randint(0, size - 1)
        if u != v:
            G.add_edge(u, v)
    return G

def generate_degree_sorted_greedy_tests():
    base_seed = 13579
    base_dir = "generated_graphs/GREEDY_DEGREE"
    sizes = [10, 15, 18, 20]

    for size in sizes:
        for i in range(10):
            seed = generate_unique_seed(base_seed, 1000, i, (size, "dense"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_dense_graph(size, seed),
                size
            )
            save_graph(graph, os.path.join(base_dir, "DENSE"), f"dense_{size}_{i}.txt", used_seed)

    hard_dir = os.path.join(base_dir, "HARD_TESTS")
    sizes_hard = [20, 30]
    for size in sizes_hard:
        for i in range(5):
            seed = generate_unique_seed(base_seed, 6000, i, (size, "star_with_noise"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_star_with_noise(size, seed),
                size
            )
            save_graph(graph, hard_dir, f"star_with_noise_{size}_{i}.txt", used_seed)


def generate_dsatur_tests():
    base_seed = 24680
    base_dir = "generated_graphs/DSATUR"
    sizes = [10, 15, 18, 20]

    for size in sizes:
        for i in range(10):
            seed = generate_unique_seed(base_seed, 1000, i, (size, "dense"))
            graph, used_seed = generate_and_validate(
                lambda seed: generate_dense_graph(size, seed),
                size
            )
            save_graph(graph, os.path.join(base_dir, "DENSE"), f"dense_{size}_{i}.txt", used_seed)

    hard_dir = os.path.join(base_dir, "HARD_TESTS")
    sizes_hard = [20, 30]
    for size in sizes_hard:
        for i in range(5):
            seed = generate_unique_seed(base_seed, 6000, i, (size, "sparse_high_chromatic"))
            graph, used_seed = generate_and_validate(
                lambda seed: nx.gnm_random_graph(size, size // 2, seed=seed),
                size
            )
            save_graph(graph, hard_dir, f"sparse_high_chromatic_{size}_{i}.txt", used_seed)

if __name__ == "__main__":
    generate_brute_force_tests()
    generate_backtracking_tests()
    generate_greedy_tests()
    generate_degree_sorted_greedy_tests()
    generate_dsatur_tests()
