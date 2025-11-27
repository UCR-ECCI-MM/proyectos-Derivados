from typing import Tuple
from .general import safe_log10

def silica_geothermometer(si: float) -> float:
  """
  Compute the Silica (Quartz) geothermometer temperature.

  Equation:
      T_Si = [1309 / (5.19 - log10(Si))] - 273.15

  :param si: Silica concentration
  :return: Reservoir temperature °C.
  """
  log_si = safe_log10(si)

  denominator = (5.19 - log_si)
  # Safety floor
  if denominator == 0.0:
    denominator = 1e-6

  # Compute T_Si
  t_si = 1309.0 / denominator - 273.15
  return t_si

def nak_geothermometer(na: float, k: float) -> float:
  """
  Compute the Na-K geothermometer temperature.

  Equation:
      T_NaK = [1217 / (log10(Na/K) + 1.483)] - 273.15

  :param na: Sodium concentration.
  :param k: Potassium concentration.
  :return: Reservoir temperature °C.
  """
  # Ratio Na/K
  ratio = na / max(k, 1e-6)
  log_ratio = safe_log10(ratio)

  denominator = log_ratio + 1.483
  # Safety floor
  if denominator == 0.0:
    denominator = 1e-6

  t_nak = 1217.0 / denominator - 273.15
  return t_nak

def nakca_geothermometer(na: float, k: float, ca: float) -> float:
  """
  Compute the Na-K-Ca geothermometer temperature.

  Equation:
      T_NaKCa = [1647 / (log10(Na/K) + β * log10(Ca/Na) + 2.24)] - 273.15

  β (beta factor):
      - β = 4/3 if T_NaK < 100°C
      - β = 1/3 if T_NaK >= 100°C

  :param na: Sodium concentration.
  :param k: Potassium concentration.
  :param ca: Calcium concentration.
  :return: Reservoir temperature °C.
  """
  # Na/K temperature
  t_nak = nak_geothermometer(na, k)

  # β factor
  beta = 4.0 / 3.0 if t_nak < 100.0 else 1.0 / 3.0

  # Required ratios
  ratio_nak = na / max(k, 1e-6)
  ratio_ca_na = ca / max(na, 1e-6)

  log_nak = safe_log10(ratio_nak)
  log_ca_na = safe_log10(ratio_ca_na)

  denominator = log_nak + beta * log_ca_na + 2.24
  if denominator == 0.0:
    denominator = 1e-6

  t_nakca = 1647.0 / denominator - 273.15
  return t_nakca

def compute_geothermometers(si: float, na: float, k: float, ca: float)\
        -> Tuple[float, float, float]:
  """
  Wrapper that computes the three geothermometers.

  :return: (T_Si, T_NaK, T_NaKCa)
  """
  t_si = silica_geothermometer(si)
  t_nak = nak_geothermometer(na, k)
  t_nakca = nakca_geothermometer(na, k, ca)
  return t_si, t_nak, t_nakca
