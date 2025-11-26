import csv
import time
from typing import List
import statistics

import matplotlib.pyplot as plt

from src.heuristic import heuristic_weigths
from src.structures.Manifestation import Manifestation
from src.structures.NormalizationStats import NormalizationStats

from src.functions.general import safe_min, safe_max, subset_energy, \
 random_initial_subset, subset_neighbor_cap
from src.functions.geothermometers import compute_geothermometers

from src.simulated_annealing import simulated_annealing
from src.genetic_algorithm import genetic_algorithm
from src.tabu_search import tabu_search


def load_manifestations_from_csv(path: str) -> List[Manifestation]:
  lst = []
  with open(path, newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
      lst.append(
        Manifestation(
          mid=row["id"],
          x=float(row["coord_x"]),
          y=float(row["coord_y"]),
          temp=float(row["temp"]),
          cond=float(row["cond"]),
          cl=float(row["Cl"]),
          ca=float(row["Ca"]),
          si=float(row["Si"]),
          na=float(row["Na"]),
          k=float(row["K"]),
        )
      )
  return lst

def compute_normalization_stats(manifestations: List[Manifestation]) -> NormalizationStats:
  temps = [m.temp for m in manifestations]
  conds = [m.cond for m in manifestations]
  cls = [m.cl for m in manifestations]

  t_avgs = []
  for m in manifestations:
    t_si, t_nak, t_nakca = compute_geothermometers(m.si, m.na, m.k, m.ca)
    t_avgs.append((t_si + t_nak + t_nakca) / 3.0)

  return NormalizationStats(
    temp_min=safe_min(temps),
    temp_max=safe_max(temps),
    cond_min=safe_min(conds),
    cond_max=safe_max(conds),
    cl_min=safe_min(cls),
    cl_max=safe_max(cls),
    tavg_min=safe_min(t_avgs),
    tavg_max=safe_max(t_avgs)
  )


def run_benchmark_single(manifestations: List[Manifestation], method: str):
  stats = compute_normalization_stats(manifestations)
  h_vals = heuristic_weigths(manifestations, stats)
  num_items = len(manifestations)

  energy = lambda s: subset_energy(s, h_vals)
  init_state = random_initial_subset(num_items, min_size=1)

  start = time.time()

  if method == "SA":
    best_state, best_energy = simulated_annealing(
      initial_state=init_state,
      energy_fn=energy,
      neighbor_fn=lambda s: subset_neighbor_cap(s, num_items, 1, 5),
      initial_temp=1.0,
      final_temp=1e-3,
      alpha=0.99,
      max_steps=4000,
      rng_seed=None
    )

  elif method == "TS":
    best_state, best_energy = tabu_search(
      num_items=num_items,
      h_values=h_vals,
      energy_fn=energy,
      tabu_tenure=10,
      max_iterations=500,
      min_size=1,
      max_size=5,
      rng_seed=None
    )

  elif method == "GA":
    best_state, best_energy = genetic_algorithm(
      num_items=num_items,
      energy_fn=energy,
      pop_size=40,
      generations=150,
      mutation_rate=0.05,
      rng_seed=None
    )

  else:
    raise ValueError("Unknown method " + method)

  end = time.time()
  elapsed = end - start

  best_indices = sorted(list(best_state))

  return elapsed, best_energy, len(best_indices), best_indices

def print_run_summary(method, n, times, energies, sizes):
  print("\n=======================================================")
  print(f"   SUMMARY — {method} on N={n} (50 runs)")
  print("=======================================================\n")
  print(f"   Time:   mean={statistics.mean(times):.4f}s   std={statistics.stdev(times):.4f}")
  print(f"   Energy: mean={statistics.mean(energies):.4f}  std={statistics.stdev(energies):.4f}")
  print(f"   Size:   mean={statistics.mean(sizes):.2f}     std={statistics.stdev(sizes):.2f}")
  print(f"   Best Energy:  {max(energies):.4f}")
  print(f"   Worst Energy: {min(energies):.4f}")
  print("-------------------------------------------------------\n")

def main():
  print("\n=== METAHEURISTIC BENCHMARKING — 50 RUNS EACH ===\n")

  all_manifestations = load_manifestations_from_csv("../dataset/dataset_300.csv")
  sizes = [100, 150, 300]
  methods = ["SA", "TS", "GA"]

  # Construccion de diccionarios
  results_time = {m: {n: [] for n in sizes} for m in methods}
  results_energy = {m: {n: [] for n in sizes} for m in methods}
  results_size = {m: {n: [] for n in sizes} for m in methods}

  # Test runs
  for n in sizes:
    subset = all_manifestations[:n]

    print(f"\n==============================")
    print(f"  DATASET SIZE N={n}")
    print("==============================\n")

    for method in methods:
      print(f" → Running 50 runs of {method}...")

      for _ in range(50):
        elapsed, energy, size, best_indices = run_benchmark_single(subset, method)
        results_time[method][n].append(elapsed)
        results_energy[method][n].append(energy)
        results_size[method][n].append(size)

      # Print summary
      print_run_summary(
        method, n,
        results_time[method][n],
        results_energy[method][n],
        results_size[method][n]
      )

  plt.figure(figsize=(14, 5))

  # Media Tiempo
  plt.subplot(1, 3, 1)
  for method in methods:
    means = [statistics.mean(results_time[method][n]) for n in sizes]
    plt.plot(sizes, means, marker="o", label=method)
  plt.title("Media de Tiempo en Ejecución")
  plt.xlabel("Tamaño de muestra")
  plt.ylabel("Segundos")
  plt.legend()

  # Media Energia
  plt.subplot(1, 3, 2)
  for method in methods:
    means = [statistics.mean(results_energy[method][n]) for n in sizes]
    plt.plot(sizes, means, marker="o", label=method)
  plt.title("Media de Energía Encontrada")
  plt.xlabel("Tamaño de muestra")
  plt.ylabel("Energía")
  plt.legend()

  # Media Tamaño
  plt.subplot(1, 3, 3)
  for method in methods:
    means = [statistics.mean(results_size[method][n]) for n in sizes]
    plt.plot(sizes, means, marker="o", label=method)
  plt.title("Media de Tamaño de Solución")
  plt.xlabel("Tamaño de muestra")
  plt.ylabel("Tamaño S.")
  plt.legend()

  plt.tight_layout()
  plt.show()


if __name__ == "__main__":
  main()
