import pygame
import sys
import classes.states.Menu as menu
import classes.states.LocalGameMenu as localgamemenu
import classes.states.GameScene as gamescene

def main():
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
        if last_state != state:
            match state:
                case "menu":
                    app = menu.Menu(SCREEN_HEIGHT, SCREEN_WIDTH)
                case "local_game_menu":
                    app = localgamemenu.LocalGameMenu(SCREEN_HEIGHT, SCREEN_WIDTH)
                case "local_game":
                    app = gamescene.GameScene(SCREEN_HEIGHT, SCREEN_WIDTH, players)
                case _:
                    running = False
            last_state = state
        app.update(screen)
        state = app.state
        running = app.running
        if hasattr(app, "players"):
            players = app.players

    pygame.quit()
    sys.exit() 


if __name__ == "__main__":
    main()