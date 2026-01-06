import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, idle_color, hover_color, text_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()

        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.idle_color

        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.text_color, self.rect, 2, border_radius=10)

        
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)

    def is_clicked(self):
        return self.rect.collidepoint(pygame.mouse.get_pos()) and pygame.mouse.get_pressed()[0]