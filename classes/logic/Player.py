import classes.logic.Deck as deck
import math
import random
class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = deck.Deck()
        self.bioms = {"modra":[0,0], "cerna":[0,0], "hneda":[0,0], "zelena":[0,0], "zlata":[0,0], "fialova":[0,0]}
        self.occupied = {"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
        self.upgrades = deck.Deck()
        self.for_scoring = deck.Deck()
        self.buffs = []
        self.evaluation = []
        self.seasons_won = 0
        self.season_buff = None
        self.stored = deck.StoredDeck()
        self.monsters = deck.Deck()
        self.money = 4
        self.loans = 0
        self.cages = 0
        self.had_played = False
    def pay(self, price):
        if self.money >= price:
            self.money -= price
        else:
            debt = self.money - price
            loan_num = math.ceil(-1*debt/3)
            self.loans += loan_num
            self.money = (debt + loan_num*3)
    def pay_biom(self, level, color):
        self.bioms[color][0]-=level
        self.bioms[color][1]+=level
    def end_season(self, grant, season):
        grant += self.buffs.count('safe')
        fury = 0
        s_goal = 0
        if season== "agro":
            for card in self.played.cards:
                fury += card.fury
                s_goal += card.fury
        else:
            for card in self.played.cards:
                fury += card.fury
                s_goal += (1 if season == card.color else 0)*card.points
        initial_fury = fury
        fury -= grant
        cages_used = 0
        money_used = 0
        loans_taken = 0
        while fury > 0 and self.cages >0:
            self.cages -= 1
            fury -= 1
            cages_used += 1
        while fury >0 and self.money >2:
            self.money -= 3
            fury -= 1
            money_used += 3
        if fury >0:
            self.loans += fury
            loans_taken = fury
            fury = 0
        return [initial_fury, grant, cages_used, money_used, loans_taken, s_goal]
    
    def score(self):
        monster_points = 0
        objective_points = 0
        money_points = self.money
        cage_points = self.cages
        season_points = self.seasons_won *3
        loan_penalty = self.loans* -5
        for monster in self.monsters.cards:
            monster_points += monster.points
        for ob in self.stored.cards: 
            if ob.card_type == "objective":
                objective_points += ob.score(self)
        return [monster_points, objective_points, money_points, cage_points, season_points, loan_penalty]
        

        

class AIstupid(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        i = random.sample(range(len(deck.cards)),1)[0]
        return [i, 'play', None]
    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            return True, random.sample(playables,1)[0]
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected == maxs
        goal = card.level
        selectable = []
        while sum(selected)<goal:
            selectable = [idx for idx, val in enumerate(maxs) if val > 0]
            col = random.sample(selectable, 1)[0]
            if sum(selected)+maxs[col]> goal:
                selected[col] += goal - sum(selected)
            else:
                selected[col] += maxs[col]
                maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        colors = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            colors.append(barva)
        col = random.sample(colors, 1)[0]
        card.actually_play(self, col)

        

    
class AIgamble(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        playables = []
        for xi in range(len(deck.cards)):
            if deck.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            playables = range(len(deck.cards))
        i = random.sample(playables,1)[0]
        return [i, 'play', None]
    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            return True, random.sample(playables,1)[0]
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected = maxs
        else:
            goal = card.level
            selectable = []
            if maxs[5]>=goal:
                selected[5] = goal
            else:
                selected[5] = maxs[5]
                maxs[5] = 0
            while sum(selected)<goal:
                selectable = [idx for idx, val in enumerate(maxs) if val > 0]
                col = random.sample(selectable, 1)[0]
                if sum(selected)+maxs[col]> goal:
                    selected[col] += goal - sum(selected)
                else:
                    selected[col] += maxs[col]
                    maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        colors = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            colors.append(barva)
        col = random.sample(colors, 1)[0]
        card.actually_play(self, col)

    
class AIminmax(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        maxpoints = -100
        maxid = None
        barva = None
        zp = 0
        p = 0
        action = 'play'
        if 'zadne_pujcky' in self.evaluation and self.loans == 0:
            zp = 6
        if 'pujcky' in self.evaluation:
            p = 2
        for i in range(len(deck.cards)):
            card = deck.cards[i]
            if not card.isplayable(self) and card.card_type == "objective":
                points = card.score(self) - (1 if self.money > 0 else (3 + p - zp))
                if 'ukoly' in self.evaluation:
                    points += 2
            elif not card.isplayable(self):
                points = -(1 if self.money > 0 else (3 + p - zp))
            else:
                points, barva = self.evaluate_card(card, game)
            if points > maxpoints:
                maxpoints = points
                maxid = i
            if maxpoints < 0:
                action = 'store'
                maxid = random.sample(range(len(deck.cards)),1)[0]
        return [maxid, action, barva]
    
    def evaluate_card(self, card, game):
        points = 0
        barva = None
        zp = 0
        p = 0
        if 'zadne_pujcky' in self.evaluation and self.loans == 0:
            zp = 6
        if 'pujcky' in self.evaluation:
            p = 2
        match card.card_type:
                    case "monster":
                        points = card.points
                        points += game.will_win_seas(self, card)
                        if card.color == self.season_buff:
                            points += 2
                        if card.color in self.buffs:
                            points += 2
                        if "agro" in self.buffs:
                            points += card.fury
                        if self.season_buff == "agro" and card.fury > 0:
                            points += 2
                        elif self.season_buff == card.color:
                            points += 2
                        if card.color in self.evaluation:
                            points += 2
                        if card.fury > 0 and "besneni" in self.evaluation:
                            points += card.fury
                        if card.level == 1 and "mala" in self.evaluation:
                            points += 1
                        if card.level == 3 and "velka" in self.evaluation:
                            points += 2
                        elif card.level >4 and "velka" in self.evaluation:
                            points += 3
                    case "biom":
                        points = 0
                        if 'velky_biom' in self.evaluation and sum(self.bioms[card.color]) < 7 and sum(self.bioms[card.color]) + card.level >= 7:
                            points += 7
                        if  'mnoho_biomů' in self.evaluation and sum(self.bioms[card.color]) == 1:
                            points += 2
                        if 'fialovy_biom' in self.evaluation and card.color == 'fialova':
                            points += 2
                        if 'vzdaleny_biom' in self.evaluation and card.pre > 0:
                            points += 2
                        if 'malo_biomů' in self.evaluation:
                            biom_num = 0
                            for biom in self.bioms:
                                if sum(self.bioms[biom]) >0:
                                    biom_num += 1
                            if biom_num <= 3 and sum(self.bioms[card.color]) ==0:
                                points -= 7
                            elif biom_num == 4 and sum(self.bioms[card.color]) ==0:
                                points -= 4
                    case "employee":
                        points = (-card.price if self.money >= card.price else (-card.price - 2 + p - zp))
                        if 'zamestnanci' in self.evaluation:
                            points += 3
                        if card.action == "add_biom" and 'velky_biom' in self.evaluation and max([sum(b) for b in self.bioms.values()]) == 6:
                            points += 7
                            barva = next((k for k, v in self.bioms.items() if sum(v) == 6), None)
                        elif card.action == "add_biom" and 'mnoho_biomů' in self.evaluation and 1 in [sum(b) for b in self.bioms.values()]:
                            points += 2
                            barva = next((k for k, v in self.bioms.items() if sum(v) == 1), None)
                    case "event":
                        points = card.evaluate(self)
                        if 'event' in self.buffs:
                            points += 1
        return points, barva
                        
            

    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            maxpoints = -100
            maxid = None
            for xi in playables:
                points, barva = self.evaluate_card(self.stored.cards[xi], game)
                if points > maxpoints:
                    maxpoints = points
                    maxid = xi
            if maxpoints > 0:
                return True , maxid
            else:
                return False, None
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected = maxs
        else:
            goal = card.level
            selectable = []
            if maxs[5]>=goal:
                selected[5] = goal
            else:
                selected[5] = maxs[5]
                maxs[5] = 0
            while sum(selected)<goal:
                selectable = [idx for idx, val in enumerate(maxs) if val > 0]
                col = random.sample(selectable, 1)[0]
                if sum(selected)+maxs[col]> goal:
                    selected[col] += goal - sum(selected)
                else:
                    selected[col] += maxs[col]
                    maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        if barva is not None:
            card.actually_play(self, barva)
        else:
            colors = []
            for id, (barva, biom) in enumerate(self.bioms.items()):
                colors.append(barva)
            col = random.sample(colors, 1)[0]
            card.actually_play(self, col)
            


            