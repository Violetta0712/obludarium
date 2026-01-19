import classes.ux.Button as button
import classes.logic.Game as game
import pygame
class GameScene():
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, players):
        self.running = True
        self.state = 'local_game'
        back_b_width = SCREEN_WIDTH // 6
        back_b_height = SCREEN_HEIGHT // 12
        back_b_x = back_b_width // 4
        back_b_y = back_b_height // 2
        self.back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "Back", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
        self.local_game = game.Game(players)
        print(players)
    def update(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.back_button.is_clicked(event):
                self.state = "local_game_menu"
        screen.fill((30, 30, 30))
        self.back_button.draw(screen)
        pygame.display.flip()





def draw_game(screen, SCREEN_WIDTH, SCREEN_HEIGHT, players):
    running = True
    state = 'local_game'
    b_width = SCREEN_HEIGHT // 4
    b_height = SCREEN_HEIGHT // 12
    b_x = (SCREEN_WIDTH - b_width) // 2
    b_y = (SCREEN_HEIGHT - b_height) //2
    back_b_width = SCREEN_WIDTH // 6
    back_b_height = SCREEN_HEIGHT // 12
    back_b_x = back_b_width // 4
    back_b_y = back_b_height // 2
    back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "Back", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    local_game = game.Game(players)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif back_button.is_clicked(event):
                running = False
                state = "local_game_menu"
            screen.fill((30, 30, 30))
            back_button.draw(screen)
            pygame.display.flip()
    return state, players