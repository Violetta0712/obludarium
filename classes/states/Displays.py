import classes.ux.Button as button
import classes.ux.CardImage as img
import pygame
class Display:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, phase):
        self.running = True
        self.state = state
        self.phase = phase
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

    
class Season(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state,phase, cardid):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, phase)
        card_width = SCREEN_WIDTH // 6
        card_x = (SCREEN_WIDTH - card_width)/2
        card_y = (SCREEN_HEIGHT - (13/9)*card_width)/2
        self.seasoncard = img.CardImage(card_x,card_y, card_width, cardid)
        ok_width = card_width
        ok_height = SCREEN_HEIGHT // 15
        ok_x = card_x
        ok_y = card_y + (13/9)*card_width + SCREEN_HEIGHT // 30
        self.okbutton = button.Button( ok_x,ok_y,ok_width,ok_height,"OK", pygame.font.SysFont(None, 36),(70, 130, 180),(100, 160, 210))

    
    def draw(self, screen):
        super().draw(screen)
        self.seasoncard.draw(screen)
        self.okbutton.draw(screen)

    def check(self, event):
        super().check(event)
        if self.okbutton.is_clicked(event):
            self.phase = 'turn'

class Turn(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, phase, person, hand):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, phase)
        self.person = person
        self.hand = hand
        