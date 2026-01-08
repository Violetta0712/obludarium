import classes.logic.Player as player
import classes.logic.Deck as deck
import functions.functions as f
class Game:
    def __init__(self, player_num):
        self.players = []
        self.round = 1
        self.hands = []
        self.game_deck = f.load_deck()
        self.reference = f.load_card_ref()
        for i in range(player_num):
            new_player = player.Player(i, "Human")
            self.players.append(new_player)
        for i in range(player_num):
            new_hand = deck.Deck(i, self.game_deck, self.reference)
            for j in new_hand.cardids:
                self.game_deck.remove(j)
            self.hands.append(new_hand)
        print(self.hands[0].cards)


    
