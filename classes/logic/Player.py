import classes.logic.Deck as deck
class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = deck.Deck()
        self.bioms = {"modra":[0,0], "cerna":[0,0], "hneda":[0,0], "zelena":[0,0], "zlata":[0,0], "fialova":[0,0]}
        self.occupied = {"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
        self.upgrades = deck.Deck()
        self.stored = deck.Deck()
        self.monsters = deck.Deck()
        self.money = 4
        self.loans = 0
    def pay(self, price):
        if self.money >= price:
            self.money -= price
        



            


            