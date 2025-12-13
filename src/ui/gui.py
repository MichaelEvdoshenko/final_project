import tkinter as tk
from core.game import Krestik_nolik
from ai.bot_MCTS import MCTS_bot
from ai.bot_Q_learning import Q_learning_bot
from ai.construct_bot import bot_choice

class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики - Выбор режима")
        self.bot_choice_var = tk.StringVar(value="MCTS")
        self.size_var = tk.IntVar(value=3)
        self.turn_var = tk.StringVar(value="player")
        self.create_widgets()
    
    def create_widgets(self):
        title_label = tk.Label(self.root, text = "Выберите режим игры", font = ("Arial", 16, "bold"))
        title_label.pack(pady=20)
        
        tk.Radiobutton(self.root, text="MCTS", variable=self.bot_choice_var, value="MCTS").pack()
        tk.Radiobutton(self.root, text="Q_Learning", variable=self.bot_choice_var, value="Q_learning").pack()

        self.vs_friend_btn = tk.Button(self.root, text = "Играть с другом", 
                                      command = self.start_vs_friend, 
                                      width=20, height=2, font=("Arial", 12), bg="lightgreen")
        self.vs_friend_btn.pack(pady=10)
        
        self.vs_bot_btn = tk.Button(self.root, text="Играть с ботом", 
                                   command=self.start_vs_bot, 
                                   width=20, height=2, font=("Arial", 12), bg="lightblue")
        self.vs_bot_btn.pack(pady=10)
        
        size_frame = tk.Frame(self.root)
        size_frame.pack(pady=20)

        turn_frame = tk.Frame(self.root)
        turn_frame.pack(pady=10)
    
        tk.Label(turn_frame, text="Кто ходит первым:", font=("Arial", 12)).pack()
    
        tk.Radiobutton(turn_frame, text="Я (О)", variable=self.turn_var, value="player", font=("Arial", 10)).pack()
        tk.Radiobutton(turn_frame, text="Бот (X)", variable=self.turn_var, value="bot", font=("Arial", 10)).pack()
        
        tk.Label(size_frame, text="Размер поля:", font=("Arial", 12)).pack()
        
        sizes = [3, 4, 5]
        for size in sizes:
            rb = tk.Radiobutton(size_frame, text=f"{size}x{size}", 
                               variable=self.size_var, value=size, font=("Arial", 10))
            rb.pack()
    
    def start_vs_friend(self):
        self.clear_screen()
        KrestInterface(self.root, self.size_var.get(), "friend", None, "player")
    
    def start_vs_bot(self):
        self.clear_screen()
        selected_bot = self.bot_choice_var.get()
        size = self.size_var.get()
        first_turn = self.turn_var.get()
        
        KrestInterface(self.root, size, "bot", selected_bot, first_turn)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

class KrestInterface:
    def __init__(self, root, size=3, game_mode = "friend", selected_bot = None, first_turn = "player"):
        self.root = root
        self.size = size
        self.game_mode = game_mode
        self.selected_bot = selected_bot
        self.game = Krestik_nolik(size)
        self.first_turn = first_turn
        if game_mode == "bot":
            if self.selected_bot == "MCTS":
                self.to_move_by_bot = bot_choice(MCTS_bot, first_turn)
            else:
                self.to_move_by_bot = bot_choice(Q_learning_bot, first_turn)
        
            if first_turn == "player":
                self.current_player = "O"
                self.bot_player = "X"
            else:
                self.current_player = "X"
                self.bot_player = "X"
        else:
            self.current_player = "O"
        
        if game_mode == "friend":
            mode_text = "с другом" 
        else:
            mode_text = "с ботом"
        self.root.title(f"Крестики-нолики {size}x{size} ({mode_text})")
        
        self.create_interface()
    
    def create_interface(self):
        back_btn = tk.Button(self.root, text="Назад", command=self.back_to_menu, font=("Arial", 10), bg="lightgray")
        back_btn.pack(anchor="nw", padx=10, pady=10)
        
        self.table_frame = tk.Frame(self.root, bg="lightgray", borderwidth=2, relief="solid")
        self.table_frame.pack(expand=True, padx=20, pady=20)
        
        self.buttons = []
        for i in range(self.size):
            row_buttons = []
            for j in range(self.size):
                btn = tk.Button(self.table_frame, width=6, height=3, text=" ", state="normal", bg="white", command=lambda row=i, col=j: self.on_button_click(row, col))
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)
        
        self.status_label = tk.Label(self.root, text=f"Сейчас ходит: {self.current_player}", font=("Arial", 14))
        self.status_label.pack(pady=10)
        
        if self.game_mode == "bot" and self.first_turn == "bot":
            self.root.after(100, self.bot_move)

        self.restart_button = tk.Button(self.root, text="Новая игра", command=self.restart_game, font=("Arial", 12), bg="lightblue")
        self.restart_button.pack(pady=10)
    
    def back_to_menu(self):
        self.clear_screen()
        StartScreen(self.root)
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def switch_player(self):
        if self.current_player == "O":
            self.current_player = "X" 
        else:
            self.current_player = "O"
        self.status_label.config(text=f"Сейчас ходит: {self.current_player}")

    def on_button_click(self, row, col):
        if self.game_mode == "bot" and self.current_player == self.bot_player:
            return
            
        if self.buttons[row][col]['text'] != " ":
            return
            
        if self.game.winner != None:
            return
        
        self.game.make_move(row, col, self.current_player)
        self.buttons[row][col].config(text=self.current_player)
        self.check_game_state()
        
        if self.game.winner is None:
            if self.game_mode == "bot":
                self.current_player = self.bot_player
                self.status_label.config(text=f"Сейчас ходит: {self.current_player}")
                self.root.after(500, self.bot_move)
            else:
                self.switch_player()
    
    def bot_move(self):
        if self.selected_bot == "MCTS":
            row, col = self.to_move_by_bot.to_do_move(self.game)
        else:
            row, col = self.to_move_by_bot.to_do_move(self.game)
        
        self.game.make_move(row, col, self.bot_player)
        self.buttons[row][col].config(text=self.bot_player)
        self.check_game_state()

        if self.game.winner is None:
            if self.bot_player == "X":
                self.current_player = "O"
            else:
                self.current_player = "X"
            self.status_label.config(text=f"Сейчас ходит: {self.current_player}")
    
    def check_game_state(self):
        if self.game.winner == "НИЧЬЯ":
            self.status_label.config(text="Ничья! Игра окончена.", fg="blue")
            self.disable_all_buttons()
        elif self.game.winner is not None:
            self.status_label.config(text=f"Победил: {self.game.winner}!", fg="green")
            self.disable_all_buttons()
    
    def disable_all_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(state="disabled")
    
    def restart_game(self):
        self.game = Krestik_nolik(self.size)
        if self.game_mode == "bot":
            if self.first_turn == "player":
                self.current_player = "O"
                self.bot_player = "X"
            else:
                self.current_player = "X"
                self.bot_player = "X"
                self.root.after(500, self.bot_move)
        else:
            self.current_player = "O"

        self.status_label.config(text=f"Сейчас ходит: {self.current_player}", fg="black")
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(text=" ", state="normal", bg="white")
