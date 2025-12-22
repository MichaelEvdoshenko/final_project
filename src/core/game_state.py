from typing import List, Optional


class GameState:
    def __init__(self, size: int = 3) -> None:
        if not isinstance(size, int):
            raise TypeError("Размер должен быть целым числом")
        if size <= 0:
            raise ValueError("Размер поля должен быть положительным")

        self.size: int = size
        self.field: List[List[str]] = [[" " for _ in range(self.size)]
                                       for _ in range(self.size)]
        self.last_move: List[Optional[int]] = [None, None]
        self.winner: Optional[str] = None
        self.count_move: int = 0
        self.available_stats: List[List[int]] = [
            [i, j]
            for i in range(self.size)
            for j in range(self.size)
        ]

    def make_move(self, row: int, col: int, player_sign: str) -> bool:
        if not (0 <= row < self.size and 0 <= col < self.size):
            print(f"Ошибка валидации: {ValueError}")
            return False
        if player_sign not in ["X", "O"]:
            print(f"Ошибка валидации: {ValueError}")
            return False
        if self.field[row][col] != " ":
            return False
        if self.winner is not None:
            return False

        self.field[row][col] = player_sign
        self.available_stats.remove([row, col])
        self.last_move = [row, col]
        self.count_move += 1
        return True
