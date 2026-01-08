class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name


class MonsterCard(Card): 
    def __init__(self, id, name, color, level, points, fury = 0, cards = 0): 
        super().__init__(id, name) 
        self.color = color
        self.card_type="monster"
        self.level = level
        self.points = points
        self.fury = fury
        self.cards = cards

class BiomCard(Card):
    def __init__(self, id, name, color, level, pre = 0): 
        super().__init__(id, name) 
        self.card_type="biom"
        self.color = color
        self.level = level
        self.pre = pre

class EmployeeCard(Card):
    def __init__(self, id, name, price):
        super().__init__(id, name)
        self.card_type="employee"
        self.price = price

class ObjectiveCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.card_type = "objective"
