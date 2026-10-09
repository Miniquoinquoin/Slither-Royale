"""Snake object to simplify snake interaction

It's all base on GameState
"""

from dataclasses import dataclass
import numpy as np

from typing import Literal

from state import GameState, wrap_angle
from config import Config

@dataclass(frozen=True, slots=True)
class Snake:
    """Snake object to simplify snake interaction

    Attributes:
        state (GameState): GameState object
        index (int): Index of the snake in the GameState arrays
    """
    state: GameState
    index: int
    config : Config

    @property
    def head(self) -> np.ndarray:
        """Head position of the snake

        Returns:
            np.ndarray: float32 view of coordinate, shape [2]
        """
        return self.state.heads[self.index]

    @property
    def angle(self) -> np.float32:
        """Angle of the snake in radian

        Returns:
            np.float32: angle of the snake on the map
        """
        return self.state.angle[self.index]

    @angle.setter
    def angle(self, value : np.float32) -> None:
        self.state.angle[self.index] = value

    def kill(self, killed_snake : "Snake") -> None:
        """Kill the snake 'killed_snake'

        Args:
            killed_snake (Snake): Snake that the current snake as killed
        """
        self.state.killer[killed_snake.index] = self.index
        self.state.kills[self.index] +=1
        self.state.alive[killed_snake.index] = False
        self.state.death_tick[killed_snake.index] = self.state.tick

    def _head_new_position(self) -> np.ndarray:
        """Calculate the next position of the Snake

        Returns:
            np.ndarray: head next position
        """
        
        direction = np.array([np.cos(self.angle), np.sin(self.angle)], dtype=np.float32)
        return self.head + direction * self.config.speed

    def move(self, action : float = 0.0) -> None:
        """Next head position after moving ``speed`` along ``angle``

        Args:
            action (float): angle of the moved snake. 
                ``[-max_turn_rate, max_trun_rate]``. Default 0 (Straight)
        """

        action = np.clip(action, -self.config.max_turn_rate, self.config.max_turn_rate)
        self.angle = wrap_angle(self.angle + action)
        new_head = self._head_new_position()
        self.state.body[:-1] = self.state.body[1:]
        self.state.body[0] = new_head
        
        

