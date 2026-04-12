import json
import os
import shutil
from ...systems.commands import get_command
import engine.utils.terminal as terminal

# ***************
# *** CLASSES ***
# ***************
class Char:
    id_counter = 0

    def __init__(self):
        Char.id_counter += 1
        self.id = Char.id_counter

    def to_dict(self):
        return {
            'name': self.name,
            'id': self.id,
            'priority': self.priority,
            'y': self.y,
            'x': self.x,
            'symbol': self.symbol,
            'vision': self.vision
        }

class Player(Char):
    characters= {}

    def __init__(self, name, symbol, vision):
        super().__init__()

        self.name = name
        self.priority = 1
        self.y = 0
        self.x = 0
        self.symbol = symbol
        self.vision = vision

        Player.characters[self.name] = self
    
    @classmethod
    def reset(cls):
        cls.players.clear()
        

class Enemy(Char):
    characters = {}

    def __init__(self, name, symbol, vision):
        super().__init__()

        self.name = name
        self.priority = 1
        self.y = 0
        self.x = 0
        self.symbol = symbol
        self.vision = vision
        self.chase_turn = 0
        self.wait_turn = 0
        self.old_distance = None # float('-inf')

        Enemy.characters[self.name] = self

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'chase_turn': self.chase_turn,
            'wait_turn': self.wait_turn,
            'old_distance': self.old_distance
        })
        return data
    
    @classmethod
    def reset(cls):
        cls.enemies.clear()

# *****************
# *** FUNCTIONS ***
# *****************
def my_import(name):
    components = name #.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def get_single_character(character):
    print(f"Name: {character.name}")
    print(f"ID: {character.id}")
    print(f"y: {character.y}")
    print(f"x: {character.x}")
    print(f"symbol: {character.symbol}")
    print(f"vision: {character.vision}")
    print() 

def get_character_dict(dict_char):
    for value in dict_char.values():
        print(f"Name: {value.name}")
        print(f"ID: {value.id}")
        print(f"y: {value.y}")
        print(f"x: {value.x}")
        print(f"symbol: {value.symbol}")
        print(f"vision: {value.vision}")
        print()

def get_character():
    while True:
        print(f'Choose: Player/Enemy')
        choose = get_command("Enter a character you want to create:\n")
        print()
        choose = choose.strip().upper()
        if choose in ('P', 'PLAYER', 'E', 'ENEMY'):
            return choose
        else:
            print(f"'{choose}' is not correct choose. Please choose player or enemy.")
            print()
    
def get_name(character):
    name = get_command(f'Enter name for {character}:\n')
    name = str(name)
    return name
    
def get_vision(character):
    while True:
        print('Choose: Default/NUMBER BIGGER THAN 0')
        vision = get_command(f'Enter a number for {character} vision (Default is 7):\n')
        try:
            vision = str(vision).strip().upper()
            if vision in ('D', 'DEFAULT'):
                vision = 7
                return vision
            else:
                vision = int(vision)
                if vision > 0:
                    return vision
                if vision < 0:
                    print(f"'{vision}' is not correct number. Please type number bigger than 0.\n")
        except ValueError:
            print(f"Incorrect number. You can type only whole numbers bigger than 0.\n")

def get_symbol(character):
    symbol = get_command(f'Enter symbol for {character}:\n')
    print()
    return symbol
    
def get_create_another(character, dict_char):
    while True:
        print("INFO: CHOOSE TO CREATE FOLDER AND NAME IT 'players' or 'enemies'.\n")

        print("Choose: Yes/No/Delete/Clear")
        another = get_command(f"Do you want to create another {character}?:\n")
        another = another.strip().upper()
        print()
        match another:
            case 'Y' | 'YES':
                repeat = True

                return repeat
            case 'N' | 'NO':
                if not bool(dict_char):
                    print(f"You don't have any characters! You need at least one {character} to export.")
                    print()
                else:
                    print("Current list of characters: ")
                    get_character_dict(dict_char)
                    repeat = False

                    return repeat
            case 'D' | 'DELETE':
                if not bool(dict_char):
                    print(f"You don't have any characters! You need at least one {character} to delete.")
                    print()
                else:
                    while True:
                        try:
                            delete = get_command("Which player would you like to delete?:\n")
                            print()
                            dict_char.pop(delete)

                            break
                        except KeyError:
                            print(f"This {character} doesn't exists. please type {character} name from this list: ")
                            get_character_dict(dict_char)

            case 'C' | 'CLEAR':
                if not bool(dict_char):
                    print(f"You don't have any characters! You need at least one {character} to clear.")
                    print()
                else:
                    while True:
                        print("Choose: Yes/No")
                        choose = get_command("Do you want to clear whole list?:\n")
                        print()
                        choose = choose.strip().upper()
                        match choose:
                            case 'Y' | 'YES':
                                dict_char.clear()
                                break
                            case 'N' | 'NO':
                                break
                            case _:
                                print(f"'{choose}' is not correct choose. Please choose yes or no.")
                                print()
            case _:
                print(f"'{another}' is not correct choose. Please choose yes or no.")
                print()

