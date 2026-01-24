import random 
import classes.logic.Card as card
class Deck:
    def __init__(self):
        self.cards = []
        self.isplayable = False
        self.isstorable = False
    def play_card(self, id, person):
        played_card = self.cards.pop(id)
        played_card.play(person)
    def store_card(self, id, person, price = 1):
        played_card = self.cards.pop(id)
        person.pay(price)
        person.stored.cards.append(played_card)


class PlayerDeck(Deck):
    def __init__(self, id, game_deck, card_ref):
        super().__init__()
        self.id = id
        self.isplayable = True
        self.isstorable = True
        self.cardids = random.sample(game_deck, 8)
        for cardid in self.cardids:
            cardinfo = card_ref[cardid]
            match cardinfo['typ']:
                case 'K':
                    pre = cardinfo.get("prerekvizity", 0)
                    new_card = card.BiomCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['pruzkum'], pre)
                case 'O':
                    fury = cardinfo.get("besneni", 0)
                    extra = cardinfo.get("karty", 0)
                    if cardinfo['barva'] == 'fialova':
                        new_card = card.PurpleMonsterCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['uroven'], cardinfo['body'], fury, extra)
                    else:
                        new_card = card.MonsterCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['uroven'], cardinfo['body'], fury, extra)
                case 'P':
                    new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"])
                case 'TU':
                    new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'])
                case 'U':
                    new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'])
                case _:
                    new_card = cardinfo['typ'] + cardinfo['jmeno']
            self.cards.append(new_card)
    def play_card(self, id, person):
        super().play_card(id, person)
        self.isplayable = False
        self.isstorable = False
        person.had_played = True
    def store_card(self, id, person, price=1):
        super().store_card(id, person, price)
        self.isplayable = False
        self.isstorable = False
        person.had_played = True
class DKDeck(Deck):
    def __init__(self, game_deck, card_ref):
        super().__init__()
        self.cardids = game_deck
        for cardid in self.cardids:
            cardinfo = card_ref[cardid]
            new_card = card.HomeBiomCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['pruzkum'])
            self.cards.append(new_card)

class StoredDeck(Deck):
    def __init__(self):
        super().__init__()
        self.isplayable = True