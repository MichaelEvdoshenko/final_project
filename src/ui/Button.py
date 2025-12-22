import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Button:
    def __init__(self,
                 x,
                 y,
                 width,
                 height,
                 text,
                 color=WHITE,
                 hover_color=WHITE):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font_size = 32
        self.is_hovered = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen):
        pygame.draw.rect(screen,
                         self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 2, border_radius=10)

        font = pygame.font.Font(None, self.font_size)
        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered:
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        return self.is_hovered

    def is_clicked(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(pos)
        return False
