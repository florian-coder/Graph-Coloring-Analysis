# Project - Graph Coloring

This project implements and evaluates several graph coloring algorithms, including:
- **Brute Force**
- **Backtracking**
- **Greedy**
- **Greedy (Degree Sorted)**
- **DSATUR**

## Archive Contents

### 1. Python Scripts
- `graph_generator.py`: The script responsible for generating the graphs used in the tests.  
                        The graphs are saved in the `generated_graphs` directory.  
                        The generated graphs are created with specific characteristics, because  
                        the algorithms must be tested in multiple situations.

- `graph_benchmark.py`: The script that runs the benchmark of the coloring algorithms on the generated graphs.  
                        This script uses the utilities in `utils/read_graph.py`, which help with  
                        reading data from files, and `algorithms.py`, which contains all algorithms and  
                        is called by this script. The results are saved in the `out` directory and in  
                        the `results.txt` and `benchmark.txt` files.

### 2. Makefile
- Automates the entire process:
  - Cleans the `generated_graphs` and `out` directories.
  - Runs the generation and benchmark scripts.

- Available commands:
  ```bash
  make        # Runs the entire pipeline (clean -> generate -> benchmark)
  make help   # Displays this README with all instructions
  make generate  # Runs only graph generation
  make benchmark # Runs only the benchmark
  make clean_directories  # Cleans the generated_graphs, out, charts directories
  make clean   # Deletes temporary files

### 3. Results
The result of each test from generated_graphs will be found in out.
It will have the same path as in generated_graphs and will contain the output, namely
the number of colors and the assigned colors. In results.txt, the benchmark results
for each algorithm are saved, and in benchmark.txt, the averages achieved by each
algorithm for correctness, ops/sec, and runtime are saved.
Additionally, the plots for each heuristic are saved in the charts folder.
