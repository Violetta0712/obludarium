import pandas as pd
import json
import params as p

def load_deck():
    deck = []
    for deck_json in p.deck_jsons:
        with open(deck_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            deck.extend(cards)
    return deck

