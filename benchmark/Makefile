PYTHON = python3
GENERATOR = graph_generator.py
BENCHMARK = graph_benchmark.py
CHARTS = charts
GENERATED_DIR = generated_graphs
OUT_DIR = out
README = README.md

.PHONY: all
all: clean_directories generate benchmark

.PHONY: clean_directories
clean_directories:
	@echo "Clearing contents of $(GENERATED_DIR) and $(OUT_DIR) for a clean run"
	rm -rf $(GENERATED_DIR)/*
	rm -rf $(OUT_DIR)/*
	rm -rf $(CHARTS)/*

.PHONY: generate
generate:
	@echo "Running the graph generation script"
	$(PYTHON) $(GENERATOR)

.PHONY: benchmark
benchmark:
	@echo "Running the benchmarking script"
	$(PYTHON) $(BENCHMARK)

.PHONY: clean
clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -exec rm -rf {} +
	rm -rf .pytest_cache


.PHONY: help
help:
	@cat $(README)
