import random
from typing import Set, Sequence, Optional, Tuple, Callable
from src.functions.general import subset_neighbor_cap

State = Set[int]

def tabu_search(
  num_items: int,
  h_values: Sequence[float],
  energy_fn: Callable[[State], float],
  tabu_tenure: int = 10,
  max_iterations: int = 500,
  min_size: int = 1,
  max_size: Optional[int] = 5,
  rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """
  Perform Tabu Search to maximize an energy function over subsets.

  :param num_items: Total number of items.
  :param h_values: Precomputed heuristic values H(i).
  :param energy_fn: Energy evaluation function.
  :param tabu_tenure: Number of iterations an index stays tabu.
  :param max_iterations: Maximum iterations for the search.
  :param min_size: Minimum subset size allowed.
  :param max_size: Maximum subset size allowed.
  :param rng_seed: Optional RNG seed.
  :return: (best_state, best_energy)
  """

  if rng_seed is not None:
    random.seed(rng_seed)

  if max_size is None:
    max_size = num_items

  # initial solution
  current_state: State = set(random.sample(range(num_items), k=min_size))
  current_energy = energy_fn(current_state)

  best_state = set(current_state)
  best_energy = current_energy

  tabu_list = {}

  for iteration in range(max_iterations):

    best_candidate = None
    best_candidate_energy = float("-inf")

    # Generate multiple neighbors and choose the best non-tabu
    for _ in range(25):  # number of neighbors to explore per iteration
      candidate = subset_neighbor_cap(
        current_state,
        num_items=num_items,
        min_size=min_size,
        max_size=max_size
      )

      moves = candidate.symmetric_difference(current_state)

      # Check tabu condition
      is_tabu = any(i in tabu_list for i in moves)

      candidate_energy = energy_fn(candidate)

      # Greedy Candidate
      if is_tabu and candidate_energy <= best_energy:
        continue

      if candidate_energy > best_candidate_energy:
        best_candidate = candidate
        best_candidate_energy = candidate_energy

    # Update tabu list counters
    for i in list(tabu_list.keys()):
      tabu_list[i] -= 1
      if tabu_list[i] <= 0:
        del tabu_list[i]

    # Aplica el movimiento
    if best_candidate is None:
      continue

    # Verificacion de cambios
    changes = best_candidate.symmetric_difference(current_state)
    for i in changes:
      tabu_list[i] = tabu_tenure

    current_state = best_candidate
    current_energy = best_candidate_energy

    # Update best founded
    if current_energy > best_energy:
      best_state = set(current_state)
      best_energy = current_energy

  return best_state, best_energy