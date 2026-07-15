import random
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

GRID_SIZE = 15


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


DIRECTION_ORDER = [Direction.UP, Direction.RIGHT, Direction.DOWN, Direction.LEFT]


@dataclass
class SnakeEnvironment:
    grid_size: int = GRID_SIZE
    snake: List[Tuple[int, int]] = field(default_factory=list)
    direction: Direction = Direction.RIGHT
    apple: Tuple[int, int] = (0, 0)
    score: int = 0
    steps_without_apple: int = 0
    game_over: bool = False

    def reset(self):
        mid = self.grid_size // 2
        self.snake = [(mid, mid), (mid - 1, mid), (mid - 2, mid)]
        self.direction = Direction.RIGHT
        self.score = 0
        self.steps_without_apple = 0
        self.game_over = False
        self.apple = self._spawn_apple()
        return self.get_state()

    def _spawn_apple(self) -> Tuple[int, int]:
        while True:
            pos = (
                random.randint(0, self.grid_size - 1),
                random.randint(0, self.grid_size - 1),
            )
            if pos not in self.snake:
                return pos

    def _rotate(self, current: Direction, action: str) -> Direction:
        idx = DIRECTION_ORDER.index(current)
        if action == "left":
            idx = (idx - 1) % 4
        elif action == "right":
            idx = (idx + 1) % 4
        return DIRECTION_ORDER[idx]

    def step(self, action: str):
        if self.game_over:
            return self.get_state(), 0.0, True

        self.direction = self._rotate(self.direction, action)
        dx, dy = self.direction.value
        head_x, head_y = self.snake[0]
        new_head = (head_x + dx, head_y + dy)

        hit_wall = not (
            0 <= new_head[0] < self.grid_size and 0 <= new_head[1] < self.grid_size
        )
        hit_self = new_head in self.snake

        if hit_wall or hit_self:
            self.game_over = True
            return self.get_state(), -10.0, True

        self.snake.insert(0, new_head)

        if new_head == self.apple:
            self.score += 10
            self.apple = self._spawn_apple()
            self.steps_without_apple = 0
            reward = 10.0
        else:
            self.snake.pop()
            self.steps_without_apple += 1
            reward = -0.1

        if self.steps_without_apple > self.grid_size * self.grid_size * 2:
            self.game_over = True
            reward = -10.0

        return self.get_state(), reward, self.game_over

    def get_state(self):
        return {
            "snake": [{"x": x, "y": y} for x, y in self.snake],
            "apple": {"x": self.apple[0], "y": self.apple[1]},
            "direction": self.direction.name,
            "score": self.score,
            "level": self.score // 50 + 1,
            "stars": min(self.score // 50 + 1, 3),
            "gameOver": self.game_over,
        }

    def get_agent_observation(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction.value

        def is_collision(pos: Tuple[int, int]) -> bool:
            x, y = pos
            return (
                x < 0
                or x >= self.grid_size
                or y < 0
                or y >= self.grid_size
                or (x, y) in self.snake
            )

        left_dir = self._rotate(self.direction, "left")
        right_dir = self._rotate(self.direction, "right")

        straight_pos = (head_x + dx, head_y + dy)
        left_pos = (head_x + left_dir.value[0], head_y + left_dir.value[1])
        right_pos = (head_x + right_dir.value[0], head_y + right_dir.value[1])

        apple_x, apple_y = self.apple

        return (
            is_collision(straight_pos),
            is_collision(left_pos),
            is_collision(right_pos),
            self.direction == Direction.UP,
            self.direction == Direction.DOWN,
            self.direction == Direction.LEFT,
            self.direction == Direction.RIGHT,
            apple_x < head_x,
            apple_x > head_x,
            apple_y < head_y,
            apple_y > head_y,
        )