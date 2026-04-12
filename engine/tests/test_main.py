import json
import os
import subprocess
import engine.systems
from engine.systems.commands import get_command

GAME_MAP = "engine\data\map\game_map.json"

LAYERS = []
RENDER = []

def load_map(path):
    with open(path, "r") as f:
        return json.load(f)

# ************
# *** MAIN ***
# ************

def main():
    
    # --- PUTTING JSON MAP TO LAYERS LIST ---
    game_map = load_map(GAME_MAP)
    z = 0

    for layer, value in game_map.items():
        y = 0

        LAYERS.append([])
        for column in value:
            LAYERS[z].append([])
            for row in column:
                if row == '0':
                    LAYERS[z][y].append('0')
                else:
                    LAYERS[z][y].append(row)
            y += 1
        z += 1

    z = 0
    # --- MIXING ALL LAYERS ---
    for layer in LAYERS:
        y = 0

        for column in layer:
            x = 0
            RENDER.append([])

            for row in column:
                if x == len(RENDER[y]):
                    RENDER[y].append(row)
                else:
                    if LAYERS[z][y][x] == '0' and RENDER[y][x] != '0':
                        x += 1
                        continue
                    else:
                        RENDER[y][x] = row

                x += 1
            y += 1
        z += 1

    
    # --- RENDERING MAP ---
    for y in RENDER:
        for x in y:
            print(x, end=' ')
        print()
    

if __name__ == '__main__':
    main()