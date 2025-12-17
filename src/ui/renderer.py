import pygame

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH = 800
        self.HEIGHT = 700
        self.ring_image = None
        try:
            self.ring_image = pygame.image.load('assets/ring2.png').convert_alpha()
            self.ring_image = pygame.transform.scale(self.ring_image, (80, 80))
        except:
            self.ring_image = None
        
    def draw_ring(self, x, y, size):
        if self.ring_image:
            img_rect = self.ring_image.get_rect(center=(x, y))
            self.screen.blit(self.ring_image, img_rect)
        else:
            pygame.draw.circle(self.screen, (212, 175, 55), (x, y), size//2 - 5, 8)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), size//2 - 15)
            pygame.draw.circle(self.screen, (255, 245, 200, 180), (x - size//8, y - size//8), size//12)

    def draw_start_screen(self, screen_elements):
        self.screen.fill((255, 255, 255))
        
        title_font = pygame.font.Font(None, 48)
        title = title_font.render("Крестики-нолики", True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.WIDTH//2, 105))
        self.screen.blit(title, title_rect)
        
        label_font = pygame.font.Font(None, 36)
        subtitle = label_font.render("Выберите режим игры", True, (0, 0, 0))
        subtitle_rect = subtitle.get_rect(center=(self.WIDTH//2, 154))
        self.screen.blit(subtitle, subtitle_rect)
        
        bot_label = label_font.render("Тип бота:", True, (0, 0, 0))
        bot_label_rect = bot_label.get_rect(midright=(264, 245))
        self.screen.blit(bot_label, bot_label_rect)
        
        element_list = [
            screen_elements.get('mcts_rb'),
            screen_elements.get('qlearning_rb'),
            screen_elements.get('vs_friend_btn'),
            screen_elements.get('vs_bot_btn'),
            screen_elements.get('back_btn'),
            screen_elements.get('size_buttons'),
            screen_elements.get('player_first_rb'),
            screen_elements.get('bot_first_rb'),
        ]
        
        for element in element_list:
            if element is not None:
                if isinstance(element, list):
                    for item_pair in element:
                        if hasattr(item_pair[0], 'draw'):
                            item_pair[0].draw(self.screen)
                else:
                    if hasattr(element, 'draw'):
                        element.draw(self.screen)
        
        size_label = label_font.render("Размер поля:", True, (0, 0, 0))
        size_label_rect = size_label.get_rect(center=(self.WIDTH//2, 455))
        self.screen.blit(size_label, size_label_rect)
        
        turn_label = label_font.render("Кто ходит первым:", True, (0, 0, 0))
        turn_label_rect = turn_label.get_rect(center=(self.WIDTH//2, 525))
        self.screen.blit(turn_label, turn_label_rect)
    
    def draw_game_interface(self, game_interface):
        self.screen.fill((255, 255, 255))
        
        if game_interface.game_mode == "friend":
            mode_text = "с другом"
        else:
            mode_text = "с ботом"
        
        title_font = pygame.font.Font(None, 48)
        title_text = f"Крестики-нолики {game_interface.size}x{game_interface.size} ({mode_text})"
        title = title_font.render(title_text, True, (0, 0, 0))
        title_rect = title.get_rect(center=(self.WIDTH//2, 50))
        self.screen.blit(title, title_rect)
        
        game_interface.back_btn.draw(self.screen)
        game_interface.restart_btn.draw(self.screen)
        
        status_font = pygame.font.Font(None, 36)
        
        if game_interface.game.winner == "НИЧЬЯ":
            status_text = "Ничья! Игра окончена."
            color_value = (0, 0, 0)
        else:
            if game_interface.game.winner is not None:
                status_text = f"Победил: {game_interface.game.winner}!"
                color_value = (0, 0, 0)
            else:
                if game_interface.bot_thinking:
                    status_text = "Бот думает..."
                    color_value = (0, 0, 0)
                else:
                    status_text = f"Сейчас ходит: {game_interface.current_player}"
                    color_value = (0, 0, 0)
            
        status = status_font.render(status_text, True, color_value)
        status_rect = status.get_rect(center=(self.WIDTH//2, 100))
        self.screen.blit(status, status_rect)
        
        CELL_SIZE = 100
        MARGIN = 10
        
        for row in range(game_interface.size):
            for col in range(game_interface.size):
                x = game_interface.board_x + col * (CELL_SIZE + MARGIN)
                y = game_interface.board_y + row * (CELL_SIZE + MARGIN)
                
                cell_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (255, 255, 255), cell_rect, border_radius=5)
                pygame.draw.rect(self.screen, (0, 0, 0), cell_rect, 2, border_radius=5)
                
                cell_value = game_interface.game.field[row][col]
                if cell_value != ' ':
                    color_value = (0, 0, 0)
                    line_width = 5
                    
                    if cell_value == 'X':
                        offset = 15
                        pygame.draw.line(self.screen, color_value, (x + offset, y + offset), (x + CELL_SIZE - offset, y + CELL_SIZE - offset), line_width)
                        pygame.draw.line(self.screen, color_value, (x + CELL_SIZE - offset, y + offset), (x + offset, y + CELL_SIZE - offset), line_width)
                    else:
                        center_x = x + CELL_SIZE // 2
                        center_y = y + CELL_SIZE // 2
                        self.draw_ring(center_x, center_y, CELL_SIZE)