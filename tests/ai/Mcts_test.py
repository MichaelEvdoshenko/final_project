import pytest
from src.ai.bot_MCTS import MCTS_bot
from src.core.game import Krestik_nolik


class TestMCTSBot:
    def test_mcts_1(self):
        game = Krestik_nolik(3)
        bot = MCTS_bot(game)
        assert bot.symbol == "X"
        assert bot.opponent_symbol == "O"
        assert hasattr(bot, 'find_best_move')

    def test_mcts_bot_2(self):
        with pytest.raises(ValueError):
            MCTS_bot(None)

        with pytest.raises(TypeError):
            MCTS_bot("invalid_game")

    def test_evaluate(self):
        game = Krestik_nolik(3)
        bot = MCTS_bot(game)

        assert bot.evaluate_result("X") == 1
        assert bot.evaluate_result("O") == 0
        assert bot.evaluate_result("НИЧЬЯ") == 0.5

        with pytest.raises(TypeError):
            bot.evaluate_result(123)

    def test_find_best_move_1(self):
        game = Krestik_nolik(3)
        game.make_move(0, 0, "X")
        game.make_move(0, 1, "O")
        game.make_move(1, 1, "X")
        game.make_move(0, 2, "O")
        game.make_move(2, 2, "X")

        bot = MCTS_bot(game)

        with pytest.raises(ValueError):
            bot.find_best_move()

    def test_simulate_1(self):
        game = Krestik_nolik(3)
        bot = MCTS_bot(game)

        result = bot.simulate([0, 0], game, "X")

        assert result in [0, 0.5, 1]

    def test_simulate_2(self):
        game = Krestik_nolik(3)
        bot = MCTS_bot(game)

        with pytest.raises(ValueError):
            bot.simulate([0], game, "X")

        with pytest.raises(TypeError):
            bot.simulate([0, 0], "", "X")

        with pytest.raises(ValueError):
            bot.simulate([0, 0], game, "Y")
