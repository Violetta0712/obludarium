import classes.ux.Button as button
import classes.ux.CardImage as img
import classes.ux.TextBall as textball
import classes.ux.TextBox as textbox
import classes.logic.Deck as deck
import pygame
import random
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
        self.okbutton = button.Button( ok_x,ok_y,ok_width,ok_height,"OK", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))

    
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
        coin = textbox.TextBox(self.s_width- self.offset, 0, self.offset, self.offset, str(person.money), pygame.font.SysFont('gabriola', 40), (232, 213, 0), (0, 0, 0))
        self.balls.append(coin)
        loan = textbox.TextBox(self.s_width- 2*self.offset, 0, self.offset, self.offset, str(person.loans), pygame.font.SysFont('gabriola', 40), (222, 0, 0), (0,0,0))
        self.balls.append(loan)
        hunter = textbox.TextBox(self.s_width- 3*self.offset, 0, self.offset, self.offset, str(person.cages), pygame.font.SysFont('gabriola', 40), (161, 151, 151), (0,0,0))
        self.balls.append(hunter)
        seas = textbox.TextBox((self.s_width- 10*self.offset)/2, 0, self.offset*10, self.offset, str(local_game.s_ref[local_game.season]['jmeno']), pygame.font.SysFont('gabriola', 36), (204, 190, 57), (0,0,0))
        self.balls.append(seas)
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
            ball = textball.TextBall(x, y, r, a + '/' + b, pygame.font.SysFont(None, 48), col, (0, 0, 0))
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
        self.b1 = button.Button(0, by, bw, bw, "<", pygame.font.SysFont('gabriola', 48), (204, 190, 57), (247, 235, 131) )
        self.b2 = button.Button(SCREEN_WIDTH-bw, by, bw, bw, ">", pygame.font.SysFont('gabriola', 48), (204, 190, 57), (247, 235, 131) )
        if self.page > 1:
            self.buttons.append(self.b1)
        else:
            self.b1 = None
        if self.page * 6 < len(hand.cards):
            self.buttons.append(self.b2)
        else:
            self.b2 = None
        it = 6*self.page
        for i in range(it-6, min(it, len(hand.cards))):
            karta = img.CardImage(cx, cy, cw, hand.cards[i].id)
            self.karty.append(karta)
            if hand.isplayable and hand.cards[i].isplayable(self.person):
                t = button.Button(cx, cy +ch, cw/2, cw/4, "Hrát", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131) )
                self.playbuttons.append(t)
                self.playid.append(i)
            if hand.isstorable:
                t = button.Button(cx+cw/2, cy +ch, cw/2, cw/4, "Uložit", pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131) )
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
                if karta.card_type == "monster" and karta.cards>0:
                    deck.sample_cards(self.local_game, self.person, karta.cards)
                if result=='párek':
                    return PurpleDisplay(self.s_height, self.s_width,self.state,self.local_game, karta, [0, 0, 0, 0, 0, 0])
                if result == 'kolděda':
                    return KoldedaDisplay(self.s_height, self.s_width,self.state,self.local_game, karta)
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
        self.person = person
        self.now_playing = self.local_game.players[self.local_game.current_player]
        self.b_deck = button.Button(0, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Balíček", pygame.font.SysFont('gabriola', 30), (204, 190, 57), (247, 235, 131) )
        self.bs.append(self.b_deck)
        self.b_stored = button.Button(self.offset*4, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Uložené", pygame.font.SysFont('gabriola', 30), (204, 190, 57), (247, 235, 131) )
        self.bs.append(self.b_stored)
        self.b_monsters = button.Button(self.offset*8, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Obludy", pygame.font.SysFont('gabriola', 30), (204, 190, 57), (247, 235, 131) )
        self.bs.append(self.b_monsters)
        self.b_upgrades = button.Button(self.offset*12, (SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Lidi", pygame.font.SysFont('gabriola', 30), (204, 190, 57), (247, 235, 131) )
        self.bs.append(self.b_upgrades)
        player_id = textbox.TextBox((SCREEN_WIDTH-self.offset*4)/2,(SCREEN_HEIGHT-self.offset)/2, self.offset*4, self.offset, "Hráč " + str(person.id + 1), pygame.font.SysFont('gabriola', 30), (204, 190, 57), (0, 0, 0) )
        self.bs.append(player_id)
        self.others = []
        self.other_ids = []
        xx = (SCREEN_WIDTH)/2 +2*self.offset
        for i in range(len(self.local_game.players)):
            if i != self.local_game.current_player:
                self.other_ids.append(i)
                self.others.append(button.Button(xx, (SCREEN_HEIGHT-self.offset)/2, self.offset*3, self.offset, 'Hráč'+str(i+1), pygame.font.SysFont('gabriola', 30), (204, 190, 57), (247, 235, 131) ))
                xx += self.offset*3



        
    def draw(self, screen):
        super().draw(screen)
        for b in self.bs:
            b.draw(screen)
        for b in self.others:
            b.draw(screen)
    def check(self, event):
        if self.now_playing.had_played:
            self.b_next = button.Button(self.s_width-self.offset*4, (self.s_height-self.offset)/2, self.offset*4, self.offset, "Konec", pygame.font.SysFont('gabriola', 30), (168, 61, 61), (194, 116, 116) )
            self.bs.append(self.b_next)
        else:
            self.b_next = None
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
            self.now_playing.had_played = False
            self.local_game.hands[self.local_game.current_deck].isplayable = True
            self.local_game.hands[self.local_game.current_deck].isstorable = True
            match self.local_game.next_player():
                case "turn":
                    return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[self.local_game.current_deck])
                case "season":
                    return EndSeason(self.s_height, self.s_width,self.state, self.local_game)
                case "end":
                    self.state = "menu"
        for b in range(len(self.others)):
            if self.others[b].is_clicked(event):
                return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.other_ids[b]], self.local_game.players[self.other_ids[b]].upgrades)
        return self

class PurpleDisplay(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, karta, selected=None):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
        if selected is None:
            selected = [0, 0, 0, 0, 0, 0]
        self.selected_bioms = list(selected)
        self.karta = karta
        self.person = self.local_game.players[self.local_game.current_player]
        card_width = SCREEN_WIDTH // 6
        card_x = (SCREEN_WIDTH - card_width)/4
        card_y = (SCREEN_HEIGHT - (13/9)*card_width)/2
        self.purplecard = img.CardImage(card_x,card_y, card_width, karta.id)
        self.goal = karta.level
        self.achieved = sum(self.selected_bioms)
        self.ballbuttons = []
        self.balls = []
        self.maxs = []
        r = (SCREEN_WIDTH-2*self.offset)/36
        x = SCREEN_WIDTH/2 + r/2
        y = (SCREEN_HEIGHT - len(self.person.bioms) * 2 * r) / 2
        t = textbox.TextBox(3*SCREEN_WIDTH/4,SCREEN_HEIGHT/2, self.offset*3, self.offset*2, str(self.achieved)+'/'+str(self.goal),pygame.font.SysFont('gabriola', 40), (204, 190, 57), (0, 0, 0))
        if self.goal == self.achieved:
            self.confirm_b = button.Button(3*SCREEN_WIDTH/4+self.offset*4, SCREEN_HEIGHT/2, self.offset*3, self.offset*2, 'OK',pygame.font.SysFont('gabriola', 40), (204, 190, 57), (247, 235, 131))
        else:
            self.confirm_b = None
        self.balls.append(t)
        for id, (barva, biom) in enumerate(self.person.bioms.items()):
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
            self.maxs.append(biom[0])
            ball = textball.TextBall(x, y, r, str(self.selected_bioms[id])+'/'+str(biom[0]), pygame.font.SysFont('gabriola', 48), col, (0, 0, 0))
            self.balls.append(ball)
            b1 = button.Button(x-r-self.offset, y-self.offset/2, self.offset, self.offset, '<', pygame.font.SysFont('gabriola', 48), (204, 190, 57), (247, 235, 131))
            b2 = button.Button(x+r, y-self.offset/2, self.offset, self.offset, '>', pygame.font.SysFont('gabriola', 48), (204, 190, 57), (247, 235, 131))
            self.ballbuttons.append(b1)
            self.ballbuttons.append(b2)

            y+= 2*r



    def draw(self, screen):
        super().draw(screen)
        self.purplecard.draw(screen)
        for b in self.balls:
            b.draw(screen)
        for b in self.ballbuttons:
            b.draw(screen)
        if self.confirm_b:
            self.confirm_b.draw(screen)

    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        for i in range(len(self.ballbuttons)):
            if self.ballbuttons[i].is_clicked(event):
                if i%2==0:
                    index = int(i/2)
                    if self.selected_bioms[index]>0:
                        self.selected_bioms[index] -= 1
                        return PurpleDisplay(self.s_height, self.s_width,self.state,self.local_game, self.karta, self.selected_bioms)
                else:
                    index = int((i-1)/2)
                    if self.selected_bioms[index]<self.maxs[index]:
                        self.selected_bioms[index] += 1
                        return PurpleDisplay(self.s_height, self.s_width,self.state,self.local_game, self.karta, self.selected_bioms)
        if self.confirm_b and self.confirm_b.is_clicked(event):
            self.karta.actually_play(self.person, self.selected_bioms)
            return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[self.local_game.current_deck])
        return self
    
class KoldedaDisplay(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game, karta):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
        self.karta = karta
        self.person = self.local_game.players[self.local_game.current_player]
        card_width = SCREEN_WIDTH // 6
        card_x = (SCREEN_WIDTH - card_width)/4
        card_y = (SCREEN_HEIGHT - (13/9)*card_width)/2
        self.purplecard = img.CardImage(card_x,card_y, card_width, karta.id)
        self.balls = []
        r = (SCREEN_WIDTH-2*self.offset)/18
        x = SCREEN_WIDTH/2 + r/2
        y = (SCREEN_HEIGHT - len(self.person.bioms) * r) / 2
        self.colors = []
        for id, (barva, biom) in enumerate(self.person.bioms.items()):
            match barva:
                case "modra":
                    col = (58, 170, 255)
                    col2 = (128, 155, 255)
                case "cerna":
                    col = (102, 110,117)
                    col2 = (184, 184, 184)
                case "hneda":
                    col = (153, 76, 0)
                    col2 = (153, 107, 72)
                case "zelena":
                    col = (76, 153, 0)
                    col2 = (106, 199, 99)
                case "zlata":
                    col = (255, 255, 51)
                    col2 = (255, 238, 150)
                case "fialova":
                    col = (153, 0, 153)
                    col2 = (167, 118, 222)
            self.colors.append(barva)
            ball = button.Button(x, y, r,r, '', pygame.font.SysFont('gabriola', 48), col, col2)
            self.balls.append(ball)
            y+= r

    def draw(self, screen):
        super().draw(screen)
        self.purplecard.draw(screen)
        for b in self.balls:
            b.draw(screen)

    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        for i in range(len(self.balls)):
            if self.balls[i].is_clicked(event):
                self.karta.actually_play(self.person, self.colors[i])
                return TurnDeck(self.s_height, self.s_width,self.state, self.local_game, self.local_game.players[self.local_game.current_player], self.local_game.hands[self.local_game.current_deck])
        return self
        

class EndSeason(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)

        dice = random.sample([0,0,0,0,1,2], 1)[0] + random.sample([0,0,0,0,1,2], 1)[0]

        self.boxes = []
        font = pygame.font.SysFont('gabriola', 36)
        goals =[]
        x = (SCREEN_WIDTH-self.offset*42)/2
        y = self.offset * 3
        h = self.offset*2
        w = self.offset *6
        self.boxes.append(textbox.TextBox(
                    x,y,w,h,
                    "Hráč",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ))
        self.boxes.append(textbox.TextBox(
                    x+w,y,w,h,
                    "Běsnění",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
        self.boxes.append(textbox.TextBox(
                    x+2*w,y,w,h,
                    "Prominuté",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
        self.boxes.append(textbox.TextBox(
                    x+3*w,y,w,h,
                    "Klece",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
        self.boxes.append(textbox.TextBox(
                    x+4*w,y,w,h,
                    "Peníze",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
        self.boxes.append(textbox.TextBox(
                    x+5*w,y,w,h,
                    "Půjčky",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
        self.boxes.append(textbox.TextBox(
                    x+6*w,y,w,h,
                    "Cíl",
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )

        y += h
        for play in range(len(local_game.players)):
            vals = local_game.players[play].end_season(dice,  local_game.s_ref[local_game.season]['akce'])
            goals.append(vals[5])
            self.boxes.append(textbox.TextBox(
                    x,y,w,h,
                    "Hráč "+str(play+1),
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ) )
            self.boxes.append(textbox.TextBox(
                    x+w,y,w,h,
                    str(vals[0]),
                    font,
                    (204, 190, 57),
                    (0, 0, 0)
                ))
            self.boxes.append(textbox.TextBox(
                        x+2*w,y,w,h,
                        str(vals[1]),
                        font,
                        (204, 190, 57),
                        (0, 0, 0)
                    ) )
            self.boxes.append(textbox.TextBox(
                        x+3*w,y,w,h,
                        str(vals[2]),
                        font,
                        (204, 190, 57),
                        (0, 0, 0)
                    ) )
            self.boxes.append(textbox.TextBox(
                        x+4*w,y,w,h,
                        str(vals[3]),
                        font,
                        (204, 190, 57),
                        (0, 0, 0)
                    ) )
            self.boxes.append(textbox.TextBox(
                        x+5*w,y,w,h,
                        str(vals[4]),
                        font,
                        (204, 190, 57),
                        (0, 0, 0)
                    ) )
            self.boxes.append(textbox.TextBox(
                        x+6*w,y,w,h,
                        str(vals[5]),
                        font,
                        (204, 190, 57),
                        (0, 0, 0)
                    ) )
            y+=h
        if goals.count(max(goals))==1:
            index = goals.index(max(goals))
            local_game.players[index].seasons_won +=1
            message = f"Hráč {index +1} vyhrál sezónu"
        else:
            message = "Sezónu nezískal nikdo"

        self.ok_button = button.Button(
            (SCREEN_WIDTH - self.offset * 4)/2,
            SCREEN_HEIGHT - self.offset * 2,
            self.offset * 4,
            self.offset,
            "OK",
            pygame.font.SysFont('gabriola', 36),
            (204, 190, 57), (247, 235, 131)
        )
        self.boxes.append(
                textbox.TextBox(
                    0,
                    self.offset,
                    SCREEN_WIDTH/2,
                    self.offset*2,
                    f"Kostky: {dice}",
                    font,
                    (204, 190, 57),
                    (0,0,0)
                )
            )
        self.boxes.append(
            textbox.TextBox(
                    SCREEN_WIDTH/2,
                    self.offset,
                    SCREEN_WIDTH/2,
                    self.offset*2,
                    message,
                    font,
                    (204, 190, 57),
                    (0,0,0)
                )
        )

    def draw(self, screen):
        super().draw(screen)
        for b in self.boxes:
            b.draw(screen)
        self.ok_button.draw(screen)

    def check(self, event):
        result = super().check(event)
        if result is not self:
            return result
        if self.ok_button.is_clicked(event):
            match self.local_game.end_round():
                case 'season':
                    return Season(self.s_height, self.s_width,self.state, self.local_game, self.local_game.season)
                case 'end':
                    self.local_game.end_game()
                    return End(self.s_height, self.s_width,self.state, self.local_game)
        return self
    

class End(Display):
    def __init__(self, SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game):
        super().__init__(SCREEN_HEIGHT, SCREEN_WIDTH, state, local_game)
        order = self.local_game.order
        results = self.local_game.results
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
    def draw(self, screen):
        super().draw(screen)
        for v in self.visuals:
            v.draw(screen)
    