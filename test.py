import functions.functions as f
import pandas as pd
import json
import random 
import params as p
import functions as u
import pygame
import sys
import classes.ux.Button as button
import classes.ux.TextBox as textbox
import classes.logic.Card as card

deck = f.load_seasons()
s = random.sample(deck, 1)[0]
deck.remove(s)
print(s, deck)