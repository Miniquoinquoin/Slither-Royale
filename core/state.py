"""NumPy representation of the game state.

N = config.n_snakes, L = config.length. All floats are float32.
"""

from dataclasses import dataclass

import numpy as np

LEFT, STRAIGHT, RIGHT = 0, 1, 2


@dataclass(slots=True)
class GameState:
    """Full state of a game at a given tick.

    Dead snakes stay in the arrays; ``alive`` is used as a mask.

    Attributes:
        tick (int): Current tick number, 0 at the start of the game.
        body (np.ndarray): Segment positions, float32 of shape [N, L, 2].
            ``body[:, 0]`` is the head.
        angle (np.ndarray): Heading of each snake in radians within
            ``[-pi, pi)``, float32 of shape [N].
        alive (np.ndarray): Snakes still in play, bool of shape [N].
        kills (np.ndarray): Number of eliminations per snake, int16 of shape [N].
        death_tick (np.ndarray): Tick of death, -1 while the snake is alive,
            int32 of shape [N].
        killer (np.ndarray): Index of the snake responsible for the death, -1 if
            none (alive, zone or map border), int8 of shape [N].
        zone_radius (float): Current radius of the play zone, centered on the origin.
    """

    tick: int
    body: np.ndarray
    angle: np.ndarray
    alive: np.ndarray
    kills: np.ndarray
    death_tick: np.ndarray
    killer: np.ndarray
    zone_radius: float

    @property
    def heads(self) -> np.ndarray:
        """Head positions.

        Returns:
            np.ndarray: float32 view of shape [N, 2] on ``body[:, 0]``. Writing to
            it modifies ``body``.
        """
        return self.body[:, 0]

    def copy(self) -> "GameState":
        """Deep copy of the state.

        Returns:
            GameState: New state whose arrays are all independent from the
            original.
        """
        return GameState(
            tick=self.tick,
            body=self.body.copy(),
            angle=self.angle.copy(),
            alive=self.alive.copy(),
            kills=self.kills.copy(),
            death_tick=self.death_tick.copy(),
            killer=self.killer.copy(),
            zone_radius=self.zone_radius,
        )
