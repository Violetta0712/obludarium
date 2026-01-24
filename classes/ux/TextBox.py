import pygame

class TextBox:
    def __init__(self, x, y, width, height, text, font, color, text_color=(0,0,0)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color
 
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, border_radius=10)
        pygame.draw.rect(surface, self.text_color, self.rect, 2, border_radius=10)

        
        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)