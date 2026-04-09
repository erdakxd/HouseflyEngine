import os
import json
from ...systems.commands import get_command
from engine.core.exceptions import NoJsonFile
import engine.utils.terminal as terminal

PLAYERS_PATH = "engine/data/players/players.json"
ENEMIES_PATH = "engine/data/enemies/enemies.json"

# ***************
# *** CLASSES ***
# ***************

class CharacterEdit():
    def __init__(self, data):
        self.data = data

# *****************
# *** FUNCTIONS ***
# *****************

def load_map(path_load):
    if not os.path.exists(path_load):
        raise NoJsonFile()
    
    with open(path_load, "r") as f:
        return json.load(f)
    
def set_edit(character_dict):
    while True:
        character_list = []
        for key in character_dict.keys():
            print(f"{key}")
            character_list.append(key)
        
        name = get_command("Enter number or name of character you want to edit:\n")
        try:
            name = int(name)
            if name in character_list:
                return name
            else:
                print("Wrong 'number' or 'name'.")
        except ValueError:
            name = str(name)
            if name in character_list:
                return name
            else:
                print("Wrong 'number' or 'name'.")

def character_dict(character_dict, character_id):
    character = {}
    for key, value in character_dict.items():
        character[key] = value
    return character

def character_edit(character, dictionary):
    while True:
        for key, value in dictionary[character].items():
            print(f"{key}: {value}")
        print()

        print(f"Choose: {[k for k in dictionary[character].keys()]}/Save")
        choose = get_command("Enter key you want to edit:\n")
        choose = choose.strip().lower()
        if choose in dictionary[character].keys():
            return choose
        elif choose == 's' or choose == 'save':
            return choose
        else:
            print("Wrong choose.\n")
        
def edit(choose, character, dictionary):
    while True:
        edit_choose = get_command(f"Enter {choose}:\n")
        try:
            if type(dictionary[character][choose]) == type(1):
                edit_choose = int(edit_choose)
                if edit_choose < 0:
                    print("Invalide number. You can type only whole numbers and at least 0.\n")
                    continue
            return edit_choose
        except ValueError:
            print("Invalide number. You can type only whole numbers and at least 0.\n")

def save(dictionary, character, file_path):
    while True:
        print("Choose: Yes/No")
        choose = get_command("Do you want to save character? It will change Json file.:\n")
        choose = choose.strip().upper()
        match choose:
            case 'Y' | 'YES':
                try:
                    n = character.split('.')[0]
                    value = dictionary[character]
                    new_key = f"{n}. {value['name']}"

                    dictionary[new_key] = dictionary.pop(character)
                    data = dict(sorted(dictionary.items()))
                    print(data)
                    with open(file=file_path, mode="w") as file:
                        json.dump(data, file, indent=4)

                        print("Json file was created.\n")
                    return True
                except Exception:
                    print("Something went wrong.\n")
                return False
            case 'N' | 'NO':
                return False
            case _:
                print("Wrong choose.\n")

def main():
    players = load_map(PLAYERS_PATH)
    enemies = load_map(ENEMIES_PATH)

    while True:
        repeat = True
        character = set_edit(players)
        
        while repeat:
            choose = character_edit(character, players)
            if choose == 's' or choose == 'save':
                repeat = save(players, character, PLAYERS_PATH)
                continue
            edit_choose = edit(choose, character, players)

            players[character][choose] = edit_choose




if __name__ == '__main__':
    main()