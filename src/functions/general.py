import math
import random
from typing import Sequence, Optional, Set

from src.structures import Manifestation

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

def subset_energy(
  state: State, h_values: Sequence[float]
) -> float:
  """

  :param state: Set of selected manifestation indices.
  :param h_values: Precomputed heuristic values H(i).
  :return: Energy of the subset. Empty subset gets negative infinity.
  """
  if not state:
    return float("-inf")
  s = sum(h_values[i] for i in state)
  return s / float(len(state))

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

def subset_neighbor(
  state: State,
  num_items: int,
  min_size: int = 1,
  max_size: Optional[int] = None
) -> State:
  """
  Generate a neighbor subset by randomly adding or removing one index.

  :param state: Current subset.
  :param num_items: Total number of available items.
  :param min_size: Minimum allowed subset size.
  :param max_size: Maximum allowed subset size; if None, uses num_items.
  :return: Neighbor subset.
  """
  if max_size is None:
    max_size = num_items

  new_state: State = set(state)

  can_add = len(new_state) < max_size
  can_remove = len(new_state) > min_size

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
  else:
    if new_state:
      new_state.remove(random.choice(tuple(new_state)))

  return new_state
