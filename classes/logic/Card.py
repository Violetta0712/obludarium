class Card:
    def __init__(self, id, name, card_type):
        self.id = id
        self.name = name
        self.card_type = card_type


class MonsterCard(Card): 
    def __init__(self, id, name, color, level, points, fury = 0, cards = 0): 
        super().__init__(id, name, card_type="monster") 
        self.color = color
        self.level = level
        self.points = points
        self.fury = fury
        self.cards = cards

class BiomCard(Card):
    def __init__(self, id, name, color, level, pre): 
        super().__init__(id, name, card_type="biom") 
        self.color = color
        self.level = level
