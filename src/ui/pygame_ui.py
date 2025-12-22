import pygame
import sys
from src.ui.renderer import Renderer
from src.ui.event_handler import EventHandler
from src.ui.Button import Button
from src.ui.RadioButton import RadioButton
from src.core.game import Krestik_nolik
from src.ai.construct_bot import bot_choice


class GameInterface:
    def __init__(self,
                 screen,
                 size=3,
                 game_mode="friend",
                 selected_bot=None,
                 first_turn="player"):
        self.screen = screen
        self.size = size
        self.game_mode = game_mode
        self.selected_bot = selected_bot
        self.first_turn = first_turn
        self.game = Krestik_nolik(size)

        self.current_player = "O"
        self.bot_player = None
        self.bot = None
        self.bot_move_delayed = False
        self.bot_thinking = False
        self.bot_timer = 0

        if game_mode == "bot":
            if self.selected_bot == "MCTS":
                self.bot = bot_choice("MCTS", first_turn)
            else:
                self.bot = bot_choice("Q_learning", first_turn)

            if first_turn == "player":
                self.current_player = "O"
                self.bot_player = "X"
            else:
                self.current_player = "X"
                self.bot_player = "X"
                self.bot_move_delayed = True
        else:
            self.current_player = "O"
            self.bot_player = None
            self.bot_move_delayed = False

        self.back_btn = Button(20, 20, 100, 40, "В меню")
        self.restart_btn = Button(680, 20, 100, 40, "Новая игра")

        CELL_SIZE = 100
        MARGIN = 10
        self.board_width = size * CELL_SIZE + (size - 1) * MARGIN
        self.board_height = size * CELL_SIZE + (size - 1) * MARGIN
        self.board_x = (800 - self.board_width) // 2
        self.board_y = (700 - self.board_height) // 2 + 50

    def get_cell_at_pos(self, pos):
        x, y = pos
        CELL_SIZE = 100
        MARGIN = 10

        board_right = self.board_x + self.board_width
        board_bottom = self.board_y + self.board_height
        x_in_range = self.board_x <= x <= board_right
        y_in_range = self.board_y <= y <= board_bottom

        if x_in_range and y_in_range:
            rel_x = x - self.board_x
            rel_y = y - self.board_y

            col = rel_x // (CELL_SIZE + MARGIN)
            row = rel_y // (CELL_SIZE + MARGIN)

            cell_x = rel_x % (CELL_SIZE + MARGIN)
            cell_y = rel_y % (CELL_SIZE + MARGIN)

            if cell_x < CELL_SIZE and cell_y < CELL_SIZE:
                if row < self.size and col < self.size:
                    return row, col

        return None

    def make_move(self, row, col, player):
        self.game.make_move(row, col, player)

        if self.game_mode == "friend":
            self.switch_player()
        else:
            if self.game_mode == "bot":
                if player != self.bot_player:
                    if self.game.winner is None:
                        self.current_player = self.bot_player
                        self.bot_thinking = True
                        self.bot_timer = pygame.time.get_ticks()

    def switch_player(self):
        if self.current_player == "O":
            self.current_player = "X"
        else:
            self.current_player = "O"

    def bot_move(self):
        if not self.bot_thinking:
            return

        current_time = pygame.time.get_ticks()
        time_difference = current_time - self.bot_timer
        if time_difference > 500:
            row, col = self.bot.to_do_move(self.game)
            self.make_move(row, col, self.bot_player)
            self.bot_thinking = False

            if self.game.winner is None:
                if self.bot_player == "X":
                    self.current_player = "O"
                else:
                    self.current_player = "X"

    def restart_game(self):
        self.game = Krestik_nolik(self.size)

        if self.game_mode == "bot":
            if self.first_turn == "player":
                self.current_player = "O"
                self.bot_player = "X"
                self.bot_thinking = False
                self.bot_move_delayed = False
            else:
                self.current_player = "X"
                self.bot_player = "X"
                self.bot_thinking = True
                self.bot_move_delayed = True
                self.bot_timer = pygame.time.get_ticks()
        else:
            self.current_player = "O"
            self.bot_thinking = False
            self.bot_move_delayed = False

    def update(self):
        if self.bot_move_delayed:
            self.bot_move_delayed = False
            self.bot_thinking = True
            self.bot_timer = pygame.time.get_ticks()

        if self.bot_thinking:
            self.bot_move()


