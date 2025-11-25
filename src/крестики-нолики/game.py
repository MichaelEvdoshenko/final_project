class Krestik_nolik():
    def __init__(self, size = 3):
        if size <= 0:
            self.size = 3
        else:
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
        self.check_winner()
        return True

    def is_validate_move(self, points):
        for x, y in points:
            if x < 0 or x >= self.size or y < 0 or y >= self.size:
                return False
        return True

    def check_winner(self):
        if self.last_move[0] == None:
            return
    
        x, y = self.last_move
        player = self.field[x][y]

        if self.size <= 3:
            win_length = 3 
        else:
            win_length = 4

        directions = [
            (0, 1),
            (1, 0),
            (1, 1),
            (1, -1)
        ]

        for dx, dy in directions:
            max_count = 0

            for start_offset in range(win_length):
                count = 0
                for i in range(win_length):
                    nx = x + dx * (i - start_offset)
                    ny = y + dy * (i - start_offset)

                    if (0 <= nx < self.size and 0 <= ny < self.size and 
                        self.field[nx][ny] == player):
                        count += 1
                    else:
                        break

                if count > max_count:
                    max_count = count

            if max_count >= win_length:
                self.winner = player
                return
    
        if self.count_move == self.size * self.size:
            self.winner = "НИЧЬЯ"

    def get_available_stats(self):
        return self.available_stats

    def get_game_stat(self):
        if self.winner != None:
            return True
