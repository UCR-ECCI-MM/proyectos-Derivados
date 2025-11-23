from typing import Tuple

from src.functions.general import min_max_normalize
from src.functions.geothermometers import compute_geothermometers
from src.structures import NormalizationStats

def compute_temperature_score(temp: float, stats: NormalizationStats) -> float:
  """
  Compute T_score(i)

  :param temp: Point's temperature.
  :param stats: Normalization statistics.
  :return: Temperature Score.
  """
  return min_max_normalize(temp, stats.temp_min, stats.temp_max)

def compute_geochemical_score(
  si: float,
  na: float,
  k: float,
  ca: float,
  stats: NormalizationStats
) -> float:
  """
  Compute G_score(i)

  :param si: Silica concentration.
  :param na: Sodium concentration.
  :param k: Potassium concentration.
  :param ca: Calcium concentration.
  :param stats: Normalization statistics.
  :return: Geochemical Score.
  """
  t_si, t_nak, t_nakca = compute_geothermometers(si, na, k, ca)
  t_avg = (t_si + t_nak + t_nakca) / 3.0
  return min_max_normalize(t_avg, stats.tavg_min, stats.tavg_max)

def compute_spatial_score(
  temp_interp: float,
  cond_interp: float,
  cl_interp: float,
  stats: NormalizationStats
) -> float:
  """
  Compute S_score(i)

  :param temp_interp: Interpolated temperature.
  :param cond_interp: Interpolated conductivity.
  :param cl_interp: Interpolated chloride.
  :param stats: Normalization statistics.
  :return: Spatial Score.
  """
  t_norm = min_max_normalize(temp_interp, stats.temp_min, stats.temp_max)
  cond_norm = min_max_normalize(cond_interp, stats.cond_min, stats.cond_max)
  cl_norm = min_max_normalize(cl_interp, stats.cl_min, stats.cl_max)
  return (t_norm + cond_norm + cl_norm) / 3.0

def compute_objective_F(
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
  :return: Objective value F(i).
  """
  w1, w2, w3 = weights

  t_score = compute_temperature_score(temp, stats)
  g_score = compute_geochemical_score(si, na, k, ca, stats)
  s_score = compute_spatial_score(temp, cond, cl, stats)

  return w1 * t_score + w2 * g_score + w3 * s_score