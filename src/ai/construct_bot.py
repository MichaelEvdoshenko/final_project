from typing import Optional, List
from src.ai.bot_Q_learning import Q_learning_bot
from src.ai.bot_MCTS import MCTS_bot
from src.core.game import Krestik_nolik


class bot_choice:
    def __init__(self, bot_type: str, first_turn: str, size: int = 3) -> None:
        self.bot_type = bot_type
        self.first_turn = first_turn
        self.size = size
        self.prelearn_bot: Optional[Q_learning_bot] = None

    def to_do_move(self, game: Krestik_nolik) -> List[int]:
        if self.bot_type == "Q_learning":
            if self.prelearn_bot is None:
                empty_game = Krestik_nolik(self.size)
                self.prelearn_bot = Q_learning_bot(game=empty_game)
                self.prelearn_bot.learn(self.first_turn)

            assert self.prelearn_bot is not None
            return self.prelearn_bot.find_best_move(game)

        elif self.bot_type == "MCTS":
            prelearn_bot = MCTS_bot(game)
            return prelearn_bot.find_best_move()
        else:
            raise ValueError(f"Неизвестный тип бота: {self.bot_type}")
