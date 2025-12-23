import pygame
from typing import Tuple

WHITE = (255, 255, 255)
BLUE = (190, 230, 240)
DARK_BLUE = (30, 40, 80)


class Button:
    def __init__(self,
                 x: int,
                 y: int,
                 width: int,
                 height: int,
                 text: str,
                 color: Tuple[int, int, int] = WHITE,
                 hover_color: Tuple[int, int, int] = BLUE) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font_size = 25
        self.font = pygame.font.Font(
            "assets/Zubilo.otf",
            self.font_size
        )
        self.is_hovered = False
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen,
                         self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, DARK_BLUE, self.rect, 2, border_radius=10)

        text_surf = self.font.render(self.text, True, DARK_BLUE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, pos: Tuple[int, int]) -> bool:
        self.is_hovered = self.rect.collidepoint(pos)
        if self.is_hovered:
            self.current_color = self.hover_color
        else:
            self.current_color = self.color
        return self.is_hovered

    def is_clicked(self,
                   pos: Tuple[int, int],
                   event: pygame.event.Event) -> bool:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return self.rect.collidepoint(pos)
        return False
