import math
import random
from typing import Optional, Tuple, Callable, Set

State = Set[int]

def simulated_annealing(
    initial_state: State,
    energy_fn: Callable[[State], float],
    neighbor_fn: Callable[[State], State],
    initial_temp: float = 1.0,
    final_temp: float = 1e-3,
    alpha: float = 0.99,
    max_steps: int = 10_000,
    rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """

  :param initial_state: Starting solution (subset of indices).
  :param energy_fn: Function that evaluates a solution (higher is better).
  :param neighbor_fn: Function that generates a neighbor solution.
  :param initial_temp: Initial temperature T0.
  :param final_temp: Final temperature threshold to stop the process.
  :param alpha: Cooling rate; T <- alpha * T.
  :param max_steps: Maximum number of iterations.
  :param rng_seed: Optional random seed for reproducibility.
  :return: (best_state, best_energy) found during the search.
  """
  if rng_seed is not None:
    random.seed(rng_seed)

  current_state = set(initial_state)
  current_energy = energy_fn(current_state)

  best_state = set(current_state)
  best_energy = current_energy

  T = initial_temp
  steps = 0

  while T > final_temp and steps < max_steps:
    candidate_state = neighbor_fn(current_state)
    candidate_energy = energy_fn(candidate_state)
    delta = candidate_energy - current_energy

    if delta >= 0:
      # Siempre aceptar mejores
      current_state = candidate_state
      current_energy = candidate_energy
    else:
      # Accept peores solutions
      acceptance_prob = math.exp(delta / T)
      if random.random() < acceptance_prob:
        current_state = candidate_state
        current_energy = candidate_energy

    # Check the best state
    if current_energy > best_energy:
      best_energy = current_energy
      best_state = set(current_state)

    # Bajar valor de T
    T *= alpha
    steps += 1

  return best_state, best_energy
