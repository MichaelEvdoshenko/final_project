class GameState:
    def __init__(self, size = 3):
        if not isinstance(size, int):
            raise TypeError(f"Размер должен быть целым числом")
        if size <= 0:
            raise ValueError(f"Размер поля должен быть положительным")

        self.size = size
        self.field = [[" " for _ in range(self.size)] for _ in range(self.size)]
        self.last_move = [None, None]
        self.winner = None
        self.count_move = 0
        self.available_stats = [[i, j] for i in range(self.size) for j in range(self.size)]

    def make_move(self, row, col, player_sign):
        if not (0 <= row < self.size and 0 <= col < self.size):
            print(f"Ошибка валидации: {ValueError}")
            return False
        if player_sign not in ["X", "O"]:
            print(f"Ошибка валидации: {ValueError}")
            return False
        if self.field[row][col] != " ":
            return False
        if self.winner != None:
            return False
        self.field[row][col] = player_sign
        self.available_stats.remove([row, col])
        self.last_move = [row, col]
        self.count_move += 1
        return True