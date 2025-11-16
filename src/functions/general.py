import math
from typing import Sequence

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