def get_repeat():
    while True:
        print("Choose: Yes/No")
        choose = get_command("Do you want to change character creator?:\n")
        choose = choose.upper()
        print()
        match choose:
            case 'Y' | 'YES':
                repeat = True
                return repeat
            case 'N' | 'NO':
                repeat = False
                return repeat
            case _:
                print(f"'{choose}' is not correct choose. Please choose yes or no.\n")

def get_export(file_name, char_dict):
    while True:
        print("Choose: Yes/No")
        folder = get_command("Do you want to create folder in data?:\n")
        folder = folder.strip().upper()
        match folder:
            case 'Y' | 'YES':
                while True:
                    folder_name = get_command("\nHow would you like to name it?:\n")
                    f"engine/data/{folder_name}"
                    directory_path =  f"engine/data/{folder_name}"
                    try:
                        os.mkdir(directory_path)
                        print(f"\nFolder {folder_name} was created.\n")
                        break
                    except FileExistsError:
                        shutil.rmtree(directory_path)
                        os.mkdir(directory_path)
                        break
                    except Exception:
                        print("Something went wrong. Check if you type proper symbols for folder.\n")
                break
            case 'N' | 'NO':
                folder_name = None
                break
            case _:
                print("Wrong answer. Please write: Yes or No.\n")

    if folder_name:
        file_path = f"engine/data/{folder_name}/{file_name}.json"
    else:
        file_path = f"engine/data/{file_name}.json"

    try:
        data = {}

        for i, (name, character) in enumerate(char_dict.items(), start=1):
            data[f"{i}. {name}"] = character.to_dict()

        with open(file=file_path, mode="w") as file:
            json.dump(data, file, indent=4)

            terminal.clear()
            print("Json file was created.\n")

    except Exception:
        terminal.clear()
        print("Something went wrong.\n")

# ************
# *** MAIN ***
# ************  
def main():
    Player.reset()
    Enemy.reset()
    os.system('clear||cls')
    repeat = True

    print("INFO: YOU CAN TYPE FIRST LETTER FROM OPTIONS AS A SHORTCUT.\nDOESN'T MATTER IF IS IT LOWER OR UPPER CASE.")
    print()

    test = my_import(Player)
    print(test)
    # ****************
    # *** CREATORS ***
    # ****************
    while repeat:
        character = get_character()

        # --- PLAYER CREATOR ---
        while character in ('P', 'PLAYER') and repeat:
            name = get_name('player')
            vision = get_vision('player')
            symbol = get_symbol('player')

            player = Player(name, symbol, vision)
            get_single_character(player)

            repeat = get_create_another('player', Player.players)


        # --- ENEMY CREATOR ---
        while character in ('E', 'ENEMY') and repeat:
            name = get_name('enemy')
            vision = get_vision('enemy')
            symbol = get_symbol('enemy')

            player = Enemy(name, symbol, vision)
            get_single_character(player)

            repeat = get_create_another('enemy', Enemy.enemies)

        repeat = get_repeat()

    # *****************
    # *** EXPORTING ***
    # *****************
    while True:
        print("Choose: Yes/No")
        folder = get_command("Do you want to create folder in data?:\n")
        folder = folder.strip().upper()
        print()
        match folder:
            case 'Y' | 'YES':
                while True:
                    folder_name = get_command("How would you like to name it?:\n")
                    f"engine/data/{folder_name}"
                    directory_path =  f"engine/data/{folder_name}"
                    print()
                    try:
                        os.mkdir(directory_path)
                        print(f"Folder {folder_name} was created.")
                        print()
                        break
                    except FileExistsError:
                        print("You can't create folder with that is already exists.")
                        print()
                    except Exception:
                        print("Something went wrong. Check if you type proper symbols for folder.")
                        print()
                break
            case 'N' | 'NO':
                folder_name = None
                break
            case _:
                print("Wrong answer. Please write: Yes or No.\n")

    # --- PLAYERS EXPORT ---
    if Player.players:
        get_export(folder_name, 'players', Player.players)

    # --- ENEMIES EXPORT ---
    if Enemy.enemies:
        get_export(folder_name, 'enemies', Enemy.enemies)

    return 0

if __name__ == '__main__':
    main()