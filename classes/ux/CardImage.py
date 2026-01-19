import pygame
import params as p

class CardImage:
    def __init__(self, x, y, width, cardid):
        self.path = (p.IMG_DIR / cardid).with_suffix(p.img_format)
        height = width * 13/9
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(str(self.path)).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)