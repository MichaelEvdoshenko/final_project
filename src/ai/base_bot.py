from abc import ABC, abstractmethod
from typing import Any


class BaseBot(ABC):
    def __init__(self, symbol: str = "X") -> None:
        self.symbol: str = symbol
        if symbol == "X":
            self.opponent_symbol: str = "O"
        else:
            self.opponent_symbol = "X"

    @abstractmethod
    def find_best_move(self, game_state: Any) -> Any:
        pass

    def to_do_move(self, game_state: Any) -> Any:
        return self.find_best_move(game_state)
