import pandas as pd
import json
import params as p
import random
    

def load_deck():
    deck = []
    for deck_json in p.deck_jsons:
        with open(deck_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            ids = [item["id"] for item in cards for _ in range(item["mnozstvi"])]
            deck.extend(ids)
    return deck

def deal_hands(deck, players, hand_size):
    hands = []
    for i in range(players):
        hand = random.sample(deck, hand_size)
        for card in hand:
            deck.remove(card)
        hands.append(hand)
    return deck, hands

