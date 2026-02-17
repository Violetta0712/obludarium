import classes.logic.Player as player
import classes.logic.Deck as deck
import functions.functions as f
import random
class Game:
    def __init__(self, player_ents):
        self.players = []
        self.round = 1
        self.turn = 1
        self.results = []
        self.order = []
        self.current_player = 0
        self.firstplayerdeck = 0
        self.hands = []
        self.seasondeck = f.load_seasons()
        self.s_ref = f.load_season_ref()
        self.season = None
        self.game_deck = f.load_deck()
        self.reference = f.load_card_ref()
        DK = f.load_DK()
        DK_ref = f.load_DK_ref()
        DK_deck = deck.DKDeck(DK, DK_ref)
        for i in range(len(player_ents)):
            if player_ents[i] != 'Žádný':
                if player_ents[i]=='Hráč':
                    new_player = player.Player(i, "Human")
                elif player_ents[i]=='AI střední':
                    new_player = player.AIminmax(i, "AI")
                elif player_ents[i]=='AI snadné':
                    new_player = player.AIgamble(i, "AI")
                else:
                    new_player = player.AIstupid(i, "AI")
                for j in range(2):
                    dk_card = random.sample(range(len(DK_deck.cards)), 1)[0]
                    DK_deck.play_card(dk_card, new_player)
                self.players.append(new_player)
        self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
        
    def start_round(self):
        self.season = random.sample(self.seasondeck, 1)[0]
        self.seasondeck.remove(self.season)
        for p in self.players:
            p.season_buff = self.s_ref[self.season]['akce']
        self.hands = []
        for i in range(len(self.players)):
            new_hand = deck.PlayerDeck(i, self.game_deck, self.reference)
            for j in new_hand.cardids:
                self.game_deck.remove(j)
            self.hands.append(new_hand)

    def next_turn(self):
        if self.turn <8: 
            self.turn += 1
            self.firstplayerdeck = (self.firstplayerdeck+len(self.hands)+(-1)**self.round)%len(self.players)
            self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
            return "turn"
        else:
            self.turn = 1
            self.firstplayerdeck = 0
            self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
            return 'season'
    def end_round(self):
        if self.round <4: 
            self.round+=1
            for player in self.players:
                player.monsters.cards.extend(player.played.cards)
                player.played.cards = []
                player.occupied ={"modra":[], "cerna":[], "hneda":[], "zelena":[], "zlata":[], "fialova":[]}
                for biom in player.bioms:
                    player.bioms[biom][0] += player.bioms[biom][1]
                    player.bioms[biom][1] = 0
            self.start_round()
            return "season"
        else:
            return "end"

    def next_player(self):
        if self.current_player < len(self.players)-1:
            self.current_player += 1
            self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
            if self.players[self.current_player].player_type == 'AI':
                return 'AI-turn'
            return "turn"
        else:
            self.current_player = 0
            return self.next_turn()
        
    def end_game(self):
        results = []
        for pl in self.players:
            results.append(pl.score())
        order = sorted(
            range(len(results)),
            key=lambda i: sum(results[i]),
            reverse=True
        )
        if 'second' in self.players[order[1]].buffs:
            results[order[1]][1]+= 7
        order = sorted(
            range(len(results)),
            key=lambda i: sum(results[i]),
            reverse=True
        )
        self.results = results
        self.order = order
        

        


    
