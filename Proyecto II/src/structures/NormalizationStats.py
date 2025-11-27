from dataclasses import dataclass

@dataclass
class NormalizationStats:
  """
  Holds global min/max values used for min-max normalization of
  physical and geochemical properties and average geothermometer.
  """
  temp_min: float
  temp_max: float
  cond_min: float
  cond_max: float
  cl_min: float
  cl_max: float
  tavg_min: float
  tavg_max: float