import classes.ux.Button as button
import classes.logic.Game as game
import classes.states.Displays as dis
import pygame
class GameScene():
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, players):
        self.running = True
        self.state = 'local_game'
        self.phase = 'season'
        self.local_game = game.Game(players)
        self.local_game.start_round()
        self.s_height = SCREEN_HEIGHT
        self.s_width = SCREEN_WIDTH
    def update(self, screen):
        match self.phase:
            case 'season':
                self.scene = dis.Season(self.s_height, self.s_width,self.state, self.phase, self.local_game.season,  )
            case 'turn':
                self.scene = dis.Display(self.s_height, self.s_width,self.state, self.phase)

        for event in pygame.event.get():
            self.scene.check(event)
        self.phase = self.scene.phase
        self.state = self.scene.state
        self.running = self.scene.running
        screen.fill((30, 30, 30))
        self.scene.draw(screen)
        pygame.display.flip()





