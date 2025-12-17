from .game_state import GameState

class KrestikNolikEngine:
    def __init__(self, size=3):
        if not isinstance(size, int):
            raise TypeError(f"Размер должен быть целым числом")
        if size < 1:
            raise ValueError(f"Размер поля должен быть положительным")
        if size > 5:
            raise ValueError(f"Размер поля должен быть меньше")
        self.state = GameState(size)
        self.size = size
    
    def make_move(self, row, col, player_sign):
        if not isinstance(row, int) or not isinstance(col, int):
            raise TypeError(f"Координаты должны быть целыми числами")
        
        if not isinstance(player_sign, str):
            raise TypeError(f"Знак игрока должен быть строкой")
        
        if player_sign not in ["X","O"]:
            raise ValueError(f"Знак игрока должен быть 'X' или 'O'")
        
        if not (0 <= row < self.size and 0 <= col < self.size):
            raise ValueError(f"Координаты вне поля размером")
        
        if self.state.make_move(row, col, player_sign):
            self.check_winner()
            return True
        return False
    
    def is_validate_move(self, points):
        if not isinstance(points, (list, tuple)):
            raise TypeError(f"points должен быть списком или кортежем")

        for point in points:
            if not isinstance(point, (list, tuple)) or len(point) != 2:
                raise TypeError(f"Каждая точка должна быть кортежем или списком из 2 элементов")
            
            x, y = point
            if (x < 0 or x >= self.size) or (y < 0 or y >= self.size):
                return False
        return True

    def check_winner(self):
        if self.state.last_move[0] == None:
            return
    
        x, y = self.state.last_move
        player = self.state.field[x][y]

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
                        self.state.field[nx][ny] == player):
                        count += 1
                    else:
                        break

                if count > max_count:
                    max_count = count

            if max_count >= win_length:
                self.state.winner = player
                return
    
        if self.state.count_move == self.size * self.size:
            self.state.winner = "НИЧЬЯ"

    def get_available_stats(self):
        return self.state.available_stats

    def is_game_over(self):
        return self.state.winner is not None

    def get_game_stat(self):
        if self.state.winner != None:
            return True
    
    @property
    def field(self):
        return self.state.field
    
    @property
    def last_move(self):
        return self.state.last_move
    
    @property
    def winner(self):
        return self.state.winner
    
    @property
    def count_move(self):
        return self.state.count_move
    
    @property
    def available_stats(self):
        return self.state.available_stats
