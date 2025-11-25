import math
from typing import Tuple, List, Sequence

from src.functions.scores import temperature_score, geochemical_score, \
  spatial_score
from src.functions.spatial import idw_interpolation_at_point, \
    find_k_nearest_indices
from src.structures import Manifestation, NormalizationStats

def geothermal_score(
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
