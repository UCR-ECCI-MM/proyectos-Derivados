from typing import Tuple

from src.functions.general import min_max_normalize
from src.functions.geothermometers import compute_geothermometers
from src.structures import NormalizationStats

def compute_temperature_score(temp: float, stats: NormalizationStats) -> float:
  """
  Compute T_score(i)

  :param temp: Point's temperature.
  :param stats: Normalization statistics.
  :return: Normalized temperature score [0, 1].
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
  :param stats: Normalization statistics (including T_avg range).
  :return: Normalized geochemical score in [0, 1].
  """
  t_si, t_nak, t_nakca = compute_geothermometers(si, na, k, ca)
  t_avg = (t_si + t_nak + t_nakca) / 3.0
  return min_max_normalize(t_avg, stats.tavg_min, stats.tavg_max)