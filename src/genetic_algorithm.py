import random
from typing import List, Tuple, Set, Callable, Optional

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

def initial_population(pop_size: int, n: int) -> List[List[int]]:
  pop = []
  for _ in range(pop_size):
    chrom = [random.randint(0,1) for _ in range(n)]
    if sum(chrom) == 0:
      chrom[random.randrange(n)] = 1
    pop.append(chrom)
  return pop

def crossover(a: List[int], b: List[int]) -> Tuple[List[int], List[int]]:
  point = random.randint(1, len(a) - 2)
  return (
    a[:point] + b[point:],
    b[:point] + a[point:]
  )

def mutate(chrom: List[int], rate: float = 0.05):
  for i in range(len(chrom)):
    if random.random() < rate:
      chrom[i] = 1 - chrom[i]

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
  rng_seed: Optional[int] = None
) -> Tuple[State, float]:
  """
  Binary Genetic Algorithm to maximize subset energy.
  """

  if rng_seed is not None:
    random.seed(rng_seed)

  # Initialize population
  population = initial_population(pop_size, num_items)
  fitness = evaluate_population(population, energy_fn)

  for gen in range(generations):

    total_fitness = sum(max(f, 0.00001) for f in fitness)
    probs = [f / total_fitness for f in fitness]

    new_population = []

    while len(new_population) < pop_size:
      # Parents selections
      parents = random.choices(population, weights=probs, k=2)

      # cross
      if random.random() < crossover_rate:
        child1, child2 = crossover(parents[0], parents[1])
      else:
        child1, child2 = parents[0][:], parents[1][:]

      # Mutation
      mutate(child1, mutation_rate)
      mutate(child2, mutation_rate)

      new_population.append(child1)
      new_population.append(child2)

    population = new_population[:pop_size]
    fitness = evaluate_population(population, energy_fn)

  # Best individual
  best_idx = max(range(len(population)), key=lambda i: fitness[i])
  best_state = chromosome_to_state(population[best_idx])
  best_energy = fitness[best_idx]

  return best_state, best_energy