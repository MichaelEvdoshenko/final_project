from core.game import Krestik_nolik
import random
import copy

class Q_learning_bot():
    def __init__(self, game = Krestik_nolik(), alfa = 0.1, eps = 0.9):
        self.game = game
        self.alfa = alfa
        self.eps = eps
        self.size = self.game.size
        self.massive_Q = {}
        self.learn()
    
    def from_list_to_hash(self, list):
        return ''.join(''.join(row) for row in list)
    
    def _get_q_values_for_state(self, state_hash):
        if state_hash not in self.massive_Q:
            self.massive_Q[state_hash] = [0 for _ in range(self.size * self.size)]
        return self.massive_Q[state_hash]

    def random_gaming(self, first_turn):
        sim_game = copy.deepcopy(self.game)
        if first_turn == "player":
            player = "O"
        else:
            player = "X"
        moves = []

        while sim_game.winner == None:
            avail = sim_game.available_stats.copy()
            rand_move = random.randint(0, len(avail) - 1)
            [x, y] = avail[rand_move]
            state_hash = self.from_list_to_hash(sim_game.field)
            moves.append([state_hash, [x,y]])
            sim_game.make_move(x, y, player)
            if player == "O":
                player = "X"
            else:
                player = "O"

        if sim_game.winner == "X":
            r = 1
        elif sim_game.winner == "O":
            r = -1
        else:
            r = -0.1

        moves.reverse()
        prev = None
        for [state_hash, [x,y]] in moves:
            q_values = self._get_q_values_for_state(state_hash)
            if prev == None:
                q_values[x*self.size + y] = q_values[x*self.size + y] + self.alfa * (r + self.eps * 0 - q_values[x*self.size + y])
            else:
                [prev_stat,[prev_x, prev_y]] = prev
                prev_q_values = self._get_q_values_for_state(prev_stat)
                q_values[x*self.size + y] = q_values[x*self.size + y] + self.alfa * (r + self.eps * prev_q_values[prev_x*self.size + prev_y] - q_values[x*self.size + y])
            prev = [state_hash, [x,y]]
    
    def Q_gaming(self, first_turn):
        sim_game = copy.deepcopy(self.game)
        if first_turn == "player":
            player = "O"
        else:
            player = "X"
        moves = []

        while sim_game.winner == None:
            avail = sim_game.available_stats.copy()
            state_hash = self.from_list_to_hash(sim_game.field)
            q_values = self._get_q_values_for_state(state_hash)
            best_Q, best_move = -1, [-1,-1]
            for [x,y] in avail:
                if q_values[x*self.size + y] > best_Q:
                    best_Q = q_values[x*self.size + y]
                    best_move = [x,y]
            moves.append([state_hash, best_move])
            sim_game.make_move(best_move[0], best_move[1], player)
            if player == "O":
                player = "X"
            else:
                player = "O"

        if sim_game.winner == "X":
            r = 1
        elif sim_game.winner == "O":
            r = -1
        else:
            r = -0.1

        moves.reverse()
        prev = None
        for [state_hash, [x,y]] in moves:
            q_values = self._get_q_values_for_state(state_hash)
            if prev == None:
                q_values[x*self.size + y] = q_values[x*self.size + y] + self.alfa * (r + self.eps * 0 - q_values[x*self.size + y])
            else:
                [prev_stat,[prev_x, prev_y]] = prev
                prev_q_values = self._get_q_values_for_state(prev_stat)
                q_values[x*self.size + y] = q_values[x*self.size + y] + self.alfa * (r + self.eps * prev_q_values[prev_x*self.size + prev_y] - q_values[x*self.size + y])
            prev = [state_hash, [x,y]]

    def learn(self, first_turn):
        for _ in range(500):
            self.random_gaming(first_turn)
        for _ in range(10000):
            self.Q_gaming(first_turn)
    
    def find_best_move(self, field):
        state_hash = self.from_list_to_hash(field)
        if state_hash not in self.massive_Q:
            temp_game = Krestik_nolik(self.size)
            temp_game.field = copy.deepcopy(field)
            available_moves = temp_game.available_stats
            if available_moves:
                return random.choice(available_moves)
            else:
                return [-1, -1]
        
        q_values = self.massive_Q[state_hash]
        maxi = -1
        best_move = [-1, -1]

        for i in range(self.size):
            for j in range(self.size):
                if field[i][j] == ' ':
                    if q_values[i*self.size + j] > maxi:
                        best_move = [i,j]
                        maxi = q_values[i*self.size + j]
        
        return best_move