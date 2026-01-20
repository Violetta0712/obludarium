import random 
import classes.logic.Card as card
class Deck:
    def __init__(self):
        self.cards = []
        
    
    def play_card(self, id, person):
            played_card = self.cards.pop(id)
            played_card.play(person)


class PlayerDeck(Deck):
    def __init__(self, id, game_deck, card_ref):
        super().__init__()
        self.id = id
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

class DKDeck(Deck):
    def __init__(self, game_deck, card_ref):
        super().__init__()
        self.cardids = game_deck
        for cardid in self.cardids:
            cardinfo = card_ref[cardid]
            new_card = card.HomeBiomCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['pruzkum'])
            self.cards.append(new_card)