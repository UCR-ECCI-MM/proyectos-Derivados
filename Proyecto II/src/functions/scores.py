from typing import Tuple

from .general import min_max_normalize
from .geothermometers import compute_geothermometers
from ..structures import NormalizationStats

def temperature_score(temp: float, stats: NormalizationStats) -> float:
  """
  Compute T_score(i)

  :param temp: Point's temperature.
  :param stats: Normalization statistics.
  :return: Temperature Score.
  """
  return min_max_normalize(temp, stats.temp_min, stats.temp_max)

def geochemical_score(
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

def spatial_score(
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
