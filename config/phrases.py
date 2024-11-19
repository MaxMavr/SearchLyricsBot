import json
from config.const import PHRASES_FILE

with open(PHRASES_FILE, 'r', encoding="utf-8") as file:
    phrases: dict = json.load(file)
