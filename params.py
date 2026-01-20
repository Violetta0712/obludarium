from pathlib import Path
import sys
img_format = ".jpg"

BASE_DIR = Path(__file__).parent
ASSETS_DIR = BASE_DIR / "assets"
JSON_DIR = ASSETS_DIR / "json"
IMG_DIR = ASSETS_DIR / "img" /"cards"

DK_json = JSON_DIR / "DK_cards.json"
HO_json = JSON_DIR / "HO_cards.json"
JO_json = JSON_DIR / "JO_cards.json"
K_json = JSON_DIR / "K_cards.json"
P_json = JSON_DIR / "P_cards.json"
PO_json = JSON_DIR / "PO_cards.json"
S_json = JSON_DIR / "S_cards.json"
SO_json = JSON_DIR / "SO_cards.json"
TO_json = JSON_DIR / "TO_cards.json"
TU_json = JSON_DIR / "TU_cards.json"
U_json = JSON_DIR / "U_cards.json"
ZO_json = JSON_DIR / "ZO_cards.json"

deck_jsons = [HO_json, JO_json, K_json, P_json, PO_json, SO_json,TO_json, TU_json, U_json, ZO_json]
all_jsons = deck_jsons + [DK_json, S_json]
season_jsons = [S_json]
DK_jsons = [DK_json]
hand_size = 8

