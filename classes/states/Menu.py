import classes.ux.Button as button
import pygame
class Menu():
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH):
        self.running = True
        self.state = "menu"
        self.buttons = []
        b_width = SCREEN_HEIGHT // 4
        b_height = SCREEN_HEIGHT // 12
        b_interval = SCREEN_HEIGHT // 20
        b_number = 2
        b_x = (SCREEN_WIDTH - b_width) // 2
        b_y = (SCREEN_HEIGHT - (b_number * b_height + (b_number - 1) * b_interval)) // 2
        self.local_button = button.Button(b_x, b_y, b_width, b_height, "Hra", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))  
        self.buttons.append(self.local_button)
        b_y = b_y + b_height + b_interval
        self.quit_button = button.Button(b_x, b_y, b_width, b_height, "Ukončit", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.quit_button)

    def update(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.quit_button.is_clicked(event):
                self.running = False
            elif self.local_button.is_clicked(event):
                self.state = "local_game_menu"

            screen.fill((168, 150, 150))
            for b in self.buttons:
                b.draw(screen)
            pygame.display.flip()

