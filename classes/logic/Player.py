class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = []
        self.bioms = {"modra":[0,0], "cerna":[0,0], "hneda":[0,0], "zelena":[0,0], "zlata":[0,0], "fialova":[0,0]}
        self.upgrades = []
        self.stored = []
        self.monsters = []
