import pygame
class TextBall:
    def __init__(self, x, y, radius, text, font, color, text_color=(0, 0, 0)):
        self.center = (x, y)
        self.radius = radius
        self.text = text
        self.font = font
        self.color = color
        self.text_color = text_color

        self.rect = pygame.Rect(x - radius, y - radius, radius * 2, radius * 2)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)

        pygame.draw.circle(surface, self.text_color, self.center, self.radius, 2)

        label = self.font.render(self.text, True, self.text_color)
        label_rect = label.get_rect(center=self.center)
        surface.blit(label, label_rect)