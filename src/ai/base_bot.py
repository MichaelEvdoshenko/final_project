class BaseBot:
    def __init__(self, symbol="X"):
        self.symbol = symbol
        if symbol == "X":
            self.opponent_symbol = "O"
        else:
            self.opponent_symbol = "X"
    
    def find_best_move(self, game_state):
        raise NotImplementedError
    
    def to_do_move(self, game_state):
        return self.find_best_move(game_state)