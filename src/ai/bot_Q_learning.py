from core.game import Krestik_nolik
import random
import copy
import numpy as np
from ai.base_bot import BaseBot


class Q_learning_bot(BaseBot):
    def __init__(self, game=Krestik_nolik(), alfa=0.1, eps=0.9):
        if not isinstance(game, Krestik_nolik):
            raise TypeError("game должен быть Krestik_nolik")

        if not isinstance(alfa, (int, float)) or not (0 <= alfa <= 1):
            raise ValueError("alfa должен быть числом от 0 до 1")

        if not isinstance(eps, (int, float)) or not (0 <= eps <= 1):
            raise ValueError("eps должен быть числом от 0 до 1")

        super().__init__(symbol="X")

        self.game = game
        self.sup_game = None
        self.alfa = alfa
        self.eps = eps
        self.size = self.game.size
        self.massive_Q = {}

    def from_list_to_hash(self, field):
        if not isinstance(field, (list, np.ndarray)):
            raise TypeError("field должен быть списком или массивом")

        field_array = np.array(field)
        return ''.join(field_array.flatten())

    def _get_q_values_for_state(self, state_hash):
        if not isinstance(state_hash, str):
            raise TypeError("state_hash должен быть строкой")

        if state_hash not in self.massive_Q:
            sup_v3 = self.size * self.size
            self.massive_Q[state_hash] = np.zeros(sup_v3, dtype=np.float64)
        return self.massive_Q[state_hash]

    def random_gaming(self, first_turn):
        if self.sup_game is None:
            raise ValueError("sup_game не инициализирован")
        if first_turn not in ["player", "bot"]:
            raise ValueError("first_turn должен быть 'player' или 'bot'")

        sim_game = copy.deepcopy(self.sup_game)

        if first_turn == "player":
            player = self.opponent_symbol
        else:
            player = self.symbol
        moves = []
        while sim_game.winner is None:
            avail = sim_game.available_stats.copy()
            rand_move = np.random.randint(0, len(avail))
            [x, y] = avail[rand_move]
            state_hash = self.from_list_to_hash(sim_game.field)
            moves.append([state_hash, [x, y], player])
            sim_game.make_move(x, y, player)
            if player == self.symbol:
                player = self.opponent_symbol
            else:
                player = self.symbol

        if sim_game.winner == self.symbol:
            r = 1.0
        elif sim_game.winner == self.opponent_symbol:
            r = -1.0
        else:
            r = 0.0

        moves.reverse()
        next_max_q = 0.0

        for state_hash, [x, y], move_player in moves:
            q_values = self._get_q_values_for_state(state_hash)
            idx = x * self.size + y
            if move_player == self.symbol:
                reward = r
            else:
                reward = -r
            current_q = q_values[idx]
            sup_v2 = reward + self.eps * next_max_q - current_q
            q_values[idx] = current_q + self.alfa * (sup_v2)

            next_max_q = np.max(q_values)

    def Q_gaming(self, first_turn, epsilon=0.1):
        if self.sup_game is None:
            raise ValueError("sup_game не инициализирован")

        if first_turn not in ["player", "bot"]:
            raise ValueError("first_turn должен быть 'player' или 'bot'")

        if not isinstance(epsilon, (int, float)) or not (0 <= epsilon <= 1):
            raise ValueError("epsilon должен быть числом от 0 до 1")

        sim_game = copy.deepcopy(self.sup_game)
        if first_turn == "player":
            player = self.opponent_symbol
        else:
            player = self.symbol
        moves = []
        while sim_game.winner is None:
            avail = sim_game.available_stats.copy()
            state_hash = self.from_list_to_hash(sim_game.field)

            if np.random.random() < epsilon:
                action = random.choice(avail)
            else:
                q_values = self._get_q_values_for_state(state_hash)
                best_Q = -np.inf
                best_actions = []

                for x, y in avail:
                    current_q = q_values[x*self.size + y]
                    if current_q > best_Q:
                        best_Q = current_q
                        best_actions = [[x, y]]
                    elif current_q == best_Q:
                        best_actions.append([x, y])

                if best_actions != []:
                    action = random.choice(best_actions)
                else:
                    action = random.choice(avail)

            moves.append([state_hash, action, player])
            sim_game.make_move(action[0], action[1], player)
            if player == self.symbol:
                player = self.opponent_symbol
            else:
                player = self.symbol

        if sim_game.winner == self.symbol:
            r = 1.0
        elif sim_game.winner == self.opponent_symbol:
            r = -1.0
        else:
            r = 0.5

        moves.reverse()
        next_max_q = 0.0

        for state_hash, action, move_player in moves:
            x, y = action
            q_values = self._get_q_values_for_state(state_hash)
            idx = x*self.size + y

            if move_player == self.symbol:
                reward = r
            else:
                reward = -r

            current_q = q_values[idx]
            sup_v = reward + self.eps * next_max_q - current_q
            q_values[idx] = current_q + self.alfa * (sup_v)

            next_max_q = np.max(q_values)

    def learn(self, first_turn):
        if first_turn not in ["player", "bot"]:
            raise ValueError("first_turn должен быть 'player' или 'bot'")

        self.sup_game = Krestik_nolik(self.size)
        for i in range(500):
            self.random_gaming(first_turn)
        for i in range(10000):
            self.Q_gaming(first_turn)

    def find_best_move(self, game):
        if not isinstance(game, Krestik_nolik):
            raise TypeError("game должен быть Krestik_nolik")

        if game.winner is not None:
            raise ValueError("Игра уже завершена")

        available_moves = game.available_stats
        if not available_moves:
            raise ValueError("Нет доступных ходов")

        state_hash = self.from_list_to_hash(game.field)
        if state_hash not in self.massive_Q:
            available_moves = game.available_stats
            if available_moves:
                return random.choice(available_moves)
            else:
                return [-1, -1]

        q_values = self.massive_Q[state_hash]
        maxi = -np.inf
        best_move = [-1, -1]

        for i in range(self.size):
            for j in range(self.size):
                if game.field[i][j] == ' ':
                    if q_values[i*self.size + j] > maxi:
                        best_move = [i, j]
                        maxi = q_values[i*self.size + j]

        return best_move
