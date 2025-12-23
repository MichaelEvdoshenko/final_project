import pygame
from typing import Dict, Any, Optional, List


class Renderer:
    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.WIDTH = 800
        self.HEIGHT = 700

        try:
            fallback_original = pygame.image.load("assets/ring2.png").convert_alpha()
            self.fallback_image: Optional[pygame.Surface] = pygame.transform.scale(
                fallback_original, (80, 80)
            )
        except FileNotFoundError:
            self.fallback_image = None

        try:
            bg_original = pygame.image.load("assets/main_back.png")
            self.start_bg: Optional[pygame.Surface] = pygame.transform.scale(
                bg_original, (self.WIDTH, self.HEIGHT)
            )
        except FileNotFoundError:
            self.start_bg = None

        try:
            game_bg_original = pygame.image.load("assets/main_back.png")
            self.game_bg = pygame.transform.scale(
                game_bg_original, (self.WIDTH, self.HEIGHT)
            )
        except FileNotFoundError:
            self.game_bg = None


        self.ball_images: List[pygame.Surface] = []
        for i in range(5):
            try:
                img = pygame.image.load(f"assets/balls/ball_{i}.png").convert_alpha()
                img = pygame.transform.scale(img, (80, 80))
                self.ball_images.append(img)
            except FileNotFoundError:
                break

    def draw_fallback(self, x: int, y: int, size: int) -> None:
        if self.fallback_image:
            img_rect = self.fallback_image.get_rect(center=(x, y))
            self.screen.blit(self.fallback_image, img_rect)
        else:
            pygame.draw.circle(self.screen, (212, 175, 55), (x, y), size // 2 - 5, 8)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size // 2 - 15)
            pygame.draw.circle(
                self.screen,
                (255, 245, 200, 180),
                (x - size // 8, y - size // 8),
                size // 12,
            )

    def draw_start_screen(self, screen_elements: Dict[str, Any]) -> None:
        if self.start_bg:
            self.screen.blit(self.start_bg, (0, 0))
        else:
            self.screen.fill((255, 255, 255))

        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Крестики-нолики", True, (30, 40, 80))
        title_rect = title.get_rect(center=(self.WIDTH // 2, 105))
        self.screen.blit(title, title_rect)

        label_font = pygame.font.Font(None, 36)
        subtitle = label_font.render("Выберите режим игры", True, (30, 40, 80))
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH // 2, 154))
        self.screen.blit(subtitle, subtitle_rect)

        bot_label = label_font.render("Тип бота:", True, (30, 40, 80))
        bot_label_rect = bot_label.get_rect(midright=(264, 245))
        self.screen.blit(bot_label, bot_label_rect)

        element_list = [
            screen_elements.get("mcts_rb"),
            screen_elements.get("qlearning_rb"),
            screen_elements.get("vs_friend_btn"),
            screen_elements.get("vs_bot_btn"),
            screen_elements.get("back_btn"),
            screen_elements.get("size_buttons"),
            screen_elements.get("player_first_rb"),
            screen_elements.get("bot_first_rb"),
        ]

        for element in element_list:
            if element is not None:
                if isinstance(element, list):
                    for item_pair in element:
                        if hasattr(item_pair[0], "draw"):
                            item_pair[0].draw(self.screen)
                else:
                    if hasattr(element, "draw"):
                        element.draw(self.screen)

        size_label = label_font.render("Размер поля:", True, (30, 40, 80))
        size_label_rect = size_label.get_rect(center=(self.WIDTH // 2, 455))
        self.screen.blit(size_label, size_label_rect)

        turn_label = label_font.render("Кто ходит первым:", True, (30, 40, 80))
        turn_label_rect = turn_label.get_rect(center=(self.WIDTH // 2, 525))
        self.screen.blit(turn_label, turn_label_rect)

    def draw_game_interface(self, game_interface: Any) -> None:
        if self.game_bg:
            self.screen.blit(self.game_bg, (0, 0))
        else:
            self.screen.fill((255, 255, 255))


        if game_interface.game_mode == "friend":
            mode_text = "с другом"
        else:
            mode_text = "с ботом"

        title_font = pygame.font.Font(None, 48)
        title_text = (
            f"Крестики-нолики {game_interface.size}x{game_interface.size} ({mode_text})"
        )
        title = title_font.render(title_text, True, (30, 40, 80))
        title_rect = title.get_rect(center=(self.WIDTH // 2, 50))
        self.screen.blit(title, title_rect)

        game_interface.back_btn.draw(self.screen)
        game_interface.restart_btn.draw(self.screen)

        status_font = pygame.font.Font(None, 36)

        if game_interface.game.winner == "НИЧЬЯ":
            status_text = "Ничья! Игра окончена."
            color_value = (30, 40, 80)
        else:
            if game_interface.game.winner is not None:
                status_text = f"Победил: {game_interface.game.winner}!"
                color_value = (30, 40, 80)
            else:
                if game_interface.bot_thinking:
                    status_text = "Бот думает..."
                    color_value = (30, 40, 80)
                else:
                    status_text = f"Сейчас ходит: {game_interface.current_player}"
                    color_value = (30, 40, 80)

        status = status_font.render(status_text, True, color_value)
        status_rect = status.get_rect(center=(self.WIDTH // 2, 100))
        self.screen.blit(status, status_rect)

        CELL_SIZE = 100
        MARGIN = 10

        for row in range(game_interface.size):
            for col in range(game_interface.size):
                x = game_interface.board_x + col * (CELL_SIZE + MARGIN)
                y = game_interface.board_y + row * (CELL_SIZE + MARGIN)

                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, border_radius=5)
                pygame.draw.rect(self.screen, (30, 40, 80), cell_rect, 2, border_radius=5)

                cell_value = game_interface.game.field[row][col]
                if cell_value != " ":
                    color_value = (30, 40, 80)
                    line_width = 5

                    if cell_value == "X":
                        offset = 15
                        pygame.draw.line(
                            self.screen,
                            color_value,
                            (x + offset, y + offset),
                            (x + CELL_SIZE - offset, y + CELL_SIZE - offset),
                            line_width,
                        )
                        pygame.draw.line(
                            self.screen,
                            color_value,
                            (x + CELL_SIZE - offset, y + offset),
                            (x + offset, y + CELL_SIZE - offset),
                            line_width,
                        )
                    else:
                        center_x = x + CELL_SIZE // 2
                        center_y = y + CELL_SIZE // 2

                        idx = game_interface.o_skins[row][col]
                        if idx is not None and self.ball_images:
                            img = self.ball_images[idx % len(self.ball_images)]
                            rect = img.get_rect(center=(center_x, center_y))
                            self.screen.blit(img, rect)
                        else:
                            self.draw_fallback(center_x, center_y, CELL_SIZE)
