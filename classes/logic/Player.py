import classes.logic.Deck as deck
import math
class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = deck.Deck()
        self.bioms = {"modra":[2,0], "cerna":[2,0], "hneda":[2,0], "zelena":[2,0], "zlata":[2,0], "fialova":[2,0]}
        self.occupied = {"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
        self.upgrades = deck.Deck()
        self.for_scoring = deck.Deck()
        self.buffs = []
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
        return [initial_fury, cages_used, money_used, loans_taken, s_goal]
        

        



            


            