from os import system
import json
import random
from engine.systems.commands import get_command
import engine.creators.map.tools as tools

with open("engine\data\players\players.json", "r", encoding="utf-8") as file:
    characters = json.load(file)

# GENERAL
running = True

# LAYER 1
game_map = []
y = 0
x = 0

# LAYER 2
player = characters['1. Monkey']['symbol']
player_y = -1
player_x = -1
player_vision = 45
enemy = {"symbol": "V",
         "ai_state": "PATROL",
         "vision": 35,
         "y": 0,
         "x": 0,
         "chase_turn": 0,
         "wait_turn": 0,
         "old_distance": float('-inf')
         }
wall = "X"
tool = ""
pointer = [{"pointer_y": 0},
           {"pointer_x": 0}]
entities_objects = {player, enemy["symbol"], wall}
entities = []

# |*****************|
# |****FUNCTIONS****|
# |*****************|

def map_position_xy(arg):
    while running:
        try:
            name = [k for k, v in globals().items() if v is arg][0]
            arg = get_command(f"Enter '{name}': ")
            arg = int(arg)
            if arg <= 0:
                print("Invalid number! Type only numbers larger than 0.")
            else:
                return arg
        except Exception:
            print("Invalid number! Type only whole numbers.")

def player_position_xy(arg, cor):
    while running:
        try:
            name = [k for k, v in globals().items() if v is arg][0]
            arg = int(input(f"Enter '{name}': "))
            if arg <= 0:
                print("Invalid number! Type only numbers larger than 0.")
            elif arg > cor:
                print(f"Invalid number! Max number you can type is: {cor}")
                arg = 0
            else:
                return arg
        except Exception:
            print("Invalid number! Type only whole numbers.")
            continue

# --- MAP ---
def game_size(layer, symbol):
    for i in range(0, y):
        layer.append([])
        for z in range(0, x):
            layer[0+i].append(symbol)

# --- PLAYER MOVEMENT ----
def player_movement(player_y, player_x, y_arg, x_arg):
    new_y = player_y + y_arg
    new_x = player_x + x_arg
    if new_y < 0 or new_y >= len_map_y or new_x < 0 or new_x >= len_map_x:
        print("You can't move!")
    elif entities[new_y][new_x] in entities_objects:
        print("You can't move!")
    else:
        entities[player_y][player_x] = ""
        player_y = player_y + y_arg
        player_x = player_x + x_arg
        entities[player_y][player_x] = player
    return player_y, player_x

# |**************|
# |***** AI *****|
# |**************|

# --- AI STATES ---
def ai_states(enemy, player_y, player_x):
    distance = abs(enemy['y'] - player_y) + abs(enemy['x'] - player_x)
    if distance > enemy['vision'] and enemy['chase_turn'] == 0 and enemy['wait_turn'] == 0:
        enemy['ai_state'] = "PATROL"
    elif distance <= enemy['vision'] and enemy['chase_turn'] == 0 and enemy['wait_turn'] == 0:
        enemy['ai_state'] = "CHASE"
    elif distance <= enemy['vision'] and enemy['wait_turn'] > 0 and enemy['chase_turn'] == 0:
        enemy['ai_state'] = "SEARCHING"
    elif distance > enemy['vision'] and enemy['wait_turn'] > 0 and enemy['chase_turn'] == 0:
        enemy['ai_state'] = "LOST"

    match enemy['ai_state']:
        case "PATROL":
            patrol_ai(enemy)
        case "CHASE":
            chase_ai(enemy, player_y, player_x)
        case "SEARCHING":
            searching_ai(enemy, distance)
        case "LOST":
            lost_ai(enemy)

# --- PATROL STATE ---
def patrol_ai(enemy):
    print('Patrol')
    entities[enemy['y']][enemy['x']] = ""
    new_y = enemy['y'] + random.randint(-1, 1)
    new_x = enemy['x'] + random.randint(-1, 1)
    if new_y <= -1:
        new_y = 0
    elif new_y >= len(game_map):
        new_y = len(game_map) - 1
        print('worked1')
    if new_x <= -1:
        new_x = 0
    elif new_x >= len(game_map):
        new_x = len(game_map[0]) - 1
        print('worked2')
    if entities[new_y][new_x] in entities_objects:
        new_y = enemy['y']
        new_x = enemy['x']
    enemy['y'] = new_y
    enemy['x'] = new_x
    entities[enemy['y']][enemy['x']] = enemy['symbol']

