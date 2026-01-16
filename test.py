import functions.functions as f
import pandas as pd
import json
import random 
import params as p
import functions.ux as u
import pygame
import sys
import classes.ux.Button as button
import classes.ux.TextBox as textbox
import classes.logic.Card as card

card_ref = f.load_card_ref()
cardids = f.load_deck()

for cardid in cardids:
            cardinfo = card_ref[cardid]
            match cardinfo['typ']:
                case 'K':
                    pre = cardinfo.get("prerekvizity", 0)
                    new_card = card.BiomCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['pruzkum'], pre)
                case 'O':
                    fury = cardinfo.get("besneni", 0)
                    extra = cardinfo.get("karty", 0)
                    new_card = card.MonsterCard(cardinfo['id'], cardinfo['jmeno'], cardinfo['barva'], cardinfo['uroven'], cardinfo['body'], fury, extra)
                case 'P':
                    new_card = card.EmployeeCard(cardinfo['id'], cardinfo['jmeno'],cardinfo["cena"])
                case 'TU':
                    new_card = card.ObjectiveCard(cardinfo['id'], cardinfo['jmeno'])
                case 'U':
                    new_card = card.EventCard(cardinfo['id'], cardinfo['jmeno'])
                case _:
                    print(cardinfo['typ'] + cardinfo['jmeno'])