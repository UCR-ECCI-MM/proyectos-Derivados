import random
from typing import Set, Sequence, Optional, Tuple, Callable

State = Set[int]

def tabu_search(
  num_items: int,
  h_values: Sequence[float],
  energy_fn: Callable[[State], float],
  neighbor_fn: Callable[[State], State],
  tabu_tenure: int = 10,
  max_iterations: int = 500,
  min_size: int = 1,
  max_size: Optional[int] = None,
  rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """
  Perform Tabu Search to maximize an energy function over subsets.

  :param num_items: Total number of items.
  :param h_values: Precomputed heuristic values H(i).
  :param energy_fn: Energy evaluation function.
  :param neighbor_fn: Function that generates neighbor subsets.
  :param tabu_tenure: Number of iterations an index stays tabu.
  :param max_iterations: Maximum iterations for the search.
  :param min_size: Minimum subset size allowed.
  :param max_size: Maximum subset size allowed.
  :param rng_seed: Optional RNG seed.
  :return: (best_state, best_energy)
  """