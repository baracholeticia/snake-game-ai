from typing import Callable, List, Tuple

import numpy as np

ACTIONS = ("straight", "left", "right")
N_INPUTS = 11
N_ACTIONS = 3
N_PARAMS = N_INPUTS * N_ACTIONS + N_ACTIONS  

class LinearPolicy:
    """Política linear determinística: observação (11,) -> ação (str)."""

    def __init__(self, params: np.ndarray = None):
        self.params = (
            np.asarray(params, dtype=np.float64)
            if params is not None
            else np.zeros(N_PARAMS)
        )
        assert self.params.shape == (N_PARAMS,), (
            f"esperado vetor de {N_PARAMS} parâmetros, recebi {self.params.shape}"
        )

    @property
    def weights(self) -> np.ndarray:
        return self.params[: N_INPUTS * N_ACTIONS].reshape(N_INPUTS, N_ACTIONS)

    @property
    def bias(self) -> np.ndarray:
        return self.params[N_INPUTS * N_ACTIONS :]

    def act(self, observation) -> str:
        obs = np.asarray(observation, dtype=np.float64)
        scores = obs @ self.weights + self.bias
        return ACTIONS[int(np.argmax(scores))]


class GeneticAgent:
    def __init__(self, policy: LinearPolicy):
        self.policy = policy

    def decide(self, env) -> str:
        observation = env.get_agent_observation()
        return self.policy.act(observation)


def run_episode(
    env,
    agent: GeneticAgent,
    max_idle_factor: int = 100,
    max_steps: int = 5000,
) -> Tuple[int, int]:
    env.reset()
    apples = 0
    steps = 0
    idle_steps = 0
    max_idle = max_idle_factor * max(len(env.snake), 1)

    while not env.game_over and steps < max_steps:
        prev_len = len(env.snake)
        action = agent.decide(env)
        env.step(action)
        steps += 1

        if env.game_over:
            break

        if len(env.snake) > prev_len:
            apples += 1
            idle_steps = 0
            max_idle = max_idle_factor * len(env.snake)
        else:
            idle_steps += 1
            if idle_steps > max_idle:
                break

    return apples, steps


def fitness(apples: int, steps: int) -> float:
    return apples * 5000 + steps


class GeneticAlgorithm:
    def __init__(
        self,
        env_factory: Callable[[], object],
        population_size: int = 200,
        elite_fraction: float = 0.1,
        tournament_size: int = 5,
        mutation_rate: float = 0.15,
        mutation_strength: float = 0.5,
        mutation_strength_decay: float = 1.0,
        crossover_rate: float = 0.7,
        episodes_per_individual: int = 3,
        seed: int = None,
    ):

        self.env = env_factory()
        self.population_size = population_size
        self.elite_count = max(1, int(population_size * elite_fraction))
        self.tournament_size = tournament_size
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength
        self.mutation_strength_decay = mutation_strength_decay
        self.crossover_rate = crossover_rate
        self.episodes_per_individual = episodes_per_individual
        self.rng = np.random.default_rng(seed)

        self.population: List[np.ndarray] = [
            self.rng.normal(0.0, 1.0, size=N_PARAMS) for _ in range(population_size)
        ]
        self.best_params = self.population[0].copy()
        self.best_fitness = -np.inf
        self.history: List[dict] = []

    def _evaluate(self, params: np.ndarray) -> float:
        policy = LinearPolicy(params)
        agent = GeneticAgent(policy)
        total = 0.0
        for _ in range(self.episodes_per_individual):
            apples, steps = run_episode(self.env, agent)
            total += fitness(apples, steps)
        return total / self.episodes_per_individual

    def _tournament_select(self, fitnesses: np.ndarray) -> np.ndarray:
        idxs = self.rng.integers(0, self.population_size, size=self.tournament_size)
        best_idx = idxs[np.argmax(fitnesses[idxs])]
        return self.population[best_idx]

    def _crossover(self, parent_a: np.ndarray, parent_b: np.ndarray) -> np.ndarray:
        if self.rng.random() > self.crossover_rate:
            return parent_a.copy()
        mask = self.rng.random(N_PARAMS) < 0.5
        return np.where(mask, parent_a, parent_b)

    def _mutate(self, params: np.ndarray) -> np.ndarray:
        mask = self.rng.random(N_PARAMS) < self.mutation_rate
        noise = self.rng.normal(0.0, self.mutation_strength, size=N_PARAMS)
        params = params.copy()
        params[mask] += noise[mask]
        return params

    def evolve(self, generations: int, verbose: bool = True) -> np.ndarray:
        for gen in range(generations):
            fitnesses = np.array([self._evaluate(ind) for ind in self.population])

            gen_best_idx = int(np.argmax(fitnesses))
            gen_best_fitness = float(fitnesses[gen_best_idx])
            if gen_best_fitness > self.best_fitness:
                self.best_fitness = gen_best_fitness
                self.best_params = self.population[gen_best_idx].copy()

            self.history.append(
                {
                    "generation": gen,
                    "best": gen_best_fitness,
                    "mean": float(fitnesses.mean()),
                    "worst": float(fitnesses.min()),
                }
            )
            if verbose:
                print(
                    f"geração {gen:4d} | melhor={gen_best_fitness:9.1f} "
                    f"média={fitnesses.mean():9.1f} pior={fitnesses.min():9.1f} "
                    f"| melhor histórico={self.best_fitness:9.1f}"
                )

            elite_idxs = np.argsort(fitnesses)[::-1][: self.elite_count]
            new_population = [self.population[i].copy() for i in elite_idxs]

            while len(new_population) < self.population_size:
                parent_a = self._tournament_select(fitnesses)
                parent_b = self._tournament_select(fitnesses)
                child = self._crossover(parent_a, parent_b)
                child = self._mutate(child)
                new_population.append(child)

            self.population = new_population
            self.mutation_strength *= self.mutation_strength_decay

        return self.best_params

    def save_best(self, path: str) -> None:
        np.save(path, self.best_params)

    @staticmethod
    def load_policy(path: str) -> LinearPolicy:
        params = np.load(path)
        return LinearPolicy(params)

if __name__ == "__main__":
    import os
    import sys

    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    from core.environment import SnakeEnvironment

    ga = GeneticAlgorithm(
        env_factory=lambda: SnakeEnvironment(grid_size=15),
        population_size=200,
    )

    best_params = ga.evolve(generations=100)
    ga.save_best("best_snake_policy.npy")

    print(f"\nMelhor fitness encontrado: {ga.best_fitness:.1f}")
    print("Pesos salvos em best_snake_policy.npy")
