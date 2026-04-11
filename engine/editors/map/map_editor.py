import os
import json
from ...systems.commands import get_command
from engine.core.exceptions import NoJsonFile
from ...creators.map import tools
import engine.utils.terminal as terminal

MAP_PATH = "engine/data/map/game_map.json"
EVENT_PATH = "engine/data/event_test.json"

def load_map():
    if not os.path.exists(MAP_PATH):
        raise NoJsonFile()
    
    with open(MAP_PATH, "r") as f:
        return json.load(f)

def load_event():
    if not os.path.exists(EVENT_PATH):
        raise NoJsonFile()
    
    with open(EVENT_PATH, "r") as f:
        return json.load(f)
    
class Structures:
    def __init__(self):
        pass
    
repeat = True
layer = '1'
tool = "POINTER"

wall = "X"
floor = "•"
textures = (wall, floor)
texture = "•"

# len_map_y = len(game_map['1'])
# len_map_x = len(game_map['1'][0])

# def set_layer():    
#     while True:
#         print(f"Choose: {game_map.keys()}")
#         layer = get_command("Which layer you want to edit?:\n")
#         try:
#             for k in game_map.keys():
#                 if layer == k:
#                     return layer
#                 elif layer > max(game_map.keys()) or layer < min(game_map.keys()):
#                     print(f"Invalid number! You can choose only these layers: {game_map.keys()}.\n")
#                     break
#         except Exception:
#             print("Invalid number! Type only whole numbers.\n")
#             terminal.clear()

def set_texture():
    while True:
        n = 0
        print(f"List of textures:\n")
        for t in textures:
            n += 1
            print(f"{n}. {t}")

        try:
            print(f"\nChoose: from 1 to {len(textures)}")
            texture = get_command("Which texture you choose?:\n")
            texture = int(texture)
            if texture in (1, 2):
                texture = textures[texture-1]
                return texture
            else:
                print(f"'{texture}' is a incorrect texture. You can choose from 1 to {len(textures)}")

        except Exception:
            print(f"Invalid texture. You can choose from 1 to {len(textures)}")
            terminal.clear()

def set_tool():
    pass

def edit_map():
    pass 

def put_event(event, len_map_y, len_map_x, game_map):
    while True:
        print([e for e in event])
        choose = get_command("Choose event.\n")
        if choose in event:
            choose = event[choose]
            terminal.clear()

            for map_y in range(0, len_map_y):
                for map_x in range(0, len_map_x):
                    print(game_map[layer][map_y][map_x], end=" ")
                print()

            print([c for c in choose])
            tools.pointer.y = tools.pointer.get_position('y', len_map_y)
            tools.pointer.x = tools.pointer.get_position('x', len_map_x)
            tools.pointer.place(game_map[layer], choose['Data']['symbol'])

        return

def get_export():
    pass

# ************
# *** MAIN ***
# ************

def main():
    game_map = load_map()
    event = load_event()
    repeat = True
    layer = '2'
    tool = "POINTER"

    wall = "X"
    floor = "•"
    textures = (wall, floor)
    texture = "•"

    len_map_y = len(game_map['1'])
    len_map_x = len(game_map['1'][0])
    terminal.clear()

    def set_texutre():
        while True:
            n = 0
            print(f"List of textures:\n")
            for t in textures:
                n += 1
                print(f"{n}. {t}")

            try:
                print(f"\nChoose: from 1 to {len(textures)}")
                texture = get_command("Which texture you choose?:\n")
                texture = int(texture)
                if texture in (1, 2):
                    texture = textures[texture-1]
                    return texture
                else:
                    print(f"'{texture}' is a incorrect texture. You can choose from 1 to {len(textures)}")

            except Exception:
                print(f"Invalid texture. You can choose from 1 to {len(textures)}")
                terminal.clear()

    def set_tool():
        pass

    def edit_map():
        pass 

    def get_export():
        pass

    # --- EDITING LAYER ---
    while True:
        terminal.clear()
        if not tool in ("", "POINTER", "LINER", "SQUARE"):
            print("Wrong Tool. You can choose only: Pointer, Liner, Square.\n")
            tool = ""

        for map_y in range(0, len_map_y):
            for map_x in range(0, len_map_x):
                print(game_map[layer][map_y][map_x], end=" ")
            print()

        if tool == "":
            tool = get_command("Choose tool (Pointer, Liner, Square): ")
            tool = str(tool).strip().upper()
        match tool:
            case tools.pointer.name:
                tools.pointer.y = tools.pointer.get_position('y', len_map_y)
                tools.pointer.x = tools.pointer.get_position('x', len_map_x)
                tools.pointer.place(game_map[layer], wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break
            case tools.liner.name:
                tools.liner.f_y = tools.liner.get_position('first y', len_map_y)
                tools.liner.f_x = tools.liner.get_position('first x', len_map_x)

                tools.liner.s_y = tools.liner.get_position('second y', len_map_y)
                tools.liner.s_x = tools.liner.get_position('second x', len_map_x)
                tools.liner.place(game_map[layer], wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break
            case tools.square.name:
                tools.square.f_y = tools.square.get_position('first y', len_map_y)
                tools.square.f_x = tools.square.get_position('first x', len_map_x)

                tools.square.s_y = tools.square.get_position('second y', len_map_y)
                tools.square.s_x = tools.square.get_position('second x', len_map_x)
                tools.square.place(game_map[layer], wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break

    put_event(event, len_map_y, len_map_x, game_map)

    # *****************
    # *** EXPORTING ***
    # *****************
    file_path = "engine\data\map\game_map.json"
    data = game_map

    with open(file=file_path, mode="w") as file:
        json.dump(data, file, indent=4)

        print("\nJson file was created.\n")

if __name__ == '__main__':
    main()