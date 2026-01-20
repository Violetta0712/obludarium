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
        
    def start_round(self):
        self.season = random.sample(self.seasondeck, 1)[0]
        self.seasondeck.remove(self.season)
        for i in range(len(self.players)):
            new_hand = deck.PlayerDeck(i, self.game_deck, self.reference)
            for j in new_hand.cardids:
                self.game_deck.remove(j)
            self.hands.append(new_hand)
        
        


    
