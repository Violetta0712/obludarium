import classes.ux.Button as button
import classes.logic.Game as game
import classes.states.Displays as dis
import pygame
class GameScene():
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, players):
        self.running = True
        self.state = 'local_game'
        self.local_game = game.Game(players)
        self.local_game.start_round()
        self.s_height = SCREEN_HEIGHT
        self.s_width = SCREEN_WIDTH
        self.scene = dis.Season(self.s_height, self.s_width,self.state, self.local_game, self.local_game.season)
    def update(self, screen):
        for event in pygame.event.get():
            self.scene = self.scene.check(event)
        self.state = self.scene.state
        self.running = self.scene.running
        screen.fill((168, 150, 150))
        self.scene.draw(screen)
        pygame.display.flip()





