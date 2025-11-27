import math
from ..structures import Manifestation
from typing import Sequence, Dict, List, Tuple

def euclidean_distance(
  m1: Manifestation,
  m2: Manifestation
) -> float:
  """
  Euclidean distance between two manifestations.

  :param m1: First manifestation.
  :param m2: Second manifestation.
  :return: Euclidean distance.
  """
  dx = m1.x - m2.x
  dy = m1.y - m2.y
  return math.hypot(dx, dy)

def idw_interpolation_at_point(
  target: Manifestation,
  neighbors: Sequence[Manifestation],
  properties: Sequence[str],
  power: float = 2.0
) -> Dict[str, float]:
  """
  :param target: Manifestation at which interpolation is evaluated.
  :param neighbors: Neighbor manifestations used in interpolation.
  :param properties: Names of Manifestation fields to interpolate.
  :param power: IDW power parameter k.
  :return: Dictionary mapping property name -> interpolated value.
  """
  # Check for exact coincidence
  for n in neighbors:
    d = euclidean_distance(target, n)
    if d == 0.0:
      # Checks if there's an exact neighbor.
      return {prop: getattr(n, prop) for prop in properties}

  dist_list: List[float] = [euclidean_distance(target, n) for n in neighbors]
  weights: List[float] = []
  for d in dist_list:
    # Safety floor.
    d_safe = max(d, 1e-6)
    w = 1.0 / (d_safe ** power)
    weights.append(w)

  interpolated: Dict[str, float] = {}
  weight_sum = sum(weights)

  # Interpolates each manifestation property.
  for prop in properties:
    num = 0.0
    for w, n in zip(weights, neighbors):
      num += w * getattr(n, prop)
    interpolated[prop] = num / weight_sum if weight_sum != 0.0 else 0.0

  return interpolated

def find_k_nearest_indices(
  manifestations: Sequence[Manifestation],
  index: int,
  k: int = 4
) -> List[int]:
  """
  Find the k nearest manifestations to the indexed manifestation.

  :param manifestations: List of manifestations.
  :param index: Index of the target manifestation.
  :param k: Number of neighbors to return.
  :return: List of neighbor indices.
  """
  target = manifestations[index]
  distances: List[Tuple[float, int]] = []

  for j, m in enumerate(manifestations):
    if j == index:
      continue
    d = euclidean_distance(target, m)
    distances.append((d, j))

  distances.sort(key=lambda x: x[0])
  return [idx for _, idx in distances[:k]]