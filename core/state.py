"""NumPy representation of the game state.

N = config.n_snakes, L = config.length. All floats are float32.
"""

from dataclasses import dataclass

import numpy as np

from core.config import Config

LEFT, STRAIGHT, RIGHT = 0, 1, 2

# Max deviation of the initial heading from the center direction (rad).
_SPAWN_JITTER = 0.2


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


def wrap_angle(angle: np.ndarray) -> np.ndarray:
    """Wrap angles into ``[-pi, pi)``.

    Args:
        angle (np.ndarray): Angles in radians, of any shape.

    Returns:
        np.ndarray: Equivalent angles within ``[-pi, pi)``, same shape.
    """
    return (angle + np.pi) % (2 * np.pi) - np.pi


def new_game(config: Config, seed: int) -> GameState:
    """Create the initial state of a game.

    Only source of randomness in the engine: the same ``seed`` and ``config``
    always give the same state. Heads are spread evenly on a circle, with a random
    global rotation and a random slot assignment to avoid any bias tied to the
    snake index. Each snake faces the center, with a little noise, and its body
    lies in a straight line behind the head.

    Args:
        config (Config): Game parameters.
        seed (int): Seed of the random generator.

    Returns:
        GameState: State at tick 0, with every snake alive and the zone at the
        map radius.
    """
    rng = np.random.default_rng(seed)
    n, length = config.n_snakes, config.length

    slots = rng.permutation(n)
    polar = rng.uniform(-np.pi, np.pi) + 2 * np.pi * slots / n
    spawn_r = config.spawn_radius_ratio * config.map_radius
    heads = spawn_r * np.stack([np.cos(polar), np.sin(polar)], axis=1)

    angle = wrap_angle(polar + np.pi + rng.uniform(-_SPAWN_JITTER, _SPAWN_JITTER, n))

    direction = np.stack([np.cos(angle), np.sin(angle)], axis=1)
    offsets = np.arange(length) * config.speed
    body = heads[:, None, :] - offsets[None, :, None] * direction[:, None, :]

    return GameState(
        tick=0,
        body=body.astype(np.float32),
        angle=angle.astype(np.float32),
        alive=np.ones(n, dtype=bool),
        kills=np.zeros(n, dtype=np.int16),
        death_tick=np.full(n, -1, dtype=np.int32),
        killer=np.full(n, -1, dtype=np.int8),
        zone_radius=float(config.map_radius),
    )
