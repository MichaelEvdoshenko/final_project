import pytest
import sys
import os
from ai.bot_Q_learning import Q_learning_bot
from core.game import Krestik_nolik
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'src'))


class TestQLearningBot:
    def test_q_learning_bot_1(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)
        assert bot.symbol == "X"
        assert bot.opponent_symbol == "O"
        assert bot.alfa == 0.1
        assert bot.eps == 0.9
        assert bot.size == 3
        assert isinstance(bot.massive_Q, dict)

    def test_q_learning_bot_2(self):
        game = Krestik_nolik(3)
        with pytest.raises(TypeError):
            Q_learning_bot("     ")

        with pytest.raises(ValueError):
            Q_learning_bot(game, alfa=1.5)

        with pytest.raises(ValueError):
            Q_learning_bot(game, eps=-0.1)

    def test_q_learning_bot_3(self):
        bot = Q_learning_bot()
        assert bot.symbol == "X"
        assert bot.alfa == 0.1
        assert bot.eps == 0.9
        assert hasattr(bot, 'size')

    def test_from_list_to_hash_1(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
        hash_result = bot.from_list_to_hash(board)

        assert isinstance(hash_result, str)
        assert hash_result == "         "
        assert len(hash_result) == 9

        board[0][0] = "X"
        hash_result = bot.from_list_to_hash(board)
        assert hash_result == "X        "

    def test_from_list_to_hash_2(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        with pytest.raises(TypeError):
            bot.from_list_to_hash("не список")

        with pytest.raises(TypeError):
            bot.from_list_to_hash([1, 2, 3])

    def test_get_q_values_for_state(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        state_hash = "         "
        q_values = bot._get_q_values_for_state(state_hash)

        assert isinstance(q_values, np.ndarray)
        assert len(q_values) == 9
        assert all(q == 0.0 for q in q_values)
        assert state_hash in bot.massive_Q

    def test_learn_1(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        with pytest.raises(ValueError):
            bot.learn(first_turn="YY")

    def test_random_gaming_without_learn(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        with pytest.raises(ValueError):
            bot.random_gaming("bot")

    def test_q_gaming_without_learn(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)

        with pytest.raises(ValueError):
            bot.Q_gaming("bot")

    def test_q_gaming(self):
        game = Krestik_nolik(3)
        bot = Q_learning_bot(game)
        bot.sup_game = Krestik_nolik(3)
        bot.Q_gaming("bot", epsilon=0.1)
        assert len(bot.massive_Q) > 0
