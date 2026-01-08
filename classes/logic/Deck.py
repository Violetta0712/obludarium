import random 
import classes.logic.Card as card
class Deck:
    def __init__(self, id, game_deck, card_ref):
        self.id = id
        self.cardids = random.sample(game_deck, 8)
        self.cards = []
        for cardid in self.cardids:
            cardinfo = card_ref[cardid]
            if cardinfo['typ']=='K':
                pre = cardinfo.get("prerekvizity", 0)
                new_card = card.BiomCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['pruzkum'], pre)
            elif cardinfo['typ']=='O':
                fury = cardinfo.get("besneni", 0)
                extra = cardinfo.get("karty", 0)
                new_card = card.MonsterCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['uroven'], cardinfo['body'], fury, extra)
            elif cardinfo['typ']=='P':
                new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"])
            elif cardinfo['typ']=='TU':
                new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'])
            else:
                new_card = "karta"
            self.cards.append(new_card)

        