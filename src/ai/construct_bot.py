from ai.bot_Q_learning import Q_learning_bot
from ai.bot_MCTS import MCTS_bot
from core.game import Krestik_nolik


class bot_choice():
    def __init__(self, bot_type: str, first_turn: str, size: int = 3):
        self.bot_type = bot_type
        self.first_turn = first_turn
        self.size = size
        self.prelearn_bot = None

    def to_do_move(self, game: Krestik_nolik):
        if self.bot_type == "Q_learning":
            if not self.prelearn_bot:
                empty_game = Krestik_nolik(self.size)
                self.prelearn_bot = Q_learning_bot(game=empty_game)

                self.prelearn_bot.learn(self.first_turn)

            return self.prelearn_bot.find_best_move(game)

        elif self.bot_type == "MCTS":
            prelearn_bot = MCTS_bot(game)
            return prelearn_bot.find_best_move()

        else:
            raise ValueError(f"Неизвестный тип бота: {self.bot_type}")
