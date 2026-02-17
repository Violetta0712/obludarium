import classes.ux.Button as button
import classes.ux.TextBox as textbox
import pygame
class LocalGameMenu:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH ):
        self.running = True
        self.state = "local_game_menu"
        self.buttons = []
        self.textboxes = []
        back_b_width = SCREEN_WIDTH // 6
        back_b_height = SCREEN_HEIGHT // 12
        back_b_x = back_b_width // 4
        back_b_y = back_b_height // 2
        self.back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "Zpět",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.back_button)
        b_width = SCREEN_HEIGHT // 4
        b_height = SCREEN_HEIGHT // 12
        b_interval = SCREEN_HEIGHT // 20
        b_number = 6
        b_x = (SCREEN_WIDTH + 2 * b_interval) // 2
        b_y = (SCREEN_HEIGHT - (b_number * b_height + (b_number - 1) * b_interval)) // 2
        t_x = (SCREEN_WIDTH - 2 * b_width - b_interval) // 2
        self.pa = ["Hráč", "AI velmi snadné", "AI snadné", "AI střední"]
        self.pan = ["Hráč", "AI velmi snadné", "AI snadné", "AI střední", "Žádný"]
        self.p2id = 0
        self.p3id = 0   
        self.p4id = 0
        self.p5id = 0
        t1 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 1",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0,0,0))
        self.textboxes.append(t1)
        self.p1_button = button.Button(b_x, b_y, b_width, b_height, "Hráč", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))  
        self.buttons.append(self.p1_button)
        b_y = b_y + b_height + b_interval
        t2 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 2",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0,0,0))
        self.textboxes.append(t2)
        self.p2_button = button.Button(b_x, b_y, b_width, b_height, self.pa[self.p2id],  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))  
        self.buttons.append(self.p2_button)
        b_y = b_y + b_height + b_interval
        t3 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 3",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0,0,0))
        self.textboxes.append(t3)
        self.p3_button = button.Button(b_x, b_y, b_width, b_height, self.pa[self.p3id],  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.p3_button)
        b_y = b_y + b_height + b_interval
        t4 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 4",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0,0,0))
        self.textboxes.append(t4)
        self.p4_button = button.Button(b_x, b_y, b_width, b_height, self.pan[self.p4id],  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.p4_button)
        b_y = b_y + b_height + b_interval
        t5 = textbox.TextBox(t_x, b_y, b_width, b_height, "Hráč 5",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0,0,0))
        self.textboxes.append(t5)
        self.p5_button = button.Button(b_x, b_y, b_width, b_height, self.pan[self.p5id],  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.p5_button)
        b_y = b_y + b_height + b_interval
        b_x = (SCREEN_WIDTH - b_width) // 2
        self.startgame_button = button.Button(b_x, b_y, b_width, b_height, "Spustit hru",  pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        self.buttons.append(self.startgame_button)
        self.players = ["Hráč", self.pa[self.p2id],self.pa[self.p3id], self.pan[self.p4id], self.pan[self.p5id]]
    def update(self, screen):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.back_button.is_clicked(event):
                self.state = "menu"
            elif self.startgame_button.is_clicked(event):
                self.state = "local_game"
            elif self.p2_button.is_clicked(event):
                self.p2id = (self.p2id + 1) % len(self.pa)
                self.p2_button.text = self.pa[self.p2id]

            elif self.p3_button.is_clicked(event):
                self.p3id = (self.p3id + 1) % len(self.pa)
                self.p3_button.text = self.pa[self.p3id]

            elif self.p4_button.is_clicked(event):
                self.p4id = (self.p4id + 1) % len(self.pan)
                self.p4_button.text = self.pan[self.p4id]

            elif self.p5_button.is_clicked(event):
                self.p5id = (self.p5id + 1) % len(self.pan)
                self.p5_button.text = self.pan[self.p5id]
            self.players = ["Hráč", self.pa[self.p2id],self.pa[self.p3id], self.pan[self.p4id], self.pan[self.p5id]]


        screen.fill((168, 150, 150))
        for b in self.buttons:
            b.draw(screen)
        for t in self.textboxes:
            t.draw(screen)
        pygame.display.flip()


