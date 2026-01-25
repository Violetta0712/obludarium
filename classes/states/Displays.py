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
        result = super().check(event)
        if result is not self:
            return result
        if self.okbutton.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[self.local_game.current_deck])
        return self

class Turn(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page = 1):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
        self.person = person
        self.balls = []
        r = (SCREEN_WIDTH-2*self.offset)/36
        x = self.offset+r
        y = self.offset+r
        ww = (SCREEN_WIDTH-2*self.offset)/6
        hh = self.offset
        coin = textbox.TextBox(self.s_width- 3*self.offset, 0, 3*self.offset, self.offset, str(person.money), pygame.font.SysFont(None, 48), (255, 204, 153), (255, 255, 255))
        self.balls.append(coin)
        loan = textbox.TextBox(self.s_width- 6*self.offset, 0, 3*self.offset, self.offset, str(person.loans), pygame.font.SysFont(None, 48), (255, 204, 153), (255, 255, 255))
        self.balls.append(loan)
        hunter = textbox.TextBox(self.s_width- 9*self.offset, 0, 3*self.offset, self.offset, str(person.cages), pygame.font.SysFont(None, 48), (255, 204, 153), (255, 255, 255))
        self.balls.append(hunter)
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
            y_card = y+ r
            for oc in person.occupied[barva]:
                self.balls.extend(oc.create_visual(x-r, y_card, ww, hh))
                y_card+=hh
            x += (SCREEN_WIDTH-2*self.offset)/6
        self.hand = hand
        self.karty = []
        self.buttons = []
        self.playbuttons = []
        self.playid = []
        self.storebuttons = []
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
            if hand.isplayable and hand.cards[i].isplayable(self.person):
                t = button.Button(cx, cy +ch, cw/2, cw/4, "Hrát", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
                self.playbuttons.append(t)
                self.playid.append(i)
            if hand.isstorable:
                t = button.Button(cx+cw/2, cy +ch, cw/2, cw/4, "Uložit", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
                self.storebuttons.append(t)
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
        for b in self.storebuttons:
            b.draw(screen)
    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        if self.b1 and self.b1.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.hand, self.page-1)

        if self.b2 and self.b2.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.hand, self.page+1)
        for i in range(len(self.playbuttons)):
            if self.playbuttons[i].is_clicked(event):
                karta = self.hand.cards[self.playid[i]]
                result = self.hand.play_card(self.playid[i], self.person)
                if result=='párek':
                    return PurpleDisplay(self.s_height, self.s_width,self.state,self.local_game, karta)
                return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.hand, 1)
        for i in range(len(self.storebuttons)):
            if self.storebuttons[i].is_clicked(event):
                self.hand.store_card(i, self.person)
                return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.hand, 1)
        return self 



class TurnDeck(Turn):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page = 1):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, person, hand, page)
        self.bs = []
        self.now_playing = self.local_game.players[self.local_game.current_player]
        self.b_deck = button.Button(0, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Balíček", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
        self.bs.append(self.b_deck)
        self.b_stored = button.Button(self.offset*4, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Uložené", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
        self.bs.append(self.b_stored)
        self.b_monsters = button.Button(self.offset*8, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Obludy", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
        self.bs.append(self.b_monsters)
        self.b_upgrades = button.Button(self.offset*12, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Lidi", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
        self.bs.append(self.b_upgrades)
        if person.had_played:
            self.b_next = button.Button(SCREEN_WIDTH-self.offset*4, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Konec", pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
            self.bs.append(self.b_next)
        else:
            self.b_next = None
        player_id = textbox.TextBox((SCREEN_WIDTH-self.offset*4)/2,(SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Hráč" + str(person.id + 1), pygame.font.SysFont(None, 48), (76, 153, 0), (102, 180, 0) )
        self.bs.append(player_id)
    def draw(self, screen):
        super().draw(screen)
        for b in self.bs:
            b.draw(screen)
    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        if self.b_deck.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.now_playing, self.local_game.hands[self.local_game.current_deck])
        if self.b_stored.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.now_playing, self.now_playing.stored)
        if self.b_monsters.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.now_playing, self.now_playing.monsters)
        if self.b_upgrades.is_clicked(event):
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.now_playing, self.now_playing.upgrades)
        if self.b_next and self.b_next.is_clicked(event):
            self.person.had_played = False
            self.hand.isplayable = True
            self.hand.isstorable = True
            match self.local_game.next_player():
                case "turn":
                    return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[self.local_game.current_deck])
                case "season":
                    return Season(self.s_height, self.s_width,self.state, self.local_game, self.local_game.season)
                case "end":
                    self.state = "menu"
        return self

class PurpleDisplay(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, karta):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
        self.person = self.local_game.players[self.local_game.current_player]
        card_width = SCREEN_WIDTH // 6
        card_x = (SCREEN_WIDTH - card_width)/4
        card_y = (SCREEN_HEIGHT - (13/9)*card_width)/2
        self.purplecard = img.CardImage(card_x,card_y, card_width, karta.id)
        

    def draw(self, screen):
        super().draw(screen)
        self.purplecard.draw(screen)

    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        return self