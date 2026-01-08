class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = []
        self.stored = []
        self.monsters = []
