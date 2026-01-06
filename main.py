import functions.functions as f
import pandas as pd
import json
import random 
import params as p
import functions.ux as u
import pygame
import sys
import classes.ux.Button as button

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
    pygame.display.set_caption("Obludárium")

    clock = pygame.time.Clock()
    state = "menu"
    running = True

    quit_button = button.Button(100, 100, 200, 50, "Quit Game", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if quit_button.is_clicked():
                running = False

        screen.fill((30, 30, 30))
        quit_button.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit() 


if __name__ == "__main__":
    main()