import math
from typing import Tuple, List, Sequence, Dict

from src.functions.scores import compute_objective_F
from src.functions.spatial import idw_interpolation_at_point, \
    find_k_nearest_indices
from src.structures import Manifestation, NormalizationStats

def compute_heuristic_H_for_point(
  manifestations: Sequence[Manifestation],
  index: int,
  stats: NormalizationStats,
  weights: Tuple[float, float, float] = (1.0, 1.0, 1.0),
  beta_heuristic: float = 2.0,
  idw_power: float = 2.0
) -> float:
  """
  Compute the exponential heuristic H(i) for a manifestation i.

  :param manifestations: List of manifestations.
  :param index: Index of the target manifestation.
  :param stats: Normalization statistics.
  :param weights: Weights (w1, w2, w3) for F(i).
  :param beta_heuristic: β parameter controlling exponential emphasis.
  :param idw_power: Power parameter for IDW interpolation.
  :return: Heuristic value H(i).
  """
  target = manifestations[index]
  neighbor_indices = find_k_nearest_indices(manifestations, index, k=4)
  neighbors = [manifestations[j] for j in neighbor_indices]

  if not neighbors:
    return 0.0

  # Properties to be interpolated
  props = ["temp", "cond", "cl", "si", "na", "k", "ca"]

  m = len(neighbors)
  total_h = 0.0
  subset_count = 0

  # Go through all the possible subsets
  for mask in range(1, 1 << m):
    subset_neighbors: List[Manifestation] = []
    for bit in range(m):
      if mask & (1 << bit):
        subset_neighbors.append(neighbors[bit])

    interp = idw_interpolation_at_point(target, subset_neighbors, props, power=idw_power)

    f_s = compute_objective_F(
      temp=interp["temp"],
      cond=interp["cond"],
      cl=interp["cl"],
      si=interp["si"],
      na=interp["na"],
      k=interp["k"],
      ca=interp["ca"],
      stats=stats,
      weights=weights
    )

    # Exponential transform
    h_s = math.exp(beta_heuristic * f_s)
    total_h += h_s
    subset_count += 1

  if subset_count == 0:
    return 0.0

  return total_h / float(subset_count)

