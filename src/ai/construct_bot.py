from ai.bot_Q_learning import Q_learning_bot
from ai.bot_MCTS import MCTS_bot
from core.game import Krestik_nolik

class bot_choice():
    def __init__(self, bot_name, first_turn):
        self.bot_name = bot_name
        self.first_turn = first_turn
        self.predict = False

    def to_do_move(self, game: Krestik_nolik):
        if (self.predict == False and self.bot_name == Q_learning_bot): 
            self.bot_name.learn(self.first_turn)
            self.predict = True

        if (self.bot_name == Q_learning_bot):
            return self.bot_name.find_best_move(game)
        
        if (self.bot_name == MCTS_bot):
            bot_instance = MCTS_bot(game)
            return bot_instance.find_best_move()