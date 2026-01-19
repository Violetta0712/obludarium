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

def load_card_ref():
    ref = []
    for all_json in p.all_jsons:
        with open(all_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            ref.extend(cards)
    final_ref = {r['id']:r for r in ref}
    return final_ref

def load_season_ref():
    deck = []
    for s_json in p.season_jsons:
        with open(s_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            deck.extend(cards)
    final_deck = {r['id']:r for r in deck}
    return final_deck

def load_seasons():
    deck = []
    for s_json in p.season_jsons:
        with open(s_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            deck.extend(cards)
    final_deck = [r['id'] for r in deck]
    return final_deck


def deal_hands(deck, players, hand_size):
    hands = []
    for i in range(players):
        hand = random.sample(deck, hand_size)
        for card in hand:
            deck.remove(card)
        hands.append(hand)
    return deck, hands

