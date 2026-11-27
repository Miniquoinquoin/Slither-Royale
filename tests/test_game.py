import numpy as np

from core import Config
from core.game import Game


def make_game(n_snakes: int = 4, length: int = 3) -> Game:
    """Game whose snakes lie on separate horizontal lines, and with separate segments to trigger specific collisions."""
    game = Game(Config(n_snakes=n_snakes, length=length), seed=0)
    for s in range(n_snakes):
        game.state.body[s, :, 0] = np.arange(length) * 5
        game.state.body[s, :, 1] = s * 10
    return game


def test_spawn_has_no_collision():
    game = Game(Config(), seed=0)
    game._collisions()
    assert game.state.alive.all()


def test_head_on_body_kills_and_credits_killer():
    game = make_game()
    game.state.tick = 7
    game.state.body[0, 0] = game.state.body[1, 2]
    game.state.body[2, 0] = game.state.body[1, 1]

    game._collisions()

    np.testing.assert_array_equal(game.state.alive, [False, True, False, True])
    np.testing.assert_array_equal(game.state.killer, [1, -1, 1, -1])
    np.testing.assert_array_equal(game.state.kills, [0, 2, 0, 0])
    np.testing.assert_array_equal(game.state.death_tick, [7, -1, 7, -1])


def test_dead_snakes_are_ignored():
    game = make_game()
    game.state.alive[:] = [True, False, False, True]
    game.state.body[0, 0] = game.state.body[1, 2]
    game.state.body[2, 0] = game.state.body[3, 2]

    game._collisions()

    np.testing.assert_array_equal(game.state.alive, [True, False, False, True])
    assert (game.state.kills == 0).all()


def test_head_on_collision_kills_both():
    game = make_game(n_snakes=2)
    game.state.tick = 7
    game.state.body[1, 0] = game.state.body[0, 0]

    game._collisions()

    assert not game.state.alive.any()
    np.testing.assert_array_equal(game.state.killer, [1, 0])
    np.testing.assert_array_equal(game.state.kills, [1, 1])
    np.testing.assert_array_equal(game.state.death_tick, [7, 7])
