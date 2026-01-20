import classes.ux.Button as button
import classes.ux.CardImage as img
import classes.ux.TextBall as textball
import classes.ux.TextBox as textbox
import pygame
class Display:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, phase):
        self.running = True
        self.state = state
        self.phase = phase
        self.offset = SCREEN_HEIGHT //24
        back_b_width = self.offset
        back_b_height = self.offset
        back_b_x = 0
        back_b_y = 0
        self.back_button = button.Button(back_b_x, back_b_y, back_b_width, back_b_height, "x", pygame.font.SysFont(None, 36), (180, 60, 60), (220, 90, 90))
    
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
            self.phase = 'turn-deck'

class Turn(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, phase, person):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, phase)
        self.person = person
        self.balls = []
        r = (SCREEN_WIDTH-2*self.offset)/36
        x = self.offset+r
        y = self.offset+r
        for barva,biom in person.bioms.items():
            match barva:
                case "modra":
                    col = (58, 170, 255)
                case "cerna":
                    col = (102, 110,117)
                case "hneda":
                    col = (153, 76, 0)
                case "zelena":
                    col = (76, 153, 0)
                case "zlata":
                    col = (255, 255, 51)
                case "fialova":
                    col = (153, 0, 153)
            a = str(biom[0])
            b = str(sum(biom))
            ball = textball.TextBall(x, y, r, a + '/' + b, pygame.font.SysFont(None, 48), col, (255, 255, 255))
            self.balls.append(ball)
            x += (SCREEN_WIDTH-2*self.offset)/6
    
    def draw(self, screen):
        super().draw(screen)
        for ball in self.balls:
            ball.draw(screen)


class TurnDeck(Turn):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, phase, person, hand, page = 1):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, phase, person)
        self.hand = hand
        self.karty = []
        self.buttons = []
        self.page = page
        w = SCREEN_WIDTH
        h = (SCREEN_HEIGHT -self.offset)/2
        x = 0
        y = (SCREEN_HEIGHT +self.offset)/2
        self.bg = textbox.TextBox(x, y, w, h, "", pygame.font.SysFont(None, 48), (255, 204, 153) )
        cw = (SCREEN_WIDTH-7*self.offset)/6
        ch = 13*cw/9
        cx = x+self.offset
        cy = y+ self.offset
        bw = self.offset
        by = (SCREEN_HEIGHT/2)+(h/2)
        if self.page > 1:
            self.b1 = button.Button(0, by, bw, bw, "<", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
            self.buttons.append(self.b1)
        if self.page * 6 < len(hand.cards):
            self.b2 = button.Button(SCREEN_WIDTH-bw, by, bw, bw, ">", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
            self.buttons.append(self.b2)
        for i in range(6):
            karta = img.CardImage(cx, cy, cw, hand.cards[i].id)
            self.karty.append(karta)
            cx += ((cw+self.offset))

    def draw(self, screen):
        super().draw(screen)
        self.bg.draw(screen)
        for k in self.karty:
            k.draw(screen)
        for b in self.buttons:
            b.draw(screen)
