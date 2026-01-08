import functions.functions as f
import pandas as pd
import json
import random 
import params as p
import functions.ux as u
import pygame
import sys
import classes.ux.Button as button
import classes.ux.TextBox as textbox

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    pygame.display.set_caption("Obludárium")

    clock = pygame.time.Clock()
    state = "menu"
    running = True
    while running:
        clock.tick(60)
        if state == "menu":
            state = u.draw_menu(screen,SCREEN_WIDTH, SCREEN_HEIGHT)
        elif state == "local_game_menu":
            state, players = u.draw_local_game_menu(screen,SCREEN_WIDTH, SCREEN_HEIGHT)
        elif state == "local_game":
            state, players = u.draw_game(screen,SCREEN_WIDTH, SCREEN_HEIGHT, players)
        else:
            print("EXITING because state =", state)
            running = False

    pygame.quit()
    sys.exit() 


if __name__ == "__main__":
    main()