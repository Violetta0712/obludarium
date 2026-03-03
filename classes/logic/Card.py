import classes.ux.TextBox as textbox
import pygame
import functions.functions as f
class Card:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.status = [-1] *5
        self.cost = [0, 0, 0]
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
        self.s_buff_lost = None
    def isplayable(self, person):
        if person.bioms[self.color][0] >= self.level:
            return True
        else:
            return False
    def play(self, person):
        person.occupied[self.color].append(PlayedMonster(self.level, self.name, self.fury, self.points))
        person.played.cards.append(self)
        person.pay_biom(self.level, self.color)
        self.cost = [0, 0, 0]
        if self.color in person.buffs:
            self.cost[0] += 2
        if 'agro' in person.buffs:
            self.cost[0] += self.fury
        if person.season_buff == self.color:
            self.cost[0] += 2
            self.s_buff_lost = person.season_buff
            person.season_buff = None
        if person.season_buff == 'agro' and self.fury>0:
            self.cost[0] += 2
            person.season_buff = None
        person.money += self.cost[0]
    def undo_play(self, person):
        person.played.cards.remove(self)
        person.unpay_biom(self.level, self.color)

class PurpleMonsterCard(Card):
    def __init__(self, id, name, color, level, points, fury = 0, cards = 0): 
        super().__init__(id, name) 
        self.color = color
        self.card_type="monster"
        self.level = level
        self.points = points
        self.fury = fury
        self.cards = cards
        self.s_buff_lost = None
        self.selected = None
    def isplayable(self, person):
        all_bioms = 0
        for i in person.bioms.values():
            all_bioms += i[0]
        if all_bioms >= self.level:
            return True
        else:
            return False
    def play(self,person):
        return "fialova"
    def actually_play(self, person, selected):
        self.selected = selected
        person.played.cards.append(self)
        barvy= [c for c in person.bioms]
        self.cost = [0, 0, 0]
        if 'agro' in person.buffs:
            self.cost[0] += self.fury
        if person.season_buff == self.color:
            self.s_buff_lost = person.season_buff
            self.cost[0] += 2
            person.season_buff = None
        if person.season_buff == 'agro' and self.fury>0:
            self.cost[0] += 2
            person.season_buff = None
        person.money += self.cost[0]
        for i in range(len(selected)):
            if selected[i]>0:
                col = barvy[i]
                person.bioms[col][0]-=selected[i]
                person.bioms[col][1]+=selected[i]
                person.occupied[col].append(PlayedMonster(selected[i], self.name, self.fury, self.points))
    def undo_play(self, person, selected):
        person.played.cards.remove(self)
        barvy= [c for c in person.bioms]
        for i in range(len(selected)):
            if selected[i]>0:
                col = barvy[i]
                person.bioms[col][0]+=selected[i]
                person.bioms[col][1]-=selected[i]



class BiomCard(Card):
    def __init__(self, id, name, color, level, pre = 0): 
        super().__init__(id, name) 
        self.card_type="biom"
        self.color = color
        self.level = level
        self.pre = pre
    def isplayable(self, person):
        if self.pre <= sum(person.bioms[self.color]):
            return True
        else:
            return False
    def play(self, person):
        person.bioms[self.color][0] += self.level
        person.for_scoring.cards.append(self)
    def undo_play(self, person):
        person.bioms[self.color][0] -= self.level
        person.for_scoring.cards.remove(self)

class EmployeeCard(Card):
    def __init__(self, id, name, price, action):
        super().__init__(id, name)
        self.card_type="employee"
        self.price = price
        self.action = action
        self.actual_color = None
    def isplayable(self, person):
        return True
    def play(self, person):
        self.cost = person.pay(self.price)
        person.upgrades.cards.append(self)
        func = f.ACTIONS[self.action]
        return func(person)
    def actually_play(self, person, barva):
        person.bioms[barva][0] += 1
        self.actual_color = barva
    def undo_play(self, person):
        person.upgrades.cards.remove(self)
        if self.actual_color is not None:
            person.bioms[self.actual_color][0] -= 1
            self.actual_color = None
        
    

class ObjectiveCard(Card):
    def __init__(self, id, name, action, eval):
        super().__init__(id, name)
        self.card_type = "objective"
        self.action = action
        self.eval = eval
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
        self.cost = func(person)
        if 'event' in person.buffs:
            person.money += 1
            self.cost[0] += 1
        person.for_scoring.cards.append(self)
    def evaluate(self, person):
        func = f.ACTIONS[self.action]
        return func(person, "eval")
    def undo_play(self, person):
        person.for_scoring.cards.remove(self)


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
        level = textbox.TextBox(x, y, w/6, h, str(self.level),pygame.font.SysFont('gabriola', 30), (161, 151, 151),(0,0,0))
        vs.append(level)
        text = textbox.TextBox(x+w/6, y, 3*w/6, h, str(self.name),pygame.font.SysFont('gabriola', 20), (161, 151, 151),(0,0,0))
        vs.append(text)
        fury = textbox.TextBox(x+4*w/6, y, w/6, h, str(self.besneni),pygame.font.SysFont('gabriola', 30), (219, 0, 0),(0,0,0))
        vs.append(fury)
        points = textbox.TextBox(x+5*w/6, y, w/6, h, str(self.points),pygame.font.SysFont('gabriola', 30), (219, 182, 0),(0,0,0))
        vs.append(points)
        return(vs)
