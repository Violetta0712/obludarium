import classes.ux.TextBox as textbox
import pygame
import functions.functions as f
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
    def play(self, person):
        person.occupied[self.color].append(PlayedMonster(self.level, self.name, self.fury, self.points))
        person.played.cards.append(self)
        person.pay_biom(self.level, self.color)
        if self.color in person.buffs:
            person.money += 2
        if 'agro' in person.buffs:
            person.money += self.fury
        if person.season_buff == self.color:
            person.money += 2
            person.season_buff = None
        if person.season_buff == 'agro' and self.fury>0:
            person.money += 2
            person.season_buff = None

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
    def play(self,person):
        return "párek"
    def actually_play(self, person, selected):
        person.played.cards.append(self)
        barvy= [c for c in person.bioms]
        if 'agro' in person.buffs:
            person.money += self.fury
        if person.season_buff == self.color:
            person.money += 2
            person.season_buff = None
        if person.season_buff == 'agro' and self.fury>0:
            person.money += 2
            person.season_buff = None
        for i in range(len(selected)):
            if selected[i]>0:
                col = barvy[i]
                person.bioms[col][0]-=selected[i]
                person.bioms[col][1]+=selected[i]
                person.occupied[col].append(PlayedMonster(selected[i], self.name, self.fury, self.points))



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
        person.for_scoring.cards.append(self)

class EmployeeCard(Card):
    def __init__(self, id, name, price, action):
        super().__init__(id, name)
        self.card_type="employee"
        self.price = price
        self.action = action
    def isplayable(self, person):
        return True
    def play(self, person):
        person.pay(self.price)
        person.upgrades.cards.append(self)
        func = f.ACTIONS[self.action]
        return func(person)
    def actually_play(self, person, barva):
        person.bioms[barva][0] += 1

class ObjectiveCard(Card):
    def __init__(self, id, name, action):
        super().__init__(id, name)
        self.card_type = "objective"
        self.action = action
    def score(self, person):
        func = f.ACTIONS[self.action]
        return func(person)
    

class EventCard(Card):
    def __init__(self, id, name, action):
        super().__init__(id, name)
        self.card_type = 'event'
        self.action = action
    def isplayable(self, person):
        return True
    def play(self, person):
        func = f.ACTIONS[self.action]
        func(person)
        if 'event' in person.buffs:
            person.money += 1


class HomeBiomCard(Card):
    def __init__(self, id, name, color, level): 
        super().__init__(id, name) 
        self.card_type="biom"
        self.color = color
        self.level = level
    def play(self, person):
        person.bioms[self.color][0] += 1

class PlayedMonster:
    def __init__(self, level, name, besneni, points):
        self.level = level
        self.name = name
        self.besneni = besneni
        self.points = points
    def create_visual(self, x, y, w, h):
        vs = []
        v = textbox.TextBox(x, y, w, h, str(self.level)+str(self.name)+str(self.besneni)+str(self.points),pygame.font.SysFont(None, 48), (255, 204, 153),(102, 180, 0))
        vs.append(v)
        return(vs)
