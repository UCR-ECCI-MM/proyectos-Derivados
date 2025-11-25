import random
from typing import List, Tuple, Set, Sequence, Callable, Optional

State = Set[int]

def chromosome_to_state(chrom: List[int]) -> State:
  return {i for i, bit in enumerate(chrom) if bit == 1}

def state_to_chromosome(state: State, n: int) -> List[int]:
  chrom = [0] * n
  for i in state:
    chrom[i] = 1
  return chrom

def genetic_algorithm(
  num_items: int,
  energy_fn: Callable[[State], float],
  pop_size: int = 40,
  generations: int = 200,
  crossover_rate: float = 0.7,
  mutation_rate: float = 0.05,
  rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """
  Binary Genetic Algorithm to maximize subset energy.
  """