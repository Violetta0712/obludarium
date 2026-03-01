import random 
import classes.logic.Card as card
class Deck:
    def __init__(self):
        self.cards = []
        self.isplayable = False
        self.isstorable = False
    def play_card(self, id, person, game):
        played_card = self.cards.pop(id)
        return played_card.play(person)
    def store_card(self, id, person, game, price = 1):
        played_card = self.cards.pop(id)
        game.played_cards.append(played_card.id)
        person.pay(price)
        if played_card.card_type == "objective":
            person.evaluation.append(played_card.eval)
        for mct in game.mcts:
            mcts = game.players[mct]
            if mcts.seen[game.current_deck] == -1:
                mcts.sets[person.id].append(0)
                played_card.status[mct] = 0
            else:
                mctid = int(str(game.round-1)+str(game.current_deck)+str(mcts.seen[game.current_deck]))
                mcts.sets[person.id].append(mctid)
                played_card.status[mct] = mctid
        
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
                    new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"], cardinfo['akce'])
                case 'TU':
                    new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'], cardinfo['evaluace'])
                case 'U':
                    new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'])
                case _:
                    new_card = cardinfo['typ'] + cardinfo['jmeno']
            self.cards.append(new_card)
    def play_card(self, id, person, game):
        result = super().play_card(id, person, game)
        self.isplayable = False
        self.isstorable = False
        person.had_played = True
        if result:
            return result
    def store_card(self, id, person, game, price=1):
        super().store_card(id, person, game,  price)
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
        self.isstorable = False
    def play_card(self, id, person, game):
        played_card = self.cards.pop(id)
        for mct in game.mcts:
            mcts = game.players[mct]
            if played_card.status[mct] != -1:
                mcts.sets[person.id].remove(played_card.status[mct])
        return played_card.play(person)

def make_card(game, person, cardid):
    cardinfo = game.reference[cardid]
    game.game_deck.remove(cardid)
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
            new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"], cardinfo['akce'])
        case 'TU':
            new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'], cardinfo['evaluace'])
        case 'U':
            new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'])
        case _:
            new_card = cardinfo['typ'] + cardinfo['jmeno']
    for mct in game.mcts:
        mcts = game.players[mct]
        mcts.sets[person.id].append(0)
        new_card.status[mct] = 0
    person.stored.cards.append(new_card)


def sample_cards(game, person, c_num):
    cardids = random.sample(game.game_deck, c_num)
    for cardid in cardids:
            cardinfo = game.reference[cardid]
            game.game_deck.remove(cardid)
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
                    new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"], cardinfo['akce'])
                case 'TU':
                    new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'], cardinfo['evaluace'])
                case 'U':
                    new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'])
                case _:
                    new_card = cardinfo['typ'] + cardinfo['jmeno']
            for mct in game.mcts:
                mcts = game.players[mct]
                mcts.sets[person.id].append(0)
                new_card.status[mct] = 0
            person.stored.cards.append(new_card)


class SimulDeck(Deck):
    def __init__(self, id, game_deck, card_ref, cardids):
        super().__init__()
        self.id = id
        self.isplayable = True
        self.isstorable = True
        self.cardids = cardids
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
                    new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"], cardinfo['akce'])
                case 'TU':
                    new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'], cardinfo['evaluace'])
                case 'U':
                    new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['akce'])
                case _:
                    new_card = cardinfo['typ'] + cardinfo['jmeno']
            self.cards.append(new_card)
    def play_card(self, id, person, game):
        result = super().play_card(id, person, game)
        self.isplayable = False
        self.isstorable = False
        person.had_played = True
        if result:
            return result
    def store_card(self, id, person, game, price=1):
        super().store_card(id, person, game,  price)
        self.isplayable = False
        self.isstorable = False
        person.had_played = True