import random
from typing import List, Tuple, Set, Callable, Optional

from .functions.general import subset_neighbor_cap

State = Set[int]

def chromosome_to_state(chrom: List[int]) -> State:
  state = {i for i, bit in enumerate(chrom) if bit == 1}
  if not state:
    # force 1 index
    state = {random.randrange(len(chrom))}
  return state

def state_to_chromosome(state: State, n: int) -> List[int]:
  chrom = [0] * n
  for i in state:
    chrom[i] = 1
  return chrom

def initial_population(pop_size: int, n: int, min_size: int, max_size: int):
  pop = []
  for _ in range(pop_size):
    size = random.randint(min_size, max_size)
    chrom = [0] * n
    ones = random.sample(range(n), k=size)
    for i in ones:
      chrom[i] = 1
    pop.append(chrom)
  return pop

def crossover(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
  point = random.randint(1, len(a) - 2)
  return (
    a[:point] + b[point:],
    b[:point] + a[point:]
  )

def mutate_chromosome(
    chrom: List[int],
    mutation_rate: float,
    num_items: int,
    min_size: int,
    max_size: int
) -> List[int]:

  # Probability of mutation
  if random.random() > mutation_rate:
    return chrom

  state = chromosome_to_state(chrom)

  # neighbor mutation
  mutated_state = subset_neighbor_cap(
    state,
    num_items=num_items,
    min_size=min_size,
    max_size=max_size
  )

  return state_to_chromosome(mutated_state, num_items)

def evaluate_population(
  population: List[List[int]],
  energy_fn: Callable[[State], float]
) -> List[float]:
  return [energy_fn(chromosome_to_state(ch)) for ch in population]

def genetic_algorithm(
  num_items: int,
  energy_fn: Callable[[State], float],
  pop_size: int = 40,
  generations: int = 200,
  crossover_rate: float = 0.7,
  mutation_rate: float = 0.05,
  min_size: int = 1,
  max_size: int = 5,
  rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """
  Binary Genetic Algorithm to maximize subset energy.
  """

  if rng_seed is not None:
    random.seed(rng_seed)

    # Init population
  population = initial_population(pop_size, num_items, min_size, max_size)
  fitness = evaluate_population(population, energy_fn)

  for gen in range(generations):

    total_fitness = sum(max(f, 0.00001) for f in fitness)
    probs = [f / total_fitness for f in fitness]

    new_population = []

    while len(new_population) < pop_size:
      parents = random.choices(population, weights=probs, k=2)

      if random.random() < crossover_rate:
        child1, child2 = crossover(parents[0], parents[1])
      else:
        child1, child2 = parents[0][:], parents[1][:]

      # mutation
      child1 = mutate_chromosome(child1, mutation_rate,
                                 num_items, min_size, max_size)

      child2 = mutate_chromosome(child2, mutation_rate,
                                 num_items, min_size, max_size)

      new_population.append(child1)
      new_population.append(child2)

    population = new_population[:pop_size]
    fitness = evaluate_population(population, energy_fn)

  # Best solution
  best_idx = max(range(len(population)), key=lambda i: fitness[i])
  best_state = chromosome_to_state(population[best_idx])
  best_energy = fitness[best_idx]

  return best_state, best_energy