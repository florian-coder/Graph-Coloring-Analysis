import os
import time
import matplotlib.pyplot as plt
from utils.read_graph import read_graph_from_file
from utils.algorithms import run_backtracking, greedy_coloring, degree_sorted_coloring, dsatur_coloring, brute_force_coloring

def benchmark_algorithm(algorithm, graph, *args):
    """
    Benchmark an algorithm: measure execution time and compute OPS/sec.
    """
    start_time = time.time()
    result = algorithm(graph, *args)
    end_time = time.time()

    execution_time = end_time - start_time
    ops_per_second = 1 / execution_time if execution_time > 0 else float('inf')

    return execution_time, ops_per_second, result

def save_output(graph_name, result, output_dir):
    """
    Save the graph coloring result to a .out file.
    """
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{os.path.splitext(graph_name)[0]}.out")
    with open(output_path, "w") as f:
        k = len(set(result))
        f.write(f"{k}\n")
        f.write(" ".join(map(str, result)) + "\n")

ALGORITHMS_AND_FOLDERS = {
    "Brute Force": {
        "algorithm": lambda g: brute_force_coloring(g, num_colors=5),
        "folders": ["BRUTE_FORCE/TREES",
                    "BRUTE_FORCE/SMALL_SPARSE"]
    },
    "Backtracking": {
        "algorithm": lambda g: run_backtracking(g, num_colors=6),
        "folders": ["BACKTRACKING/SPARSE", 
                    "BACKTRACKING/BIPARTITE", 
                    "BACKTRACKING/TREES",
                    "BACKTRACKING/HARD_TESTS"]
    },
    "Greedy": {
        "algorithm": greedy_coloring,
        "folders": ["GREEDY/PLANAR",
                    "GREEDY/HARD_TESTS"]
    },
    "Greedy (Degree Sorted)": {
        "algorithm": degree_sorted_coloring,
        "folders": ["GREEDY_DEGREE/DENSE",
                    "GREEDY_DEGREE/HARD_TESTS"]
    },
    "DSATUR": {
        "algorithm": dsatur_coloring,
        "folders": ["DSATUR/DENSE",
                    "DSATUR/HARD_TESTS"]
    }
}

def generate_graphs_with_normalization(statistics, charts_dir):
    """
    Generate normalized charts for each algorithm.
    """
    os.makedirs(charts_dir, exist_ok=True)

    for alg_name, stats in statistics.items():
        valid_exec_times = stats["exec_times"]
        valid_ops_per_sec = stats["ops_per_sec"]

        if not valid_exec_times or not valid_ops_per_sec:
            print(f"No valid data for algorithm {alg_name}.")
            continue

        min_time = min(valid_exec_times)
        max_time = max(valid_exec_times)
        norm_exec_times = [
            (x - min_time) / (max_time - min_time) if max_time != min_time else 1 for x in valid_exec_times
        ]

        min_ops = min(valid_ops_per_sec)
        max_ops = max(valid_ops_per_sec)
        norm_ops_per_sec = [
            (x - min_ops) / (max_ops - min_ops) if max_ops != min_ops else 1 for x in valid_ops_per_sec
        ]

        plt.figure(figsize=(10, 6))
        plt.plot(norm_exec_times, label="Execution time (normalized)", marker='o')
        plt.title(f"Normalized execution time for {alg_name}")
        plt.xlabel("Valid tests")
        plt.ylabel("Time (normalized)")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(charts_dir, f"{alg_name}_norm_exec_time.png"))
        plt.close()

        plt.figure(figsize=(10, 6))
        plt.plot(norm_ops_per_sec, label="Operations/second (normalized)", marker='o', color='orange')
        plt.title(f"Normalized operations/second for {alg_name}")
        plt.xlabel("Valid tests")
        plt.ylabel("Operations/second (normalized)")
        plt.legend()
        plt.grid()
        plt.savefig(os.path.join(charts_dir, f"{alg_name}_norm_ops_per_sec.png"))
        plt.close()

        print(f"Normalized charts generated for {alg_name}: {charts_dir}/{alg_name}_norm_exec_time.png and {charts_dir}/{alg_name}_norm_ops_per_sec.png")

def test_performance():
    input_dir = "generated_graphs"
    output_dir = "out"
    charts_dir = "charts"
    output_file = "results.txt"

    if not os.path.exists(input_dir):
        print(f"Directory {input_dir} does not exist. Please create it and add graphs.")
        return

    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(charts_dir, exist_ok=True)

    statistics = {alg_name: {"exec_times": [], "ops_per_sec": [], "valid_results": 0, "total_tests": 0}
                  for alg_name in ALGORITHMS_AND_FOLDERS}

    with open(output_file, "w") as f:
        f.write("Results: Graph Coloring Algorithm Tests\n")
        f.write("=" * 50 + "\n\n")

        for alg_name, details in ALGORITHMS_AND_FOLDERS.items():
            algorithm = details["algorithm"]
            folders = details["folders"]
            f.write(f"Algorithm: {alg_name}\n")
            f.write("-" * 50 + "\n")

            for folder in folders:
                folder_path = os.path.join(input_dir, folder)
                output_subfolder = os.path.join(output_dir, folder)

                if not os.path.exists(folder_path):
                    print(f"[Warning]: Directory {folder_path} does not exist. Skipping.")
                    continue

                for file_name in os.listdir(folder_path):
                    if file_name.endswith(".txt"):
                        graph_path = os.path.join(folder_path, file_name)
                        graph = read_graph_from_file(graph_path)

                        try:
                            exec_time, ops_per_sec, result = benchmark_algorithm(algorithm, graph)

                            if result and isinstance(result, list) and len(result) > 0:
                                save_output(file_name, result, output_subfolder)
                                f.write(f"Test: {file_name} (Folder: {folder})\n")
                                f.write(f"Execution time: {exec_time:.6f} seconds\n")
                                f.write(f"Operations/second: {ops_per_sec:.2f}\n")
                                f.write(f"Number of colors: {len(set(result))}\n")
                                f.write(f"Result: {result}\n\n")

                                statistics[alg_name]["exec_times"].append(exec_time)
                                statistics[alg_name]["ops_per_sec"].append(ops_per_sec)
                                statistics[alg_name]["valid_results"] += 1
                            else:
                                f.write(f"Test: {file_name} (Folder: {folder})\n")
                                f.write("Result: No solution found.\n\n")

                            statistics[alg_name]["total_tests"] += 1
                        except Exception as e:
                            statistics[alg_name]["total_tests"] += 1
                            f.write(f"Error on test {file_name}: {str(e)}\n\n")
            f.write("\n")

    generate_graphs_with_normalization(statistics, charts_dir)

    print(f"Results saved to {output_file} and corresponding .out files in {output_dir}.")

if __name__ == "__main__":
    test_performance()
