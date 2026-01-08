
import pygame
import classes.ux.Button as button
import classes.ux.TextBox as textbox
import classes.logic.Game as game
import classes.logic.Player as player
def draw_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    running = True
    state = "menu"
    b_width = SCREEN_HEIGHT // 4
    b_height = SCREEN_HEIGHT // 12
    b_interval = SCREEN_HEIGHT // 20
    b_number = 2
    b_x = (SCREEN_WIDTH - b_width) // 2
    b_y = (SCREEN_HEIGHT - (b_number * b_height + (b_number - 1) * b_interval)) // 2
    local_button = button.Button(b_x, b_y, b_width, b_height, "Lokální hra", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))  
    b_y = b_y + b_height + b_interval
    quit_button = button.Button(b_x, b_y, b_width, b_height, "Ukončit", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif quit_button.is_clicked(event):
                state = "terminate"
                running = False
            elif local_button.is_clicked(event):
                state = "local_game_menu"
                running = False

            screen.fill((30, 30, 30))
            quit_button.draw(screen)
            local_button.draw(screen)
            pygame.display.flip()
    return state

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
    t1 = textbox.TextBox(b_x, b_y, b_width, b_height, str(players), pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
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
            t1.draw(screen)
            pygame.display.flip()
    return state, players

def draw_local_game_menu(screen, SCREEN_WIDTH, SCREEN_HEIGHT):
    running = True
    state = "local_game_menu"
    back_b_width = SCREEN_WIDTH // 6
    back_b_height = SCREEN_HEIGHT // 12
    back_b_x = back_b_width // 4
    back_b_y = back_b_height // 2
    back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "Back", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    b_width = SCREEN_HEIGHT // 4
    b_height = SCREEN_HEIGHT // 12
    b_interval = SCREEN_HEIGHT // 20
    b_number = 6
    b_x = (SCREEN_WIDTH + 2 * b_interval) // 2
    b_y = (SCREEN_HEIGHT - (b_number * b_height + (b_number - 1) * b_interval)) // 2
    t_x = (SCREEN_WIDTH - 2 * b_width - b_interval) // 2
    pa = ["Hráč", "AI"]
    pan = ["Hráč", "AI", "Žádný"]
    p2id = 0
    p3id = 0   
    p4id = 0
    p5id = 0
    t1 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 1", pygame.font.SysFont(None, 36), (200, 200, 200), (0,0,0))
    p1_button = button.Button(b_x, b_y, b_width, b_height, "Hráč", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))  
    b_y = b_y + b_height + b_interval
    t2 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 2", pygame.font.SysFont(None, 36), (200, 200, 200), (0,0,0))
    p2_button = button.Button(b_x, b_y, b_width, b_height, pa[p2id], pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))  
    b_y = b_y + b_height + b_interval
    t3 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 3", pygame.font.SysFont(None, 36), (200, 200, 200), (0,0,0))
    p3_button = button.Button(b_x, b_y, b_width, b_height, pa[p3id], pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    b_y = b_y + b_height + b_interval
    t4 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 4", pygame.font.SysFont(None, 36), (200, 200, 200), (0,0,0))
    p4_button = button.Button(b_x, b_y, b_width, b_height, pan[p4id], pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    b_y = b_y + b_height + b_interval
    t5 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 5", pygame.font.SysFont(None, 36), (200, 200, 200), (0,0,0))
    p5_button = button.Button(b_x, b_y, b_width, b_height, pan[p5id], pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    b_y = b_y + b_height + b_interval
    b_x = (SCREEN_WIDTH - b_width) // 2
    startgame_button = button.Button(b_x, b_y, b_width, b_height, "Start Game", pygame.font.SysFont(None, 36), (70, 130, 180), (100, 160, 210))
    players = 5
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif back_button.is_clicked(event):
                state = "menu"
                running = False
            elif startgame_button.is_clicked(event):
                state = "local_game"
                running = False
            elif p2_button.is_clicked(event):
                p2id = (p2id + 1) % len(pa)
                p2_button.text = pa[p2id]

            elif p3_button.is_clicked(event):
                p3id = (p3id + 1) % len(pa)
                p3_button.text = pa[p3id]

            elif p4_button.is_clicked(event):
                p4id = (p4id + 1) % len(pan)
                p4_button.text = pan[p4id]

            elif p5_button.is_clicked(event):
                p5id = (p5id + 1) % len(pan)
                p5_button.text = pan[p5id]
            players = 5 - (1 if p5id == 2 else 0) - (1 if p4id == 2 else 0)


            screen.fill((30, 30, 30))
            back_button.draw(screen)
            p1_button.draw(screen)
            p2_button.draw(screen)  
            p3_button.draw(screen)
            p4_button.draw(screen)
            p5_button.draw(screen)
            t1.draw(screen)
            t2.draw(screen) 
            t3.draw(screen)
            t4.draw(screen)
            t5.draw(screen)
            startgame_button.draw(screen)
            pygame.display.flip()
    return state, players