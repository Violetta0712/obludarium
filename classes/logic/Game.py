import classes.logic.Player as player
import classes.logic.Deck as deck
import functions.functions as f
import random
class Game:
    def __init__(self, player_num):
        self.players = []
        self.round = 1
        self.turn = 1
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
        for i in range(player_num):
            new_player = player.Player(i, "Human")
            for j in range(2):
                dk_card = random.sample(range(len(DK_deck.cards)), 1)[0]
                DK_deck.play_card(dk_card, new_player)
            self.players.append(new_player)
        self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
        
    def start_round(self):
        self.season = random.sample(self.seasondeck, 1)[0]
        self.seasondeck.remove(self.season)
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
            if self.round <4:
                self.round+=1
                self.start_round()
                return "season"
            else:
                return "end"


    def next_player(self):
        if self.current_player < len(self.players)-1:
            self.current_player += 1
            self.current_deck = (self.current_player+self.firstplayerdeck)%len(self.players)
            return "turn"
        else:
            self.current_player = 0
            return self.next_turn()
        
        


    
