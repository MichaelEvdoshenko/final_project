import pytest
from src.core.game import Krestik_nolik


def test_game_creation() -> None:
    game = Krestik_nolik(3)
    assert game.size == 3
    assert len(game.field) == 3
    assert len(game.field[0]) == 3


def test_game_default_size() -> None:
    game = Krestik_nolik()
    assert game.size == 3


def test_game_false_size() -> None:
    with pytest.raises(ValueError):
        Krestik_nolik(0)

    with pytest.raises(ValueError):
        Krestik_nolik(-1)


def test_game_type() -> None:
    with pytest.raises(TypeError):
        Krestik_nolik("три")  # type: ignore

    with pytest.raises(TypeError):
        Krestik_nolik(3.5)  # type: ignore


def test_game_enough_large_size() -> None:
    game = Krestik_nolik(5)
    assert game.size == 5
    assert len(game.field) == 5
    assert len(game.field[0]) == 5
