import functions.functions as f
import pandas as pd
import json
import random 
import params as p
import functions as u
import pygame
import sys
import classes.ux.Button as button
import classes.ux.TextBox as textbox
import classes.logic.Card as card
import classes.logic.Deck as deck
import classes.logic.Player as player
import classes.ux.TextBall as textball

class Display:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state):
        self.running = True
        self.state = state
        self.s_height = SCREEN_HEIGHT
        self.s_width = SCREEN_WIDTH
        self.offset = SCREEN_HEIGHT //24
        back_b_width = self.offset
        back_b_height = self.offset
        back_b_x = 0
        back_b_y = 0
        self.back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "x", pygame.font.SysFont(None, 36), (180, 60, 60), (220, 90, 90))
        results = [[87, 46, 5, 3, 6, -15], [90, 60, 6, 2, 10, -10], [21, 46, 5, 3, 6, -65]]
        order = [1, 0, 2]
        x = self.s_width /4
        y = 0
        w = x*2
        h = self.s_height/10
        self.visuals = []
        self.visuals.append(textbox.TextBox(x, y, w,h, 'Výsledky', pygame.font.SysFont('gabriola', 46), (128, 128, 128), (255, 215, 0) ))
        y += h
        for o in range(len(order)):
            xi = x
            self.visuals.append(textbox.TextBox(xi, y, w/10,h, str(o+1), pygame.font.SysFont('gabriola', 46), (255, 215, 0), (128, 128, 128) ))
            xi += w/10
            self.visuals.append(textbox.TextBox(xi, y, w/5,h, 'Hráč ' +str(order[o]+1), pygame.font.SysFont('gabriola', 46), (255, 215, 0), (128, 128, 128) ))
            xi += w/5
            for r in results[order[o]]:
                self.visuals.append(textbox.TextBox(xi, y, w/10,h, str(r), pygame.font.SysFont('gabriola', 46), (255, 215, 0), (128, 128, 128) ))
                xi += w/10
            self.visuals.append(textbox.TextBox(xi, y, w/10,h, str(sum(results[order[o]])), pygame.font.SysFont('gabriola', 46), (255, 215, 0), (128, 128, 128) ))        
            y +=h
    
    def check(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif self.back_button.is_clicked(event):
            self.running = False
        return self
    def draw(self, screen):
        screen.fill((30, 30, 30))
        self.back_button.draw(screen)
        for v in self.visuals:
            v.draw(screen)
        pygame.display.flip()
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
pygame.display.set_caption("Obludárium")

clock = pygame.time.Clock()
last_state = 'start'
state = "menu"
running = True
players = 5
while running:
    clock.tick(60)
    app = Display(SCREEN_HEIGHT, SCREEN_WIDTH, running)
    app.draw(screen)
    for event in pygame.event.get():
        app.check(event)
    state = app.state
    running = app.running
    if hasattr(app, "players"):
        players = app.players



pygame.quit()
sys.exit() 
    


    