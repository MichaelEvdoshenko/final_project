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
    
    def from_list_to_hash(self, list):
        return ''.join(''.join(row) for row in list)
    
    def _get_q_values_for_state(self, state_hash):
        if state_hash not in self.massive_Q:
            self.massive_Q[state_hash] = [0 for _ in range(self.size * self.size)]
        return self.massive_Q[state_hash]

    def random_gaming(self, first_turn):
        sim_game = copy.deepcopy(self.sup_game)
    
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
            moves.append([state_hash, [x, y], player])
            sim_game.make_move(x, y, player)
            if player == "X":
                player = "O"
            else:
                player = "X"

        if sim_game.winner == "X":
            r = 1.0
        elif sim_game.winner == "O":
            r = -1.0
        else:
            r = 0.0
        
        moves.reverse()
        next_max_q = 0
    
        for state_hash, [x, y], move_player in moves:
            q_values = self._get_q_values_for_state(state_hash)
            idx = x * self.size + y
            if move_player == "X":
                reward = r
            else:
                reward = -r
            current_q = q_values[idx]
            q_values[idx] = current_q + self.alfa * (reward + self.eps * next_max_q - current_q)
        
            next_max_q = max(q_values) 
    
    def Q_gaming(self, first_turn, epsilon=0.1):
        sim_game = copy.deepcopy(self.sup_game)
        if first_turn == "player":
            player = "O"
        else:
            player = "X"
        moves = []
        while sim_game.winner == None:
            avail = sim_game.available_stats.copy()
            state_hash = self.from_list_to_hash(sim_game.field)
        
            if random.random() < epsilon:
                action = random.choice(avail)
            else:
                q_values = self._get_q_values_for_state(state_hash)
                best_Q = -float('inf')
                best_actions = []
            
                for x, y in avail:
                    current_q = q_values[x*self.size + y]
                    if current_q > best_Q:
                        best_Q = current_q
                        best_actions = [[x,y]]
                    elif current_q == best_Q:
                        best_actions.append([x,y])
            
                if best_actions != []:
                    action = random.choice(best_actions) 
                else:
                    action = random.choice(avail)
        
            moves.append([state_hash, action, player])
            sim_game.make_move(action[0], action[1], player)
            if player == "O":
                player = "X"
            else:
                player = "O"
    
        if sim_game.winner == "X":
            r = 1.0
        elif sim_game.winner == "O":
            r = -1.0
        else:
            r = 0.5

        moves.reverse()
        next_max_q = 0
    
        for state_hash, action, move_player in moves:
            x, y = action
            q_values = self._get_q_values_for_state(state_hash)
            idx = x*self.size + y

            if move_player == "X":
                reward = r
            else:
                reward = -r

            current_q = q_values[idx]
            q_values[idx] = current_q + self.alfa * (reward + self.eps * next_max_q - current_q)

            next_max_q = max(q_values)

    def learn(self, first_turn):
        self.sup_game = Krestik_nolik(self.size)
        for i in range(500):
            self.random_gaming(first_turn)
        for i in range(10000):
            self.Q_gaming(first_turn)
    
    def find_best_move(self, game):
        state_hash = self.from_list_to_hash(game.field)
        if state_hash not in self.massive_Q:
            available_moves = game.available_stats
            if available_moves:
                return random.choice(available_moves)
            else:
                return [-1, -1]
        
        q_values = self.massive_Q[state_hash]
        maxi = -1
        best_move = [-1, -1]

        for i in range(self.size):
            for j in range(self.size):
                if game.field[i][j] == ' ':
                    if q_values[i*self.size + j] > maxi:
                        best_move = [i,j]
                        maxi = q_values[i*self.size + j]
        
        return best_move