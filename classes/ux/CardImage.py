import pygame
import params as p

class CardImage:
    def __init__(self, x, y, width, cardid, radius=14, border_color=(0,0,0), border_thickness=6):
        self.path = (p.IMG_DIR / cardid).with_suffix(p.img_format)

        height = int(width * 13 / 9)
        self.rect = pygame.Rect(x, y, width, height)

        image = pygame.image.load(str(self.path)).convert_alpha()
        image = pygame.transform.smoothscale(image, self.rect.size)

        mask = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        pygame.draw.rect(
            mask,
            (255, 255, 255, 255),
            mask.get_rect(),
            border_radius=radius
        )

        image.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        self.image = image

        self.radius = radius
        self.border_color = border_color
        self.border_thickness = border_thickness

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

        pygame.draw.rect(
            surface,
            self.border_color,
            self.rect,
            width=self.border_thickness,
            border_radius=self.radius
        )
