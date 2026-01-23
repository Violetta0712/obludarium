class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def play(self, person):
        print("Played" + str(self.name))
    def isplayable(self, person):
        return False


class MonsterCard(Card): 
    def __init__(self, id, name, color, level, points, fury = 0, cards = 0): 
        super().__init__(id, name) 
        self.color = color
        self.card_type="monster"
        self.level = level
        self.points = points
        self.fury = fury
        self.cards = cards
    def isplayable(self, person):
        if person.bioms[self.color][0] >= self.level:
            return True
        else:
            return False

class PurpleMonsterCard(Card):
    def __init__(self, id, name, color, level, points, fury = 0, cards = 0): 
        super().__init__(id, name) 
        self.color = color
        self.card_type="monster"
        self.level = level
        self.points = points
        self.fury = fury
        self.cards = cards
    def isplayable(self, person):
        all_bioms = 0
        for i in person.bioms.values():
            all_bioms += i[0]
        if all_bioms >= self.level:
            return True
        else:
            return False

class BiomCard(Card):
    def __init__(self, id, name, color, level, pre = 0): 
        super().__init__(id, name) 
        self.card_type="biom"
        self.color = color
        self.level = level
        self.pre = pre
    def isplayable(self, person):
        if self.pre <= person.bioms[self.color][0]:
            return True
        else:
            return False
    def play(self, person):
        person.bioms[self.color][0] += self.level

class EmployeeCard(Card):
    def __init__(self, id, name, price):
        super().__init__(id, name)
        self.card_type="employee"
        self.price = price
    def isplayable(self, person):
        return True
    def play(self, person):
        person.upgrades.cards.append(self.name)

class ObjectiveCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.card_type = "objective"
    

class EventCard(Card):
    def __init__(self, id, name):
        super().__init__(id, name)
        self.card_type = 'event'
    def isplayable(self, person):
        return True

class HomeBiomCard(Card):
    def __init__(self, id, name, color, level): 
        super().__init__(id, name) 
        self.card_type="biom"
        self.color = color
        self.level = level
    def play(self, person):
        person.bioms[self.color][0] += 1
