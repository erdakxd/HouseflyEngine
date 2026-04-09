import json
import os
import shutil
from ...systems.commands import get_command
import engine.utils.terminal as terminal

class GameMap:
    def __init__(self):
        self.y = 0
        self.x = 0
        GameMap.game_map = self

    def to_dict(self):
        return {
            
        }

def game_size(symbol):
    for layer in GameMap.game_map:
        print(layer)
        GameMap.game_map[layer] = [
            [symbol for x in range(GameMap.x)]
            for y in range(GameMap.y)
            ]

def get_layer():
    while True:
        try:
            layers = get_command("How many layers you want to add?:\n")
            layers = int(layers)
            if layers > 0:
                for n in range(0, layers):
                    GameMap.game_map[n+1] = None
                return
            elif layers <= 0:
                print("Invalid number! Type only numbers larger than 0.\n")
        except ValueError:
            print("Invalid number! Type only whole numbers.\n")

# --- EXPORT ---
def get_export(file_name, data):
    print("INFO: CHOOSE TO CREATE FOLDER AND NAME IT 'map'.\n")

    print("Choose: Yes/No")
    folder = get_command("Do you want to create folder in data?:\n")
    folder = folder.strip().upper()
    match folder:
        case 'Y' | 'YES':
            while True:
                folder_name = get_command("How would you like to name it?:\n")
                directory_path =  f"engine/data/{folder_name}"
                try:
                    os.mkdir(directory_path)
                    print(f"Folder {folder_name} was created.")
                    print()
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
        case _:
            print("Wrong answer. Please write: Yes or No.\n")

    if folder_name:
        file_path = f"engine/data/{folder_name}/{file_name}.json"
    else:
        file_path = f"engine/data/{file_name}.json"

    # try:

    with open(file=file_path, mode="w") as file:
        json.dump(data, file, indent=4)

        terminal.clear()
        print("Json file was created.\n")
    return

def map_position_xy(name):
    while True:
        try:
            arg = get_command(f"Enter '{name}': ")
            arg = int(arg)
            if arg <= 0:
                print("Invalid number! Type only numbers larger than 0.")
            else:
                return arg
        except Exception:
            print("Invalid number! Type only whole numbers.")

def render_map():
    try:
        len_map_y = len(GameMap.game_map[1])
        len_map_x = len(GameMap.game_map[1][0])

        for map_y in range(0, len_map_y):
            for map_x in range(0, len_map_x):
                print(GameMap.game_map[1][map_y][map_x], end=" ")
            print()
    except Exception:
        print("Set layers and size.\n")

#|************|
#|*** MAIN ***|
#|************|
def main():
    repeat = True
    tool = ""
    os.system("clear||cls")

    # --- LAYER 1 ---
    game_map = GameMap()

    game_map.get_layer()
    game_map.y = game_map.map_position_xy('y')
    game_map.x = game_map.map_position_xy('x')

    game_map.game_size('0')

    len_map_y = len(game_map.game_map[1])
    len_map_x = len(game_map.game_map[1][0])

    for map_y in range(0, len_map_y):
        for map_x in range(0, len_map_x):
            print(game_map.game_map[1][map_y][map_x], end=" ")
        print()

    # *****************
    # *** EXPORTING ***
    # *****************
    while True:
        print("INFO: CHOOSE TO CREATE FOLDER AND NAME IT 'map'.\n")

        print("Choose: Yes/No")
        folder = get_command("Do you want to create folder in data?:\n")
        folder = folder.strip().upper()
        print()
        match folder:
            case 'Y' | 'YES':
                while True:
                    folder_name = get_command("How would you like to name it?:\n")
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
                print("Wrong answer. Please write: Yes or No.")
                print()
    game_map.get_export(folder_name, 'layers')
        

if __name__ == '__main__':
    main()