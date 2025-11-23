import math
from src.structures import Manifestation

def euclidean_distance(m1: Manifestation, m2: Manifestation) -> float:
  """
  Euclidean distance between two manifestations.

  :param m1: First manifestation.
  :param m2: Second manifestation.
  :return: Euclidean distance.
  """
  dx = m1.x - m2.x
  dy = m1.y - m2.y
  return math.hypot(dx, dy)