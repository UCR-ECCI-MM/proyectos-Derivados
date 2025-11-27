import math
import random
from typing import Sequence, Optional, Set, Callable

def min_max_normalize(value: float, vmin: float, vmax: float) -> float:
  """
  Apply min-max normalization to map value into [0, 1].

  :param value: Raw value.
  :param vmin: Global minimum.
  :param vmax: Global maximum.
  :return: Normalized value in [0, 1].
  """
  if vmax <= vmin:
    return 0.0
  return (value - vmin) / (vmax - vmin)

def safe_min(values: Sequence[float]) -> float:
    return min(values) if values else 0.0

def safe_max(values: Sequence[float]) -> float:
    return max(values) if values else 1.0

def safe_log10(x: float, epsilon: float = 1e-6) -> float:
  """
  base-10 logarithm using a small epsilon floor to avoid
  domain errors for non-positive inputs.

  :param x: Value to log.
  :param epsilon: Minimum allowed positive value.
  :return: log10(max(x, epsilon)).
  """
  return math.log10(max(x, epsilon))

State = Set[int]

def subset_energy(state: Set[int], h_values: Sequence[float]) -> float:
  if not state:
    return float("-inf")
  return sum(h_values[i] for i in state) / len(state)

def random_initial_subset(
  num_items: int,
  min_size: int = 1,
  max_size: Optional[int] = None) -> State:
  """
  Generate a random initial subset of indices.

  :param num_items: Total number of items available.
  :param min_size: Minimum subset size.
  :param max_size: Maximum subset size; if None, uses num_items.
  :return: Random subset of indices.
  """
  if max_size is None:
    max_size = num_items
  min_size = max(0, min_size)
  max_size = max(min_size, max_size)
  size = random.randint(min_size, min(max_size, num_items))
  indices = list(range(num_items))
  random.shuffle(indices)
  return set(indices[:size])

def subset_neighbor_cap(
        state: Set[int],
        num_items: int,
        min_size: int,
        max_size: int
) -> Set[int]:
  """
  Always produces a valid neighbor within constraints.
  """

  new_state = set(state)

  can_add = len(new_state) < max_size
  can_remove = len(new_state) > min_size

  # Choose whether to add or remove
  if can_add and can_remove:
    add_mode = random.random() < 0.5
  elif can_add:
    add_mode = True
  elif can_remove:
    add_mode = False
  else:
    return new_state

  if add_mode:
    available = [i for i in range(num_items) if i not in new_state]
    if available:
      new_state.add(random.choice(available))
    return new_state

  else:
    new_state.remove(random.choice(tuple(new_state)))
    return new_state
