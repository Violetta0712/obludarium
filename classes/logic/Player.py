import classes.logic.Deck as deck
import math
import random
import functions.functions as f
import copy

class Player:
    def __init__(self, id, player_type):
        self.id = id
        self.player_type = player_type
        self.played = deck.Deck()
        self.bioms = {"modra":[0,0], "cerna":[0,0], "hneda":[0,0], "zelena":[0,0], "zlata":[0,0], "fialova":[0,0]}
        self.occupied = {"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
        self.upgrades = deck.Deck()
        self.for_scoring = deck.Deck()
        self.buffs = []
        self.evaluation = []
        self.seasons_won = 0
        self.season_buff = None
        self.stored = deck.StoredDeck()
        self.monsters = deck.Deck()
        self.money = 4
        self.loans = 0
        self.cages = 0
        self.had_played = False
    def pay(self, price):
        if self.money >= price:
            self.money -= price
        else:
            debt = self.money - price
            loan_num = math.ceil(-1*debt/3)
            self.loans += loan_num
            self.money = (debt + loan_num*3)
    def pay_biom(self, level, color):
        self.bioms[color][0]-=level
        self.bioms[color][1]+=level
    def end_season(self, grant, season):
        grant += self.buffs.count('safe')
        fury = 0
        s_goal = 0
        if season== "agro":
            for card in self.played.cards:
                fury += card.fury
                s_goal += card.fury
        else:
            for card in self.played.cards:
                fury += card.fury
                s_goal += (1 if season == card.color else 0)*card.points
        initial_fury = fury
        fury -= grant
        cages_used = 0
        money_used = 0
        loans_taken = 0
        while fury > 0 and self.cages >0:
            self.cages -= 1
            fury -= 1
            cages_used += 1
        while fury >0 and self.money >2:
            self.money -= 3
            fury -= 1
            money_used += 3
        if fury >0:
            self.loans += fury
            loans_taken = fury
            fury = 0
        return [initial_fury, grant, cages_used, money_used, loans_taken, s_goal]
    
    def score(self):
        monster_points = 0
        objective_points = 0
        money_points = self.money
        cage_points = self.cages
        season_points = self.seasons_won *3
        loan_penalty = self.loans* -5
        for monster in self.monsters.cards:
            monster_points += monster.points
        for ob in self.stored.cards: 
            if ob.card_type == "objective":
                objective_points += ob.score(self)
        return [monster_points, objective_points, money_points, cage_points, season_points, loan_penalty]
        

        

class AIstupid(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        i = random.sample(range(len(deck.cards)),1)[0]
        return [i, 'play', None]
    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            return True, random.sample(playables,1)[0]
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected == maxs
        goal = card.level
        selectable = []
        while sum(selected)<goal:
            selectable = [idx for idx, val in enumerate(maxs) if val > 0]
            col = random.sample(selectable, 1)[0]
            if sum(selected)+maxs[col]> goal:
                selected[col] += goal - sum(selected)
            else:
                selected[col] += maxs[col]
                maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        colors = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            colors.append(barva)
        col = random.sample(colors, 1)[0]
        card.actually_play(self, col)

        

    
class AIgamble(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        playables = []
        for xi in range(len(deck.cards)):
            if deck.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            playables = range(len(deck.cards))
        i = random.sample(playables,1)[0]
        return [i, 'play', None]
    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            return True, random.sample(playables,1)[0]
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected = maxs
        else:
            goal = card.level
            selectable = []
            if maxs[5]>=goal:
                selected[5] = goal
            else:
                selected[5] = maxs[5]
                maxs[5] = 0
            while sum(selected)<goal:
                selectable = [idx for idx, val in enumerate(maxs) if val > 0]
                col = random.sample(selectable, 1)[0]
                if sum(selected)+maxs[col]> goal:
                    selected[col] += goal - sum(selected)
                else:
                    selected[col] += maxs[col]
                    maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        colors = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            colors.append(barva)
        col = random.sample(colors, 1)[0]
        card.actually_play(self, col)

    
class AIminmax(Player):
    def __init__(self, id, player_type):
        super().__init__(id, player_type)
    
    def choose(self, deck, game):
        maxpoints = -100
        maxid = None
        barva = None
        zp = 0
        p = 0
        action = 'play'
        if 'zadne_pujcky' in self.evaluation and self.loans == 0:
            zp = 6
        if 'pujcky' in self.evaluation:
            p = 2
        for i in range(len(deck.cards)):
            card = deck.cards[i]
            if not card.isplayable(self) and card.card_type == "objective":
                points = card.score(self) - (1 if self.money > 0 else (3 + p - zp))
                if 'ukoly' in self.evaluation:
                    points += 2
            elif not card.isplayable(self):
                points = -(1 if self.money > 0 else (3 + p - zp))
            else:
                points, barva = self.evaluate_card(card, game)
            if points > maxpoints:
                maxpoints = points
                maxid = i
            if maxpoints < 0:
                action = 'store'
                maxid = random.sample(range(len(deck.cards)),1)[0]
        return [maxid, action, barva]
    
    def evaluate_card(self, card, game):
        points = 0
        barva = None
        zp = 0
        p = 0
        if 'zadne_pujcky' in self.evaluation and self.loans == 0:
            zp = 6
        if 'pujcky' in self.evaluation:
            p = 2
        match card.card_type:
                    case "monster":
                        points = card.points
                        points += game.will_win_seas(self, card)
                        if card.color == self.season_buff:
                            points += 2
                        if card.color in self.buffs:
                            points += 2
                        if "agro" in self.buffs:
                            points += card.fury
                        if self.season_buff == "agro" and card.fury > 0:
                            points += 2
                        elif self.season_buff == card.color:
                            points += 2
                        if card.color in self.evaluation:
                            points += 2
                        if card.fury > 0 and "besneni" in self.evaluation:
                            points += card.fury
                        if card.level == 1 and "mala" in self.evaluation:
                            points += 1
                        if card.level == 3 and "velka" in self.evaluation:
                            points += 2
                        elif card.level >4 and "velka" in self.evaluation:
                            points += 3
                    case "biom":
                        points = 0
                        if 'velky_biom' in self.evaluation and sum(self.bioms[card.color]) < 7 and sum(self.bioms[card.color]) + card.level >= 7:
                            points += 7
                        if  'mnoho_biomů' in self.evaluation and sum(self.bioms[card.color]) == 1:
                            points += 2
                        if 'fialovy_biom' in self.evaluation and card.color == 'fialova':
                            points += 2
                        if 'vzdaleny_biom' in self.evaluation and card.pre > 0:
                            points += 2
                        if 'malo_biomů' in self.evaluation:
                            biom_num = 0
                            for biom in self.bioms:
                                if sum(self.bioms[biom]) >0:
                                    biom_num += 1
                            if biom_num <= 3 and sum(self.bioms[card.color]) ==0:
                                points -= 7
                            elif biom_num == 4 and sum(self.bioms[card.color]) ==0:
                                points -= 4
                    case "employee":
                        points = (-card.price if self.money >= card.price else (-card.price - 2 + p - zp))
                        if 'zamestnanci' in self.evaluation:
                            points += 3
                        if card.action == "add_biom" and 'velky_biom' in self.evaluation and max([sum(b) for b in self.bioms.values()]) == 6:
                            points += 7
                            barva = next((k for k, v in self.bioms.items() if sum(v) == 6), None)
                        elif card.action == "add_biom" and 'mnoho_biomů' in self.evaluation and 1 in [sum(b) for b in self.bioms.values()]:
                            points += 2
                            barva = next((k for k, v in self.bioms.items() if sum(v) == 1), None)
                    case "event":
                        points = card.evaluate(self)
                        if 'event' in self.buffs:
                            points += 1
        return points, barva
                        
            

    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            maxpoints = -100
            maxid = None
            for xi in playables:
                points, barva = self.evaluate_card(self.stored.cards[xi], game)
                if points > maxpoints:
                    maxpoints = points
                    maxid = xi
            if maxpoints > 0:
                return True , maxid
            else:
                return False, None
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected = maxs
        else:
            goal = card.level
            selectable = []
            if maxs[5]>=goal:
                selected[5] = goal
            else:
                selected[5] = maxs[5]
                maxs[5] = 0
            while sum(selected)<goal:
                selectable = [idx for idx, val in enumerate(maxs) if val > 0]
                col = random.sample(selectable, 1)[0]
                if sum(selected)+maxs[col]> goal:
                    selected[col] += goal - sum(selected)
                else:
                    selected[col] += maxs[col]
                    maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        if barva is not None:
            card.actually_play(self, barva)
        else:
            colors = []
            for id, (barva, biom) in enumerate(self.bioms.items()):
                colors.append(barva)
            col = random.sample(colors, 1)[0]
            card.actually_play(self, col)
            


class AIMCTS(Player):
    def __init__(self, id, player_type, player_num):
        super().__init__(id, player_type)
        self.known = [[[] for _ in range(player_num)] for _ in range(4)]
        self.seen = [-1] * player_num
        self.sets = [[] for _ in range(player_num)]
    
    def start_turn(self, deck, game):
        if self.seen[game.current_deck] != -1:
            cardids = [card.id for card in deck.cards]
            for id in self.known[game.round-1][game.current_deck][self.seen[game.current_deck]].copy():
                if id in cardids:
                    self.known[game.round-1][game.current_deck][self.seen[game.current_deck]].remove(id)
        self.known[game.round-1][game.current_deck].append([card.id for card in deck.cards])
        self.seen[game.current_deck] += 1
    
    def discretize(self, game):
        pass
    def choose(self, deck, game):
        i = random.sample(range(len(deck.cards)),1)[0]
        return [i, 'play', None]
    
    def want(self, game):
        playables = []
        for xi in range(len(self.stored.cards)):
            if self.stored.cards[xi].isplayable(self):
                playables.append(xi)
        if playables == []:
            return False, None
        else:
            return True, random.sample(playables,1)[0]
    
    def play_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        maxs = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            maxs.append(biom[0])
        if sum(selected)==sum(maxs):
            selected == maxs
        goal = card.level
        selectable = []
        while sum(selected)<goal:
            selectable = [idx for idx, val in enumerate(maxs) if val > 0]
            col = random.sample(selectable, 1)[0]
            if sum(selected)+maxs[col]> goal:
                selected[col] += goal - sum(selected)
            else:
                selected[col] += maxs[col]
                maxs[col] = 0
        card.actually_play(self, selected)
    
    def play_biom_e(self, card, barva = None):
        colors = []
        for id, (barva, biom) in enumerate(self.bioms.items()):
            colors.append(barva)
        col = random.sample(colors, 1)[0]
        card.actually_play(self, col)
    


class Root:
    def __init__(self, game, mcts, msg = None, b_card = None):
        self.parent = None
        self.children = []
        self.visits = 0
        self.wins = 0
        self.biom_card = b_card
        self.players = game.players.copy()
        self.round = game.round
        self.turn = game.turn
        self.colors = ["modra", "cerna", "hneda", "zelena", "zlata"]
        random.shuffle(self.colors)
        self.msg = msg
        self.results = []
        self.order = []
        self.mcts = []
        self.played_cards = []
        self.current_player = game.current_player
        self.firstplayerdeck = game.firstplayerdeck
        self.seasondeck = game.seasondeck.copy()
        random.shuffle(self.seasondeck)
        self.s_ref = game.s_ref
        self.season = game.season
        self.reference = game.reference
        self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
        game_deck = f.load_deck()
        played = game.played_cards.copy()
        in_deck = [item for round in mcts.known
                    for player in round
                    for turn in player
                    for item in turn]
        played.extend(in_deck)
        self.game_deck = [item for item in game_deck if item not in played]
        random.shuffle(self.game_deck)
        for player in self.players:
            if player.id == mcts.id:
                pass
            else:
                player.stored.cards = []
                for card in mcts.sets[player.id]:
                    if card == 0:
                        deck.sample_cards(self, player, 1)
                    else:
                        random_card = random.sample(mcts.known[card[0]][card[1]][card[2]], 1)[0]
                        mcts.known[card[0]][card[1]][card[2]].remove(random_card)
                        deck.make_card(self, player, random_card)
        self.hands = []
        for i in range(len(mcts.seen)):
            if mcts.seen[i] == -1:
                modifier = 1 if (i if i > self.firstplayerdeck else i + self.firstplayerdeck) < (i if i > self.current_deck else i + self.current_deck) else 0
                card_num = 9-self.turn - modifier
                cardids = random.sample(self.game_deck, card_num)
                for cardid in cardids:
                    self.game_deck.remove(cardid)
                new_hand = deck.SimulDeck(i, self.game_deck, self.reference, cardids)
            else:
                new_hand = mcts.known[self.round-1][i][-1]
            self.hands.append(new_hand)
    
    def create_children(self):
        if self.round == 5:
            return
        if self.biom_card is not None:
            for color in self.colors:
                new_child = Child(self)
                self.biom_card.actually_play(new_child.state.players[new_child.state.current_player], color)
                new_child.state.biom_card = None
                self.children.append(new_child)
        else:
            for c in range(len(self.players[self.current_player].stored.cards)):
                if self.players[self.current_player].stored.cards[c].isplayable(self.players[self.current_player]):
                    new_child = Child(self)
                    played_card = self.players[self.current_player].stored.cards[c]
                    msg = new_child.state.players[self.current_player].stored.play_card(c, new_child.state.players[self.current_player],new_child.state)
                    if played_card.card_type == "monster" and played_card.cards>0:
                        for i in range(played_card.cards):
                            deck.make_card(new_child.state, new_child.state.players[self.current_player], new_child.state.game_deck[0])
                            new_child.state.game_deck.pop(0)
                    if msg == "biom":
                        new_child.state.biom_card = played_card
                    elif msg == "purple":
                        choice = self.choose_purple(played_card)
                        played_card.actually_play(new_child.state.players[self.current_player], choice)
                    self.children.append(new_child)
            if self.players[self.current_player].had_played == False:
                for c in range(len(self.hands[self.current_deck].cards)):
                    if self.hands[self.current_deck].cards[c].isplayable(self.players[self.current_player]):
                        new_child = Child(self)
                        played_card = self.hands[self.current_deck].cards[c]
                        msg = new_child.state.hands[self.current_deck].play_card(c, new_child.state.players[new_child.state.current_player],new_child.state)
                        if played_card.card_type == "monster" and played_card.cards>0:
                            for i in range(played_card.cards):
                                deck.make_card(new_child.state, new_child.state.players[self.current_player], new_child.state.game_deck[0])
                                new_child.state.game_deck.pop(0)
                        if played_card.card_type == "monster" and played_card.cards>0:
                            for i in range(played_card.cards):
                                deck.make_card(new_child.state, new_child.state.players[self.current_player], new_child.state.game_deck[0])
                                new_child.state.game_deck.pop(0)
                        if msg == "biom":
                            new_child.state.msg = "biom"
                        elif msg == "purple":
                            choice = self.choose_purple(played_card)
                            played_card.actually_play(new_child.state.players[self.current_player], choice)
                        self.children.append(new_child)
                    new_child = Child(self)
                    new_child.state.hands[self.current_deck].store_card(c, new_child.state.players[new_child.state.current_player],new_child.state)
                    self.children.append(new_child)
            else:
                new_child = Child(self)
                new_child.state.players[new_child.state.current_player].had_played = False
                self.progress(new_child.state)
                self.children.append(new_child)

    def choose_purple(self, card):
        selected = [0, 0, 0, 0, 0, 0]
        goal = card.level
        maxs = []
        for id, (barva, biom) in enumerate(self.players[self.current_player].bioms.items()):
            maxs.append(biom[0])
        goal = card.level
        selectable = []
        if maxs[5]>=goal:
            selected[5] = goal
        else:
            selected[5] = maxs[5]
            maxs[5] = 0
        clr = 0
        while sum(selected)<goal:
            selectable = [idx for idx, val in enumerate(maxs) if val > 0]
            col = self.colors[clr]
            if sum(selected)+maxs[col]> goal:
                selected[col] += goal - sum(selected)
            else:
                selected[col] += maxs[col]
                maxs[col] = 0
            clr += 1
        return selected
    
    def progress(self, game):
        if game.current_player < len(game.players)-1:
            game.current_player += 1
            game.current_deck = (game.current_player+game.firstplayerdeck)%len(game.players)
        else:
            game.current_player = 0
            if game.turn <8: 
                game.turn += 1
                game.firstplayerdeck = (game.firstplayerdeck+len(game.hands)+(-1)**game.round)%len(game.players)
                game.current_deck = (game.current_player+game.firstplayerdeck)%len(game.players)
            else:
                game.turn = 1
                game.firstplayerdeck = 0
                game.current_deck = (game.current_player+game.firstplayerdeck)%len(game.players)
                game.round+=1
                for player in game.players:
                    player.monsters.cards.extend(player.played.cards)
                    player.played.cards = []
                    player.occupied ={"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
                    for biom in player.bioms:
                        player.bioms[biom][0] += player.bioms[biom][1]
                        player.bioms[biom][1] = 0
                game.season = game.seasondeck[0]
                game.seasondeck.remove(game.season)
                for p in game.players:
                    p.season_buff = self.s_ref[game.season]['akce']
                game.hands = []
                for i in range(len(game.players)):
                    cardids = game.deck[0:8]
                    new_hand = deck.SimulDeck(i, game.game_deck, game.reference, cardids)
                    for cardid in cardids:
                        game.game_deck.remove(cardid)
                    game.hands.append(new_hand)

            


class Child:
    def __init__(self, game):
        self.parent = game
        self.state = copy.deepcopy(game)
        self.children = []
        self.visits = 0
        self.wins = 0
        