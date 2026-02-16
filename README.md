# Proiect - Graph Coloring

Acest proiect implementează și evaluează mai mulți algoritmi pentru colorarea grafurilor, inclusiv:
- **Brute Force**
- **Backtracking**
- **Greedy**
- **Greedy (Degree Sorted)**
- **DSATUR**

## Conținutul Arhivei

### 1. Scripturi Python
- `graph_generator.py`: Scriptul responsabil pentru generarea grafurilor utilizate în teste. 
                        Grafurile sunt salvate în directorul `generated_graphs`.
                        Grafurile generate sunt generate cu o anumita specificitate, deoarece 
                        algoritmii trebuie testati in mai multe situatii.

- `graph_benchmark.py`: Scriptul care rulează benchmark-ul algoritmilor de colorare pe grafurile generate. 
                        Acest script se foloseste de programele din utils:`read_graph.py` care ajuta la 
                        citirea datelor din fisiere, iar `algorithms.py` care contine toti algoritmii si 
                        este apelat in acest script. Rezultatele sunt salvate în directorul `out` și în 
                        fișierele `results.txt` și `benchmark.txt`.  

### 2. Makefile
- Automatizeaza intregul proces:
  - Curata directoarele `generated_graphs` și `out`.
  - Ruleaza scripturile de generare și benchmark.

- Comenzi disponibile:
  ```bash
  make        # Rulează intregul flux (clean -> generate -> benchmark)
  make help   # Afiseaza acest README care are toate instructiunile
  make generate  # Ruleaza doar generarea grafurilor
  make benchmark # Ruleaza doar benchmark-ul
  make clean_directories  # Curata directoarele generated_graphs, out, charts
  make clean   # Sterge fisierele temporare

### 3. Rezultatele
Rezultatul fiecarui test din `generated_graphs` se va afla in `out`. 
Va avea aceeasi cale ca in `generated_graphs` si va fi outputul, adica
numarul de culori si culorile. In `results.txt` se salveaza benchmarkul
fiecarui algoritm, iar in `benchmark.txt` se salveaza averageul pe care
l-a avut fiecare algoritm la corectitudine, ops/sec si timp de rulare.
De asemenea, graficele pt fiecare euristica sunt salvate in folderul charts.

