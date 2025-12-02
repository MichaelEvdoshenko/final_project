from game import Krestik_nolik
import random
import copy
import itertools

class Q_learning_bot():
    def __init__(self, game = Krestik_nolik(), alfa = 0.1, eps = 0.9):
        self.game = game
        self.alfa = alfa
        self.eps = eps
        self.size = self.game.size
        self.massive_Q = {}
        for state in self.generate_hash():
            self.massive_Q[state] = [0 for _ in range(self.size * self.size)]
        self.learn()

    def generate_hash(self):
        elements = ['X', 'O', ' ']
        total_cells = self.size * self.size
        massive_Q = []

        for comb in itertools.product(elements, repeat=total_cells):
            board_string = ''.join(comb)
            massive_Q.append(board_string)
        return massive_Q
    
    def from_list_to_hash(self, list):
        return ''.join(''.join(row) for row in list)

    def random_gaming(self):
        sim_game = copy.deepcopy(self.game)
        player = "O"
        moves = []

        while sim_game.winner == None:
            avail = sim_game.available_stats.copy()
            rand_move = random.randint(0, len(avail) - 1)
            [x, y] = avail[rand_move]
            moves.append([self.from_list_to_hash(sim_game.field), [x,y]])
            sim_game.make_move(x, y, player)
            if player == "O":
                player = "X"
            else:
                player = "O"

        if sim_game.winner == "X":
            r = 1
        elif sim_game.winner == "O":
            r = 0
        else:
            r = 0.5

        moves.reverse()
        prev = None
        for [stat, [x,y]] in moves:
            if prev == None:
                self.massive_Q[stat][x*self.size + y] = self.massive_Q[stat][x*self.size + y] + self.alfa * (r + self.eps * 0 - self.massive_Q[stat][x*self.size + y])
            else:
                [prev_stat,[prev_x, prev_y]] = prev
                self.massive_Q[stat][x*self.size + y] = self.massive_Q[stat][x*self.size + y] + self.alfa * (r + self.eps * self.massive_Q[prev_stat][prev_x*self.size + prev_y] - self.massive_Q[stat][x*self.size + y])
            prev = [stat, [x,y]]
    
    def Q_gaming(self):
        sim_game = copy.deepcopy(self.game)
        player = "O"
        moves = []

        while sim_game.winner == None:
            avail = sim_game.available_stats.copy()
            hash_field = self.from_list_to_hash(sim_game.field)
            best_Q, best_move = -1, [-1,-1]
            for [x,y] in avail:
                if self.massive_Q[hash_field][x*self.size + y] > best_Q:
                    best_Q = self.massive_Q[hash_field][x*self.size + y]
                    best_move = [x,y]
            moves.append([best_move, [x,y]])
            sim_game.make_move(x, y, player)
            if player == "O":
                player = "X"
            else:
                player = "O"

        if sim_game.winner == "X":
            r = 1
        elif sim_game.winner == "O":
            r = 0
        else:
            r = 0.5

        moves.reverse()
        prev = None
        for [stat, [x,y]] in moves:
            if prev == None:
                self.massive_Q[stat][x*self.size + y] = self.massive_Q[stat][x*self.size + y] + self.alfa * (r + self.eps * 0 - self.massive_Q[stat][x*self.size + y])
            else:
                [prev_stat,[prev_x, prev_y]] = prev
                self.massive_Q[stat][x*self.size + y] = self.massive_Q[stat][x*self.size + y] + self.alfa * (r + self.eps * self.massive_Q[prev_stat][prev_x*self.size + prev_y] - self.massive_Q[stat][x*self.size + y])
            prev = [stat, [x,y]]

    def learn(self):
        for _ in range(500):
            self.random_gaming()
        for _ in range(10000):
            self.Q_gaming()
    
    def find_best_move(self, field):
        Q_state = self.massive_Q[self.from_list_to_hash(field)]
        maxi = -1
        best_move = [-1, -1]

        for i in range(self.size):
            for j in range(self.size):
                if Q_state[i*self.size + j] > maxi:
                    print(Q_state[i*self.size + j], i, j)
                    best_move = [i,j]
                    maxi = Q_state[i*self.size + j]
        
        return best_move
    
    def show(self):
        print(self.massive_Q)