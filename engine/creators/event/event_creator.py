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
ENEMY_PATH = 'engine/data/enemies/enemies.json'

# *****************
# *** VARIABLES ***
# *****************




# ***************
# *** CLASSES ***
# ***************

class EventCreator():
    def __init__(self, data, logic):
        self.data = data
        self.logic = logic

    def set_sprite(self, character):
        print(self.data[character]['symbol'])

    def get_export(self):
        file_path = "engine/data/event_test.json"

        data = {}

        data[f"{1}. {self.data['name']}"] = {"Data": self.data,
                                                 "Logic": self.logic}

        with open(file=file_path, mode="w") as file:
            json.dump(data, file, indent=4)

            print("Json file was created.\n")

# *****************
# *** FUNCTIONS ***
# *****************

def new_event():
    while True:
        print("Choose: Player/Enemy/Empty")
        choose = get_command("Which template for event you want to create?:\n")
        choose = choose.strip().upper()
        if choose in ("P", "PLAYER"):
            return choose
        else:
            print("Wrong choose.\n")

def print_dict(choose):
    while True:
        if choose in ("P", "PLAYER"):
            with open(PLAYER_PATH, "r") as f:
                players = json.load(f)
            print([player for player in players])
            character = get_command("Choose created character\n")
            if character in ([k for k in players.keys()]):
                return players[character]
            else:
                print("Wrong choose.\n")

def create_event(data):
    return EventCreator(data, empty_logic())

def empty_data():
    return {"name": None,
            "id": None,
            "priority": 1,
            "symbol": None,
            "y": 0,
            "x": 0
            }

def empty_logic():
    return {"movement": None,
            "pathfinding": None,
            "condition": None
            }

def data_import(path_load):
    with open(path_load, "r") as f:
        return json.load(f)

# ************
# *** MAIN ***
# ************

def main():
    # data = data_import(PLAYER_PATH)
    # player = EventCreator(data, '')

    # print([character for character in player.data])
    # character = get_command("Enter character.\n")
    # player.set_sprite(character)
    # player1 = EventCreator(empty_data(), empty_logic())

    # player1.data['name'] = 'One'

    # player1.get_export()

    choose = new_event()
    data = print_dict(choose)
    player = create_event(data)
    player.logic['movement'] = 'eight_move_direction'
    player.get_export()

if __name__ == '__main__':
    main()