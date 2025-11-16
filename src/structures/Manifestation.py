from dataclasses import dataclass

@dataclass
class Manifestation:
  """
  Represents a geothermal manifestation with spatial, thermal
  and ionic properties.
  """
  mid: str
  x: float
  y: float
  temp: float       # Temperature (°C)
  cond: float       # Electrical conductivity
  cl: float         # Chloride
  si: float         # Silica
  na: float         # Sodium
  k: float          # Potassium
  ca: float         # Calcium