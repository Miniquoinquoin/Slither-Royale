"""Game runner"""

import numpy as np

from core.config import Config
from core.state import GameState, wrap_angle

# Max deviation of the initial heading from the center direction (rad).
_SPAWN_JITTER = 0.2

class Game:
    """Game runner.

    Args:
        config (Config): Game parameters.
        seed (int): Random seed for the game.
    """

    def __init__(self, config: Config, seed: int) -> None:
        self.config = config
        self.seed = seed
        self.state = self._new_game()


    def _new_game(self) -> GameState:
        """Create the initial state of a game.

        Only source of randomness in the engine: the same ``seed`` and ``config``
        always give the same state. Heads are spread evenly on a circle, with a random
        global rotation and a random slot assignment to avoid any bias tied to the
        snake index. Each snake faces the center, with a little noise, and its body
        lies in a straight line behind the head.

        Returns:
            GameState: State at tick 0, with every snake alive and the zone at the
            map radius.
        """
        rng = np.random.default_rng(self.seed)
        n, length = self.config.n_snakes, self.config.length

        slots = rng.permutation(n)
        polar = rng.uniform(-np.pi, np.pi) + 2 * np.pi * slots / n
        spawn_r = self.config.spawn_radius_ratio * self.config.map_radius
        heads = spawn_r * np.stack([np.cos(polar), np.sin(polar)], axis=1)

        angle = wrap_angle(polar + np.pi + rng.uniform(-_SPAWN_JITTER, _SPAWN_JITTER, n))

        direction = np.stack([np.cos(angle), np.sin(angle)], axis=1)
        offsets = np.arange(length) * self.config.speed
        body = heads[:, None, :] - offsets[None, :, None] * direction[:, None, :]

        return GameState(
            tick=0,
            body=body.astype(np.float32),
            angle=angle.astype(np.float32),
            alive=np.ones(n, dtype=bool),
            kills=np.zeros(n, dtype=np.int16),
            death_tick=np.full(n, -1, dtype=np.int32),
            killer=np.full(n, -1, dtype=np.int8),
            zone_radius=float(self.config.map_radius),
        )



    def _move_snakes(self, actions: np.ndarray) -> None:
        """Advance every alive snake by one tick, in place.

        Each alive snake turns, then moves ``speed`` forward. Dead snakes do not move.

        Args:
            config (Config): Game parameters.
            state (GameState): State to update.
            actions (np.ndarray): Rotation of each snake in radians, shape [N].
                Clipped to ``[-max_turn_rate, max_turn_rate]``.
        """
        alive = self.state.alive
        actions = np.clip(actions, -self.config.max_turn_rate, self.config.max_turn_rate)
        self.state.angle[alive] = wrap_angle(self.state.angle[alive] + actions[alive])

        direction = np.stack([np.cos(self.state.angle), np.sin(self.state.angle)], axis=1)
        new_heads = self.state.heads + self.config.speed * direction

        self.state.body[alive, 1:] = self.state.body[alive, :-1]
        self.state.body[alive, 0] = new_heads[alive]

    def _collisions(self) -> None:
        """Kill every alive snake whose head touches another snake's body, in place.

        A head touches a body when it is closer than ``2 * radius`` to one of its
        segments. All deaths of the tick are computed before ``alive`` is updated,
        so a head-on collision kills both snakes. A snake never collides with
        itself, and dead snakes are ignored both as heads and as bodies. When a
        head touches several bodies at once, the killer is the lowest index.
        """
        state = self.state
        n = self.config.n_snakes

        distance = np.linalg.norm(
            state.heads[:, None, None, :] - state.body[None, :, :, :], axis=3
        )
        touched = distance < 2 * self.config.radius
        touched &= ~np.eye(n, dtype=bool)[:, :, None]
        touched &= state.alive[:, None, None] & state.alive[None, :, None]

        hits = touched.any(axis=2)  # hits[i, j]: head i touches body j
        new_deaths = hits.any(axis=1)
        killers = np.argmax(hits, axis=1)[new_deaths]

        state.alive &= ~new_deaths
        state.killer[new_deaths] = killers
        state.death_tick[new_deaths] = state.tick
        state.kills += np.bincount(killers, minlength=n).astype(state.kills.dtype)


    def _zone(self) -> None:
        """Shrink the zone radius if the tick is past the start tick, in place."""

        if self.state.tick >= self.config.zone_start_tick:
            self.state.zone_radius = max(
                self.config.zone_min_radius,
                self.state.zone_radius - self.config.zone_shrink_per_tick,
            )

    def _snake_out_of_bounds(self) -> None:
        """Kills all snakes if their heads are outside the zone, in place."""

        out_of_bounds = np.linalg.norm(self.state.heads - self.config.zone_center, axis=1) > self.state.zone_radius
        self.state.alive &= ~out_of_bounds

    def step(self, actions: np.ndarray) -> GameState:
        """Advance the game by one tick.

        Args:
            actions (np.ndarray): Rotation of each snake in radians, shape [N].
                Clipped to ``[-max_turn_rate, max_turn_rate]``.

        Returns:
            GameState: New state after the tick.
        """
        self._move_snakes(actions)
        self._collisions()
        self._zone()
        self._snake_out_of_bounds()
        self.state.tick += 1
        return self.state.copy()