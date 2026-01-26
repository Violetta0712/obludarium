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

def load_DK_ref():
    deck = []
    for s_json in p.DK_jsons:
        with open(s_json, 'r', encoding='utf-8') as file:
            cards = json.load(file)
            deck.extend(cards)
    final_deck = {r['id']:r for r in deck}
    return final_deck

def load_DK():
    deck = []
    for deck_json in p.DK_jsons:
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


def give_two_coins(person):
    person.money += 2

def give_blue_coins(person):
    person.money += sum(person.bioms['modra'])

def give_black_coins(person):
    person.money += sum(person.bioms['cerna'])

def give_brown_coins(person):
    person.money += sum(person.bioms['hneda'])

def give_green_coins(person):
    person.money += sum(person.bioms['zelena'])

def give_yellow_coins(person):
    person.money += sum(person.bioms['zlata'])

def give_cage(person):
    person.cages += 1

def give_monster_coins(person):
    monster_num = 0
    for i in person.stored.cards:
        if i.card_type == "monster":
            monster_num += 1
    person.money += monster_num

def give_employee_coins(person):
    person.money += len(person.upgrades.cards)

def add_blue_buff(person):
    person.buffs.append('modra')

def add_black_buff(person):
    person.buffs.append('cerna')

def add_brown_buff(person):
    person.buffs.append('hneda')

def add_green_buff(person):
    person.buffs.append('zelena')

def add_yellow_buff(person):
    person.buffs.append('zlata')

def add_event_buff(person):
    person.buffs.append('event')

def add_agro_buff(person):
    person.buffs.append('agro')

def add_safe_buff(person):
    person.buffs.append('safe')

def add_biom(person):
    return 'kolděda'


ACTIONS = {
    "give_two_coins": give_two_coins,
    "give_blue_coins": give_blue_coins,
    "give_black_coins": give_black_coins,
    "give_brown_coins": give_brown_coins,
    "give_green_coins": give_green_coins,
    "give_yellow_coins": give_yellow_coins,
    "give_cage": give_cage,
    "give_monster_coins": give_monster_coins,
    "give_employee_coins": give_employee_coins,
    "add_blue_buff": add_blue_buff,
    "add_black_buff": add_black_buff,
    "add_brown_buff": add_brown_buff,
    "add_green_buff": add_green_buff,
    "add_yellow_buff": add_yellow_buff,
    "add_event_buff": add_event_buff,
    "add_agro_buff": add_agro_buff,
    "add_safe_buff": add_safe_buff,
    "add_biom": add_biom
}