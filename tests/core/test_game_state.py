import pytest
from src.core.game_state import GameState


class TestGameState:
    def test_valid_inti(self) -> None:
        state = GameState(3)
        assert state.size == 3
        assert len(state.field) == 3
        assert state.count_move == 0
        assert state.winner is None
        assert len(state.available_stats) == 9

    def test_type_of_size(self) -> None:
        with pytest.raises(TypeError):
            GameState("три")  # type: ignore

        with pytest.raises(TypeError):
            GameState(3.5)  # type: ignore

    def test_value_of_size(self) -> None:
        with pytest.raises(ValueError):
            GameState(0)

        with pytest.raises(ValueError):
            GameState(-5)

    def test_move_correct(self) -> None:
        state = GameState(3)
        assert state.make_move(1, 1, "X") is True
        assert state.field[1][1] == "X"
        assert state.count_move == 1
        assert [1, 1] not in state.available_stats
        assert state.last_move == [1, 1]

    def test_invalid_coordinate_type(self) -> None:
        state = GameState(3)

        with pytest.raises(TypeError):
            state.make_move("один", 2, "X")  # type: ignore

        with pytest.raises(TypeError):
            state.make_move(1, 2.5, "O")  # type: ignore
