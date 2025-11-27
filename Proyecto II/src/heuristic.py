import math
from typing import Tuple, List, Sequence

from .functions.scores import temperature_score, geochemical_score, \
  spatial_score
from .functions.spatial import idw_interpolation_at_point, \
    find_k_nearest_indices
from .structures import Manifestation, NormalizationStats

def objective_function(
  temp: float,
  cond: float,
  cl: float,
  si: float,
  na: float,
  k: float,
  ca: float,
  stats: NormalizationStats,
  weights: Tuple[float, float, float] = (1.0, 1.0, 1.0)
) -> float:
  """
  :param temp: Temperature.
  :param cond: Conductivity.
  :param cl: Chloride.
  :param si: Silica concentration.
  :param na: Sodium concentration.
  :param k: Potassium concentration.
  :param ca: Calcium concentration.
  :param stats: Global normalization statistics.
  :param weights for the temperature, geochemical and spatial components.
  :return: Geothermal score value Gs(i).
  """
  w1, w2, w3 = weights

  t_score = temperature_score(temp, stats)
  g_score = geochemical_score(si, na, k, ca, stats)
  s_score = spatial_score(temp, cond, cl, stats)

  return w1 * t_score + w2 * g_score + w3 * s_score

def geo_heuristic_value(
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

  # Recorrido de subconjuntos
  for mask in range(1, 1 << m):
    subset_neighbors: List[Manifestation] = []
    for bit in range(m):
      if mask & (1 << bit):
        subset_neighbors.append(neighbors[bit])

    interp = idw_interpolation_at_point(
      target, subset_neighbors,
      props, power=idw_power
    )

    f_s = objective_function(
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

    # Exponential
    h_s = math.exp(beta_heuristic * f_s)
    total_h += h_s
    subset_count += 1

  if subset_count == 0:
    return 0.0

  return total_h / float(subset_count)

def heuristic_weigths(
  manifestations: Sequence[Manifestation],
  stats: NormalizationStats,
  weights: Tuple[float, float, float] = (1.0, 1.0, 1.0),
  beta_heuristic: float = 2.0,
  idw_power: float = 2.0) -> List[float]:
  """
  Compute the Heuristic for all manifestations in the dataset.

  :param manifestations: List of manifestations.
  :param stats: Normalization statistics.
  :param weights: Weights for F(i).
  :param beta_heuristic: β parameter for exponential transform.
  :param idw_power: IDW power parameter.
  :return: List H where H[i] = heuristic for manifestation i.
  """
  h_values: List[float] = []
  for i in range(len(manifestations)):
    h_i = geo_heuristic_value(
      manifestations, i, stats,
      weights=weights,
      beta_heuristic=beta_heuristic,
      idw_power=idw_power
    )
    h_values.append(h_i)
  return h_values
