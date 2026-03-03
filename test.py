import pygame
from classes.logic import Card as card
from classes.logic import Player as player
from classes.logic import Game as game
from classes.logic import Deck as deck
from functions import *
from assets import *
import random
import copy

players = ["AI těžké", "AI těžké", "AI těžké", "AI těžké", "AI těžké"]

g = game.Game(players)

g.season = random.sample(g.seasondeck, 1)[0]
g.seasondeck.remove(g.season)
for p in g.players:
    p.season_buff = g.s_ref[g.season]['akce']
g.hands = []
for i in range(len(g.players)):
    new_hand = deck.PlayerDeck(i, g.game_deck, g.reference)
    for j in new_hand.cardids:
        g.game_deck.remove(j)
    g.hands.append(new_hand)

for p in range(len(g.players)):
                person = g.players[p]
                g.current_player = p
                g.current_deck = (g.current_player+g.firstplayerdeck)%len(g.players)
                d = g.hands[g.current_deck]
                person.start_turn(d, g)
                info = person.choose(d, g)
                id = info[0]
                if d.cards[id].isplayable(person) and info[1] == 'play':
                    karta = d.cards[id]
                    if karta.card_type == "monster" and karta.cards>0:
                            deck.sample_cards(g, person, karta.cards)
                    msg = d.play_card(id, person, g)
                    if msg == 'fialova':
                        person.play_purple(karta)
                    if msg == 'biom':
                        if len(info)>1:
                            person.play_biom_e(karta, info[2])
                else: 
                    d.store_card(id, person, g)
                playing = True
                while playing == True:
                    playing, i = person.want(g)
                    if i is not None:
                        karta = person.stored.cards[i]
                        if karta.card_type == "monster" and karta.cards>0:
                                deck.sample_cards(g, person, karta.cards)
                        msg = person.stored.play_card(i, person, g)
                        if msg == 'fialova':
                            person.play_purple(karta)
                        if msg == 'biom':
                            person.play_biom_e(karta)
                person.had_played = False
g.turn += 1
g.firstplayerdeck = (g.firstplayerdeck+len(g.hands)+(-1)**g.round)%len(g.players)
g.current_deck = (g.current_player+g.firstplayerdeck)%len(g.players)


player.Root(g, g.players[0])