import pickle
import random
from pathlib import Path
from typing import Dict, List, Tuple

from core.environment import SnakeEnvironment

ACTIONS = ["straight", "left", "right"]
DEFAULT_TABLE_PATH = Path(__file__).parent / "qtable.pkl"


class QLearningAgent:

    def __init__(
        self,
        table_path: Path = DEFAULT_TABLE_PATH,
        training: bool = False,
        alpha: float = 0.1,       # taxa de aprendizado
        gamma: float = 0.9,       # fator de desconto
        epsilon: float = 1.0,     # taxa de exploração inicial
        epsilon_min: float = 0.01,
        epsilon_decay: float = 0.995,
    ):
        self.table_path = table_path
        self.training = training
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon if training else 0.0
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay

        self.q_table: Dict[Tuple[bool, ...], List[float]] = {}
        self._load()

        self._last_state: Tuple[bool, ...] | None = None
        self._last_action_idx: int | None = None

    def decide(self, env: SnakeEnvironment) -> str:
        return self.get_action(env)

    def get_action(self, env: SnakeEnvironment) -> str:
        state = env.get_agent_observation()
        action_idx = self._choose_action(state)

        if self.training:
            self._last_state = state
            self._last_action_idx = action_idx

        return ACTIONS[action_idx]

    def _choose_action(self, state: Tuple[bool, ...]) -> int:
        # epsilon greedy
        if self.training and random.random() < self.epsilon:
            return random.randrange(len(ACTIONS))
        return int(self._q_values(state).index(max(self._q_values(state))))

    def _q_values(self, state: Tuple[bool, ...]) -> List[float]:
        if state not in self.q_table:
            self.q_table[state] = [0.0, 0.0, 0.0]
        return self.q_table[state]

    def update(
        self,
        state: Tuple[bool, ...],
        action_idx: int,
        reward: float,
        next_state: Tuple[bool, ...],
        done: bool,
    ) -> None:
        # equação de Bellman: Q(s,a) <- Q(s,a) + alpha * (reward + gamma * max_a' Q(s',a') - Q(s,a))
        current_q = self._q_values(state)[action_idx]
        future_q = 0.0 if done else max(self._q_values(next_state))
        target = reward + self.gamma * future_q
        self._q_values(state)[action_idx] = current_q + self.alpha * (target - current_q)

    def decay_epsilon(self) -> None:
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)

    def _load(self) -> None:
        if self.table_path.exists():
            with open(self.table_path, "rb") as f:
                self.q_table = pickle.load(f)

    def save(self) -> None:
        self.table_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.table_path, "wb") as f:
            pickle.dump(self.q_table, f)