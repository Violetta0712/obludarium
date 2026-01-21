import classes.ux.Button as button
import classes.ux.CardImage as img
import classes.ux.TextBall as textball
import classes.ux.TextBox as textbox
import pygame
class Display:
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game):
        self.running = True
        self.state = state
        self.s_height = SCREEN_HEIGHT
        self.s_width = SCREEN_WIDTH
        self.local_game = local_game
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
        return self
    def draw(self, screen):
        self.back_button.draw(screen)

    
class Season(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state,local_game, cardid):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
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
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[0])
        return self

class Turn(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page = 1):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
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
            self.hand = hand
        self.karty = []
        self.buttons = []
        self.playbuttons = []
        self.playid = []
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
        self.b1 = button.Button(0, by, bw, bw, "<", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
        self.b2 = button.Button(SCREEN_WIDTH-bw, by, bw, bw, ">", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
        if self.page > 1:
            self.b1 = button.Button(0, by, bw, bw, "<", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
            self.buttons.append(self.b1)
        else:
            self.b1 = None
        if self.page * 6 < len(hand.cards):
            self.b2 = button.Button(SCREEN_WIDTH-bw, by, bw, bw, ">", pygame.font.SysFont(None, 48), (255, 204, 153),(255, 204, 153) )
            self.buttons.append(self.b2)
        else:
            self.b2 = None
        it = 6*self.page
        for i in range(it-6, min(it, len(hand.cards))):
            karta = img.CardImage(cx, cy, cw, hand.cards[i].id)
            self.karty.append(karta)
            if hand.isplayable and getattr(hand.cards[i], "isplayable", False):
                t = button.Button(cx, cy +ch, cw/2, cw/4, "Hrát", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
                self.playbuttons.append(t)
                self.playid.append(i)
            cx += ((cw+self.offset))
    
    def draw(self, screen):
        super().draw(screen)
        for ball in self.balls:
            ball.draw(screen)
        self.bg.draw(screen)
        for k in self.karty:
            k.draw(screen)
        for b in self.buttons:
            b.draw(screen)
        for b in self.playbuttons:
            b.draw(screen)
    def check(self, event):
        super().check(event)
        if self.b1 and self.b1.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[0], self.page-1)

        if self.b2 and self.b2.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[0], self.page+1)
        for i in range(len(self.playbuttons)):
            if self.playbuttons[i].is_clicked(event):
                self.hand.play_card(self.playid[i], self.person)
                return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[0], 1)
        return self 



class TurnDeck(Turn):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page = 1):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page)
        