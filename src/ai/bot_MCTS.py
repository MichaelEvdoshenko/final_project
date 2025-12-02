from core.game import Krestik_nolik
from core.tree import Tree
import random
import copy
import math

class MCTS_bot():
    def __init__(self, game_state: Krestik_nolik):
        self.game = copy.deepcopy(game_state)
        self.state = self.game.field
        self.root = Tree(self.state)
    
    def down_to_tree(self):
        node = self.root
        sup_game = copy.deepcopy(self.game)
        player = "X"
        
        while node.children and len(node.children) == len(sup_game.available_stats) and sup_game.winner == None:
            maximal_UBC1 = max(child.UBC1 for child in node.children)
            for ch in node.children:
                if ch.UBC1 == maximal_UBC1:
                    next_node = ch
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
                    UBC1 = float('inf') 
                    ch = Tree(value = child, count_win = prohod, count_inbound = 1, UBC1 = UBC1)
                    node.add_child(ch)
                    break
        else:
            if sup_game.winner == "X":
                prohod = 1
            elif sup_game.winner == "НИЧЬЯ":
                prohod = 0.5
            else:
                prohod = 0

        while node.parent != None:
            node.count_win += prohod
            node.count_inbound += 1
            UBC1 = (node.count_win/node.count_inbound) + math.sqrt(2*math.log(node.parent.count_inbound + 1)/node.count_inbound)
            node.UBC1 = UBC1
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

        if sim_game.winner == "X":
            return 1
        elif sim_game.winner == "НИЧЬЯ":
            return 0.5
        else:
            return 0
        
    def find_best_move(self):
        for ch in self.game.available_stats:
            support_game = copy.deepcopy(self.game)
            support_game.make_move(ch[0], ch[1], "X")
            if support_game.winner == "X":
                return ch
            
        for ch in self.game.available_stats:
            support_game = copy.deepcopy(self.game)
            support_game.make_move(ch[0], ch[1], "O")
            if support_game.winner == "O":
                return ch
        
        for _ in range(10000):
            self.down_to_tree()
        maxi = -1
        move = [-1, -1]    
        for ch in self.root.children:
            if ch.count_inbound > maxi:
                maxi = ch.count_inbound
                move = ch
        return move.value