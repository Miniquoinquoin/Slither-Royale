"""Immutable parameters of a game."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Config:
    """Game parameters, fixed when the game is created.

    All distances are in map units and all durations are in ticks.

    Attributes:
        n_snakes (int, optional): Number of snakes N. Defaults to 16.
        length (int, optional): Number of segments L per snake, fixed in v1.
            Defaults to 32.
        speed (float, optional): Distance travelled per tick, equal to the spacing
            between two segments. Defaults to 0.5.
        radius (float, optional): Radius of the head and of each segment.
            Defaults to 1.0.
        turn_rate (float, optional): Rotation per tick for the left and right
            actions, in radians. Defaults to 0.12.
        map_radius (float, optional): Radius of the circular map, centered on
            the origin. Defaults to 60.0.
        spawn_radius_ratio (float, optional): Heads spawn on a circle of radius
            ``spawn_radius_ratio * map_radius``. Defaults to 0.6.
        zone_start_tick (int, optional): Tick from which the zone starts
            shrinking. Defaults to 300.
        zone_shrink_per_tick (float, optional): Decrease of the zone radius at
            each tick. Defaults to 0.05.
        zone_min_radius (float, optional): Minimum zone radius. Defaults to 8.0.
        max_ticks (int, optional): Maximum duration of a game. Defaults to 3000.
    """

    n_snakes: int = 16
    length: int = 32
    speed: float = 0.5
    radius: float = 1.0
    turn_rate: float = 0.12
    map_radius: float = 60.0
    spawn_radius_ratio: float = 0.6
    zone_start_tick: int = 300
    zone_shrink_per_tick: float = 0.05
    zone_min_radius: float = 8.0
    max_ticks: int = 3000

    def __post_init__(self) -> None:
        """Check that the parameters are consistent.

        Raises:
            ValueError: If ``n_snakes`` is not between 1 and 127 (``killer`` is
                stored as int8).
            ValueError: If ``length`` is lower than 1.
            ValueError: If ``speed`` is not in ``]0, radius]``. Segments must
                overlap so the body is continuous and a head cannot pass through
                it in a single tick.
            ValueError: If ``zone_min_radius`` is not in ``]0, map_radius]``.
            ValueError: If the snakes do not fit inside the map at spawn.
        """
        if not 1 <= self.n_snakes <= 127:
            raise ValueError("n_snakes must be between 1 and 127 (killer is stored as int8)")
        if self.length < 1:
            raise ValueError("length must be >= 1")
        if not 0 < self.speed <= self.radius:
            raise ValueError("0 < speed <= radius is required")
        if not 0 < self.zone_min_radius <= self.map_radius:
            raise ValueError("0 < zone_min_radius <= map_radius is required")
        tail = self.spawn_radius_ratio * self.map_radius + (self.length - 1) * self.speed
        if tail + self.radius > self.map_radius:
            raise ValueError("snakes do not fit inside the map at spawn")