# --- CHASE STATE ---
def chase_ai(enemy, player_y, player_x):
    # CHASE START
    enemy['old_distance'] = float('-inf')
    if enemy['wait_turn'] == 0:
            enemy['chase_turn'] = 3
            enemy['wait_turn'] = 2
            print("start")
    # CHASE TURN
    if not enemy['chase_turn'] == 0:
        chase_ai_movement(enemy, player_y, player_x)
        enemy['chase_turn'] -= 1
        print("chase")

# CHASE MOVEMENT
def chase_ai_movement(enemy, player_y, player_x):
    start = (enemy['y'],enemy['x'])
    g_dict = {}
    came_from = {}
    found = False

    open_list = [start]
    g_dict[start] = 0
    goal = (player_y, player_x)
    def get_neighbors(node):
        y, x = node
        return [
            (y, x+1),
            (y+1, x),
            (y, x-1),
            (y-1, x)]

    # H DICT
    def heuristic(node):
        y, x = node
        return abs(y - goal[0]) + abs(x - goal[1])
    def is_walkable(node):
        y, x = node

        if y < 0 or y >= len_map_y or x < 0 or x >= len_map_x:
            return False
        
        if node == goal:
            return True
        
        if entities[y][x] in (entities_objects):
            return False
        
        return True
    
    # G DICT
    while open_list:
        current = min(open_list, key=lambda node: g_dict[node] + heuristic(node))
        if current == goal:
            found = True
            print(open_list)
            print(g_dict)
            print(f"FINDED: {current}")
            break
        print("current", current)
        print("goal", goal)
        neighbors = get_neighbors(current)
        
        for neighbor in neighbors:
            print("CHECK:", neighbor, is_walkable(neighbor))
            if neighbor == goal:
                print("GOAL IN NEIGHBORS")
            walkable_check = is_walkable(neighbor)
            if walkable_check == False:
                continue

            new_g = g_dict[current] + 1

            if neighbor not in g_dict or new_g < g_dict[neighbor]:
                g_dict[neighbor] = new_g
                came_from[neighbor] = current

                if neighbor not in open_list:
                    open_list.append(neighbor)
        
        open_list.remove(current)
    path = []
    node = goal
    if not found:
        print('Not found')
        return

    while node != start:
        path.append(node)
        node = came_from[node]

    path.append(start)
    path.reverse()

    print(path)

    if len(path) > 1:
        next_step = path[1]
        if next_step == (player_y, player_x):
            next_step = path[0]
        entities[enemy['y']][enemy['x']] = ''
        enemy['y'], enemy['x'] = next_step
        entities[enemy['y']][enemy['x']] = enemy['symbol']

# --- SEARCHING STATE ---
def searching_ai(enemy, distance):
    enemy['wait_turn'] -= 1
    if enemy['old_distance'] == float('-inf'):
        enemy['old_distance'] = distance
    print("searching")
    print(enemy['old_distance'])
    print(distance)
    # CONTINUE CHASE
    if distance < enemy['old_distance']:
        enemy['ai_state'] = "CHASE"
        enemy['chase_turn'] = 3
        enemy['wait_turn'] = 2
        enemy['old_distance'] = float('-inf')
        print("start new")

# --- LOST STATE ---
def lost_ai(enemy):
    enemy['wait_turn'] = 0
    enemy['old_distance'] = float('-inf')
    print('lost')

