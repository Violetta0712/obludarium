import classes.ux.Button as button
import pygame
class Display:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state):
        self.running = True
        self.state = state
        back_b_width = SCREEN_WIDTH // 6
        back_b_height = SCREEN_HEIGHT // 12
        back_b_x = back_b_width // 4
        back_b_y = back_b_height // 2
        self.back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "Back", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    
    def check(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif self.back_button.is_clicked(event):
            self.state = "local_game_menu"
    def draw(self, screen):
        self.back_button.draw(screen)