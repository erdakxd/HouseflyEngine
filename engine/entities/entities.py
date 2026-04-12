import json
import os
import engine.utils.terminal as terminal
from engine.systems.commands import get_command

# *****************
# *** VARIABLES ***
# *****************

GAME_MAP = "engine/data/map/game_map.json"
EVENTS = "engine/data/event_test.json"
ENTITIES = []

# *****************
# *** FUNCTIONS ***
# *****************

def load(json_file):
    with open(json_file, "r") as f:
        return json.load(f)
    
def entities_size(game_map):
    len_y = len(game_map['1'])
    len_x = len(game_map['1'][0])

    for column in range(0, len_y):
        ENTITIES.append([])
        for row in range(0, len_x):
            ENTITIES[column].append(0)

def render_entities(events):
    priority = get_command("Enter priority for entities.\n")
    priority = int(priority)

    for y in ENTITIES:
        for x in y:
            if events != None:
                if x in [events.keys()]:
                    print('WORKS')
                    for event in x:
                        n = 0
                        if event['Data']['priority'] == priority:
                            n += 1
                            print(events['Data']['symbol'])
                    if n == 0:
                        print(0, end=" ")
                else:
                    print(x, end=" ")
            else:
                print(x, end=" ")
        print()
    
def choose_event(events):
    while True:
        print([event for event in events])
        choose = get_command("Enter event:\n")
        if choose in (events):
            return events[choose]
        else:
            print("Wrong choose:\n")

def insert_event(event, game_map):
    len_y = len(game_map['1'])
    len_x = len(game_map['1'][0])

    while True:
        print("Enter: y, x")
        choose = get_command("Where you want to insert event?\n")
        try:
            choose = tuple(map(int, choose.split(",")))
            if choose[0] < 0 or choose[1] < 0 or choose[0] >= len_y or choose[1] >= len_x:
                print("Invalid number. You can only type whole numbers equals or bigger than 0.")
                print(f"Also for 'y' smaller than {len_y} and for 'x' smaller than {len_x}.\n")
            else:
                if ENTITIES[choose[0]][choose[1]] == 0:
                    ENTITIES[choose[0]][choose[1]] = [event]
                else:
                    ENTITIES[choose[0]][choose[1]].append(event)
                return
        except ValueError:
            print("Invalid number. You can only type whole numbers equals or bigger than 0.")
            print(f"Also for 'y' smaller than {len_y} and for 'x' smaller than {len_x}.\n")
        except IndexError:
            print("Invalid number. You can only type whole numbers equals or bigger than 0.")
            print(f"Also for 'y' smaller than {len_y} and for 'x' smaller than {len_x}.\n")

def delete_event():
    print("Enter: y, x")
    choose = get_command("Which event you want to delete?\n")

def export():
    file_path = "engine/data/entities/entities.json"

    data = ENTITIES

    with open(file=file_path, mode="w") as file:
        json.dump(data, file, indent=4)

        print("Json file was created.\n")

# ************
# *** MAIN ***
# ************

def main():
    game_map = load(GAME_MAP)
    events = load(EVENTS)
    event = None

    entities_size(game_map)
    render_entities(event)
    event = choose_event(events)

    counter = 0
    while True: 
        render_entities(event)
        insert_event(event, game_map)
        counter +=1
        if counter == 3:
            break
        
    export()



if __name__ == '__main__':
    main()
