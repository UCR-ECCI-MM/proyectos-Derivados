import math
from src.structures import Manifestation

def euclidean_distance(m1: Manifestation, m2: Manifestation) -> float:
  dx = m1.x - m2.x
  dy = m1.y - m2.y
  return math.hypot(dx, dy)