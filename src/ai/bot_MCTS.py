from core.game import Krestik_nolik
from core.tree import Tree
import random
import copy
import math

class MCTS_bot():
    def __init__(self, game_state: Krestik_nolik):
        self.game = copy.deepcopy(game_state)
        self.state = self.game.field
        self.root = Tree()
        self.bot_symbol = "X"
        self.player_symbol = "O"
        self.list_mean_UBC1 = [1]
    
    def evaluate_result(self, winner):
        if winner == self.bot_symbol:
            return 1
        elif winner == "НИЧЬЯ":
            return 0.5
        else:
            return 0

    def down_to_tree(self):
        node = self.root
        sup_game = copy.deepcopy(self.game)
        player = "X"
        
        while node.children and len(node.children) == len(sup_game.available_stats) and sup_game.winner == None:
            if random.random() < 0.25:
                next_node = random.choice(node.children)
            else:
                maximal_UBC1 = max(child.UBC1 for child in node.children)
                candidates = [ch for ch in node.children if ch.UBC1 == maximal_UBC1]
                next_node = random.choice(candidates)
            node = next_node
            sup_game.make_move(next_node.value[0], next_node.value[1], player)
            if player == "X":
                player = "O"
            else:
                player = "X"

        if sup_game.winner == None:
            used_children_coord = [child.value for child in node.children]
            for child in sup_game.available_stats:
                if child not in used_children_coord:
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
        sim_game.make_move(child[0], child[1], player)
        if player == "X":
            player = "O"
        else:
            player = "X"

        while sim_game.winner == None:
            random_ind = random.randint(0, len(sim_game.available_stats)-1)
            x = sim_game.available_stats[random_ind][0]
            y = sim_game.available_stats[random_ind][1]

            sim_game.make_move(x, y, player)

            if player == "X":
                player = "O"
            else:
                player = "X"

        return self.evaluate_result(sim_game.winner)
        
    def find_best_move(self):
        for _ in range(10000):
            self.down_to_tree()
        maxi = -1
        move = [-1, -1]    
        for ch in self.root.children:
            if ch.count_inbound > maxi:
                maxi = ch.count_inbound
                move = ch
        return move.value