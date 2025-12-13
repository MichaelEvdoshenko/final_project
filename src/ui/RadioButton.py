import pygame

class RadioButton:
    def __init__(self, x, y, text, group=None, is_selected=False, value=None):
        self.x = x
        self.y = y
        self.text = text
        self.is_selected = is_selected
        self.group = []
        if value is not None:
            self.value = value
        else:
            self.value = text
        self.hover_color = (255, 255, 255)
        self.normal_color = (255, 255, 255)
        self.is_hovered = False
        self.font_size = 28
        self.radius = 10
        self.click_area = pygame.Rect(x - 20, y - 20, 40, 40)
        
        if group is not None:
            self.group = group
            group.append(self)
            
            if is_selected:
                for rb in self.group:
                    if rb != self:
                        rb.is_selected = False
        else:
            if is_selected:
                self.is_selected = True
        
    def draw(self, screen):
        if self.is_hovered:
            pygame.draw.circle(screen, self.hover_color, (self.x, self.y), self.radius + 5)
        
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius, 2)
        
        if self.is_selected:
            pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius - 4)
        
        font = pygame.font.Font(None, self.font_size)
        text_surf = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surf.get_rect(midleft=(self.x + self.radius + 10, self.y))
        screen.blit(text_surf, text_rect)
    
    def check_hover(self, pos):
        self.is_hovered = self.click_area.collidepoint(pos)
        return self.is_hovered
        
    def check_click(self, pos, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.click_area.collidepoint(pos):
                    for rb in self.group:
                        rb.is_selected = False
                    self.is_selected = True
                    return True
        return False