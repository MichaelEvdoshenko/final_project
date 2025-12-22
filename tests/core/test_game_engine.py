import pytest
from src.core.game_engine import KrestikNolikEngine


class TestKrestikNolikEngine:
    def test_engine_creation(self) -> None:
        engine = KrestikNolikEngine(3)
        assert engine.size == 3
        assert len(engine.field) == 3
        assert engine.count_move == 0
        assert engine.winner is None

    def test_invalid_size(self) -> None:
        with pytest.raises(ValueError):
            KrestikNolikEngine(0)

        with pytest.raises(TypeError):
            KrestikNolikEngine("три")  # type: ignore

    def test_move_1(self) -> None:
        engine = KrestikNolikEngine(3)
        assert engine.make_move(0, 0, "X") is True
        assert engine.field[0][0] == "X"
        assert engine.count_move == 1

    def test_move_2(self) -> None:
        engine = KrestikNolikEngine(3)

        with pytest.raises(ValueError):
            engine.make_move(5, 5, "X")

        with pytest.raises(TypeError):
            engine.make_move("один", 2, "X")  # type: ignore

    def test_move_3(self) -> None:
        engine = KrestikNolikEngine(3)

        with pytest.raises(ValueError):
            engine.make_move(0, 0, "Y")

        with pytest.raises(TypeError):
            engine.make_move(0, 0, 123)  # type: ignore

    def test_is_validate_move(self) -> None:
        engine = KrestikNolikEngine(3)

        assert engine.is_validate_move([(0, 0), (1, 1)]) is True
        assert engine.is_validate_move([(5, 5), (1, 1)]) is False

        with pytest.raises(TypeError):
            engine.is_validate_move("не список")  # type: ignore

        with pytest.raises(TypeError):
            engine.is_validate_move([(0, 0, 0)])

    def test_win_1(self) -> None:
        engine = KrestikNolikEngine(3)

        engine.make_move(0, 0, "X")
        engine.make_move(1, 0, "O")
        engine.make_move(0, 1, "X")
        engine.make_move(1, 1, "O")
        engine.make_move(0, 2, "X")

        assert engine.winner == "X"
        assert engine.is_game_over() is True

    def test_win_2(self) -> None:
        engine = KrestikNolikEngine(3)

        engine.make_move(0, 0, "X")
        engine.make_move(0, 1, "O")
        engine.make_move(1, 0, "X")
        engine.make_move(1, 1, "O")
        engine.make_move(2, 0, "X")

        assert engine.winner == "X"
        assert engine.is_game_over() is True

    def test_draw(self) -> None:
        engine = KrestikNolikEngine(3)

        moves = [
            (0, 0, "X"), (0, 1, "O"), (0, 2, "X"),
            (1, 0, "X"), (1, 1, "O"), (1, 2, "O"),
            (2, 0, "O"), (2, 1, "X"), (2, 2, "X")
        ]

        for row, col, player in moves:
            engine.make_move(row, col, player)

        assert engine.winner == "НИЧЬЯ"
        assert engine.is_game_over() is True
