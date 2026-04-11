def eight_move_direction(arg):
    MOVE_MAP = {
        "W": (-1, 0),
        "S": (1, 0),
        "A": (0, -1),
        "D": (0, 1)
    }

    dy = 0
    dx = 0

    for key in MOVE_MAP.keys():
        if arg == MOVE_MAP[key]:
            my, mx = MOVE_MAP[key]
            
            dy += my
            dx += mx

    


# def player_movement(player_y, player_x, y_arg, x_arg):
#     new_y = player_y + y_arg
#     new_x = player_x + x_arg
#     if new_y < 0 or new_y >= len_map_y or new_x < 0 or new_x >= len_map_x:
#         print("You can't move!")
#     elif entities[new_y][new_x] in entities_objects:
#         print("You can't move!")
#     else:
#         entities[player_y][player_x] = ""
#         player_y = player_y + y_arg
#         player_x = player_x + x_arg
#         entities[player_y][player_x] = player
#     return player_y, player_x

MAP_FUCNTION = {"eight_move_direction": eight_move_direction}