# KLASA EVENT -> PUSTY
# JSON -> DANE I TRIGERY
# PYTHON -> LOGIKA
# 
# Aktualny kreator:
# - Sprite
# - Możliwość wklejenia logiki
# - Łączenie Danych z Json
#
import json
import os
from ...systems.commands import get_command
import engine.utils.terminal as terminal

PLAYER_PATH = 'engine/data/players/players.json'

class EventCreator():
    def __init__(self, data, logic):
        self.data = data
        self.logic = logic

    def set_sprite(self, character):
        print(self.data[character]['symbol'])

    def movement(self):
        pass

def export(path_load):
    with open(path_load, "r") as f:
        return json.load(f)

def main():
    data = export(PLAYER_PATH)
    player = EventCreator(data, '')

    print([character for character in player.data])
    character = get_command("Enter character.\n")
    player.set_sprite(character)

if __name__ == '__main__':
    main()