class PyGameUI:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 700
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Крестики-нолики")
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.renderer = Renderer(self.screen)
        self.event_handler = EventHandler()

        self.current_screen = "start"
        self.start_screen_elements = self._create_start_screen_elements()
        self.game_interface = None
        self.running = True

    def _create_start_screen_elements(self):
        bot_radio_group = []
        size_radio_group = []
        turn_radio_group = []

        elements = {}
        elements['bot_choice'] = "MCTS"
        elements['size'] = 3
        elements['first_turn'] = "player"

        elements['vs_friend_btn'] = Button(280, 308,
                                           240, 50,
                                           "Играть с другом",
                                           (255, 255, 255))
        elements['vs_bot_btn'] = Button(280, 378,
                                        240, 50,
                                        "Играть с ботом",
                                        (255, 255, 255))
        elements['back_btn'] = Button(20, 20, 100, 40, "Выход")

        elements['bot_radio_group'] = bot_radio_group
        elements['size_radio_group'] = size_radio_group
        elements['turn_radio_group'] = turn_radio_group

        elements['mcts_rb'] = RadioButton(280, 245,
                                          "MCTS бот",
                                          bot_radio_group,
                                          True,
                                          "MCTS")
        elements['qlearning_rb'] = RadioButton(280, 280,
                                               "Q-learning бот",
                                               bot_radio_group,
                                               False,
                                               "Q_learning")

        sizes = [3, 4, 5]
        base_x = 400
        size_buttons = []
        for i in range(len(sizes)):
            size = sizes[i]
            x = base_x + (i - 1) * 80
            is_selected = False
            if size == 3:
                is_selected = True
            rb = RadioButton(x, 490,
                             f"{size}x{size}",
                             size_radio_group,
                             is_selected, size)
            size_buttons.append((rb, size))
        elements['size_buttons'] = size_buttons

        elements['player_first_rb'] = RadioButton(280, 560,
                                                  "Я хожу первым (O)",
                                                  turn_radio_group,
                                                  True, "player")
        elements['bot_first_rb'] = RadioButton(280, 595,
                                               "Бот ходит первым (X)",
                                               turn_radio_group, False, "bot")

        return elements

    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break

                if self.current_screen == "start":
                    result = self.event_handler.handle_start_screen_events(
                        event, self.start_screen_elements, mouse_pos
                    )
                    self._handle_start_screen_result(result)

                elif self.current_screen == "game":
                    result = self.event_handler.handle_game_events(
                        event, self.game_interface, mouse_pos
                    )
                    self._handle_game_result(result)

            self._update()
            self._draw()

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def _handle_start_screen_result(self, result):
        if result == "friend":
            self.game_interface = self._create_game_interface("friend")
            self.current_screen = "game"
        else:
            if result == "bot":
                self.game_interface = self._create_game_interface("bot")
                self.current_screen = "game"
            else:
                if result == "exit":
                    self.running = False

    def _handle_game_result(self, result):
        if result == "back":
            self.current_screen = "start"
            self.game_interface = None

    def _create_game_interface(self, game_mode):
        size = self.start_screen_elements['size']
        selected_bot = self.start_screen_elements['bot_choice']
        first_turn = self.start_screen_elements['first_turn']

        return GameInterface(
            self.screen, size, game_mode, selected_bot, first_turn
        )

    def _update(self):
        if self.current_screen == "game":
            if self.game_interface:
                self.game_interface.update()

    def _draw(self):
        if self.current_screen == "start":
            self.renderer.draw_start_screen(self.start_screen_elements)
        else:
            if self.current_screen == "game":
                if self.game_interface:
                    self.renderer.draw_game_interface(self.game_interface)
