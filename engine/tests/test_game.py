import json
import os
import subprocess
import engine.systems
from engine.systems.commands import get_command

GAME_MAP = "engine\data\map\game_map.json"

def load_map(path):
    with open(path, "r") as f:
        return json.load(f)

def main():
    game_map = load_map(GAME_MAP)
    for layer in game_map:
        print(layer)

if __name__ == '__main__':
    main()