#|************|
#|*** MAIN ***|
#|************|
if __name__ == '__main__':
    system("clear||cls")
    # --- LAYER 1 ---
    y = map_position_xy(y)
    x = map_position_xy(x)

    game_size(game_map, '·')
    game_size(entities, "")

    len_map_y = len(game_map)
    len_map_x = len(game_map[0])

    # --- LAYER 2 ---

    # WALLS
    while running:
        system("clear||cls")
        print(y)
        print(x)
        if not tool in ("", "POINTER", "LINER", "SQUARE"):
            print("Wrong Tool. You can choose only: Pointer, Liner, Square.")
            tool = ""
        start_y = max(0, player_y-player_vision)
        end_y = min(len_map_y, player_y+player_vision+1)
        start_x = max(0, player_x-player_vision)
        end_x = min(len_map_x, player_x+player_vision+1)
        for map_y in range(start_y, end_y):
            for map_x in range(start_x, end_x):
                if entities[map_y][map_x] != "":
                    print(entities[map_y][map_x], end=" ")
                else:
                    print(game_map[map_y][map_x], end=" ")
            print()
        if tool == "":
            tool = get_command("Choose tool (Pointer, Liner, Square): ")
            tool = str(tool).upper()
        match tool:
            case tools.pointer.name:
                tools.pointer.y = tools.pointer.get_position('y', y)
                tools.pointer.x = tools.pointer.get_position('x', x)
                tools.pointer.place(entities, wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break
            case tools.liner.name:
                tools.liner.f_y = tools.liner.get_position('first y', y)
                tools.liner.f_x = tools.liner.get_position('first x', x)

                tools.liner.s_y = tools.liner.get_position('second y', y)
                tools.liner.s_x = tools.liner.get_position('second x', x)
                tools.liner.place(entities, wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break
            case tools.square.name:
                tools.square.f_y = tools.square.get_position('first y', y)
                tools.square.f_x = tools.square.get_position('first x', x)

                tools.square.s_y = tools.square.get_position('second y', y)
                tools.square.s_x = tools.square.get_position('second x', x)
                tools.square.place(entities, wall)
                con = get_command("Continue creating? (Yes/No): ")
                con = str(con).upper()
                match con:
                    case 'Y' | 'YES':
                        pass
                    case 'N' | 'NO':
                        break

    # --- PLAYER POSITION ---
    while running:
        system("clear||cls")
        start_y = max(0, player_y-player_vision)
        end_y = min(len_map_y, player_y+player_vision+1)
        start_x = max(0, player_x-player_vision)
        end_x = min(len_map_x, player_x+player_vision+1)
        for map_y in range(start_y, end_y):
            for map_x in range(start_x, end_x):
                if entities[map_y][map_x] != "":
                    print(entities[map_y][map_x], end=" ")
                else:
                    print(game_map[map_y][map_x], end=" ")
            print()
        player_y = player_position_xy(player_y, y)
        player_x = player_position_xy(player_x, x)
        print(entities)
        input("")
        player_y -= 1
        player_x -= 1
        if entities[player_y][player_x] in entities_objects:
            print("You can't place player here! There is an object already in this position.")
        else:
            break
    
    entities[player_y][player_x] = player
    entities[enemy['y']][enemy['x']] = enemy['symbol']

    new_y = player_y
    new_x = player_x

    visible = set()

    def bresenham(y1, x1, y2, x2):
        points = []

        dy = abs(y1 - y2)
        dx = abs(x1 - x2)

        sy = 1 if y1 < y2 else -1
        sx = 1 if x1 < x2 else -1

        err = dx - dy

        while True:
            points.append((y1, x1))


            if y1 == y2 and x1 == x2:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x1 += sx

            if e2 < dx:
                err += dx
                y1 += sy

        return points

    def is_visible(y1, x1, y2, x2):
        line = bresenham(y1, x1, y2, x2)
        for (y, x) in line:
            if (y, x) == (y1, x1):
                continue
            if y < 0 or y >= len_map_y or x < 0 or x >= len_map_x:
                return False
            if entities[y][x] == wall:
                return (y, x) == (y2, x2) # Z False działa również ale zostaw z celem

        return True
    # SYSTEM
    while running:
        # # GAME MAP
        start_y = max(0, player_y-player_vision)
        end_y = min(len_map_y, player_y+player_vision+1)
        start_x = max(0, player_x-player_vision)
        end_x = min(len_map_x, player_x+player_vision+1)
        # for y in range(start_y, end_y):
        #     for x in range(start_x, end_x):
        #         if entities[y][x] != "":
        #             print(entities[y][x], end=" ")
        #         else:
        #             print(game_map[y][x], end=" ")
        #     print()
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                if is_visible(player_y, player_x, y, x):
                    if entities[y][x] != "":
                        print(entities[y][x], end=" ")
                    else:
                        print(game_map[y][x], end=" ")
                else:
                    print(" ", end=" ")
            print()
        
        # COMMANDS
        command = input("").lower()
        system("clear||cls")
        match command:
            case 'w':
                player_y, player_x = player_movement(player_y, player_x, y_arg=-1, x_arg=0)
            case 's':
                player_y, player_x = player_movement(player_y, player_x, y_arg=1, x_arg=0)
            case 'a':
                player_y, player_x = player_movement(player_y, player_x, y_arg=0, x_arg=-1)
            case 'd':
                player_y, player_x = player_movement(player_y, player_x, y_arg=0, x_arg=1)
            case 'wd' | 'dw':
                player_y, player_x = player_movement(player_y, player_x, y_arg=-1, x_arg=1)
            case 'wa' | 'aw':
                player_y, player_x = player_movement(player_y, player_x, y_arg=-1, x_arg=-1)
            case 'sd' | 'ds':
                player_y, player_x = player_movement(player_y, player_x, y_arg=1, x_arg=1)
            case 'sa' | 'as':
                player_y, player_x = player_movement(player_y, player_x, y_arg=1, x_arg=-1)
            case 'stop':
                break
        
        # --- ENEMY STATE ---
        ai_states(enemy, player_y, player_x)