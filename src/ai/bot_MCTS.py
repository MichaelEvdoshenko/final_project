from core.game import Krestik_nolik
from core.tree import Tree
import random
import copy
import math
from ai.base_bot import BaseBot

class MCTS_bot(BaseBot):
    def __init__(self, game_state: Krestik_nolik()):

        if game_state is None:
            raise ValueError("game_state не может быть None")
        if not isinstance(game_state, Krestik_nolik):
            raise TypeError(f"game_state должен быть Krestik_nolik")

        super().__init__(symbol = "X")
        self.game = copy.deepcopy(game_state)
        self.state = self.game.field
        self.root = Tree()
        self.list_mean_UBC1 = [1]
    
    def evaluate_result(self, winner):

        if not isinstance(winner, str):
            raise TypeError(f"winner должен быть строкой")
        if winner not in ["X","O","НИЧЬЯ"]:
            raise TypeError(f"winner должен быть 'X' или 'O' или 'НИЧЬЯ'")

        if winner == self.symbol:
            return 1
        elif winner == "НИЧЬЯ":
            return 0.5
        else:
            return 0

    def down_to_tree(self):
        node = self.root
        sup_game = copy.deepcopy(self.game)
        player = self.symbol
        
        while node.children and len(node.children) == len(sup_game.available_stats) and sup_game.winner == None:
            if random.random() < 0.25:
                next_node = random.choice(node.children)
            else:
                maximal_UBC1 = max(child.UBC1 for child in node.children)
                candidates = [ch for ch in node.children if ch.UBC1 == maximal_UBC1]
                next_node = random.choice(candidates)

            if not isinstance(next_node.value, list) or len(next_node.value) != 2:
                raise ValueError(f"Некорректный node")
            x, y = next_node.value
            if not sup_game.make_move(x, y, player):
                raise ValueError(f"Невозможно сделать ход")

            node = next_node
            sup_game.make_move(next_node.value[0], next_node.value[1], player)
            if player == self.symbol:
                player = self.opponent_symbol
            else:
                player = self.symbol

        if sup_game.winner == None:
            used_children_coord = [child.value for child in node.children]
            for child in sup_game.available_stats:
                if child not in used_children_coord:
                    if not isinstance(child, list) or len(child) != 2:
                        raise ValueError(f"Некорректный ход")
                    sim_game = copy.deepcopy(sup_game)
                    prohod = self.simulate(child, sim_game, player)
                    UBC1 = sum(self.list_mean_UBC1)/(len(self.list_mean_UBC1))
                    ch = Tree(value = child, count_win = prohod, count_inbound = 1, UBC1 = UBC1)
                    node.add_child(ch)
                    break
        else:
            prohod = self.evaluate_result(sup_game.winner)

        while node.parent != None:
            node.count_win += prohod
            node.count_inbound += 1
            UBC1 = (node.count_win/node.count_inbound) + math.sqrt(100*math.log(node.parent.count_inbound + 1)/node.count_inbound)
            node.UBC1 = UBC1
            self.list_mean_UBC1.append(UBC1)
            node = node.parent


    def simulate(self, child, sim_game: Krestik_nolik, player):

        if not isinstance(child, list) or len(child) != 2:
            raise ValueError(f"child должен быть списком из 2 элементов")
        if not isinstance(sim_game, Krestik_nolik):
            raise TypeError(f"sim_game должен быть Krestik_nolik")
        if player not in ["X", "O"]:
            raise ValueError(f"player должен быть 'X' или 'O'")
        x, y = child
        if not sim_game.make_move(x, y, player):
            raise ValueError(f"Невозможно сделать ход")

        if player == self.symbol:
            player = self.opponent_symbol
        else:
            player = self.symbol

        while sim_game.winner == None:
            random_ind = random.randint(0, len(sim_game.available_stats)-1)
            x = sim_game.available_stats[random_ind][0]
            y = sim_game.available_stats[random_ind][1]

            sim_game.make_move(x, y, player)

            if player == self.symbol:
                player = self.opponent_symbol
            else:
                player = self.symbol

        return self.evaluate_result(sim_game.winner)
        
    def find_best_move(self, game_state=None):
        
        if game_state is not None:
            self.game = copy.deepcopy(game_state)
            self.state = self.game.field
            self.root = Tree()
            self.list_mean_UBC1 = [1]

        if not hasattr(self.game, 'available_stats') or not self.game.available_stats:
            raise ValueError("Нет доступных ходов")
        if self.game.winner is not None:
            raise ValueError(f"Игра уже завершена")

        for _ in range(10000):
            self.down_to_tree()

        if not self.root.children:
            raise ValueError("MCTS не нашёл ни одного хода")

        maxi = -1
        move = None    
        for ch in self.root.children:
            if ch.count_inbound > maxi:
                maxi = ch.count_inbound
                move = ch
        
        if move is None:
            raise ValueError("Не удалось найти лучший ход")

        return move.value