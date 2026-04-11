import json
import os
import subprocess
import engine.systems
from engine.systems.commands import get_command

GAME_MAP = "engine\data\map\game_map.json"

RENDER = []

def load_map(path):
    with open(path, "r") as f:
        return json.load(f)

# ************
# *** MAIN ***
# ************

def main():
    game_map = load_map(GAME_MAP)
    z = 0

    for layer, value in game_map.items():
        y = 0

        RENDER.append([])
        for row in value:
            RENDER[z].append([])
            for column in row:
                if column == '0':
                    RENDER[z][y].append('O')
                else:
                    RENDER[z][y].append(column)
            y += 1
        z += 1
        
    
    for z in RENDER:
        for y in z:
            for x in y:
                print(x, end=' ')
            print()
        print()
    

if __name__ == '__main__':
    main()