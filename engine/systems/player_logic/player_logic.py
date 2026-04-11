import general_systems

GAME_COMMANDS = {}

EIGHT_MOVE_DIRECTION_COMMANDS = {
    frozenset(("W")): general_systems.eight_move_direction,
    frozenset(("S")): general_systems.eight_move_direction,
    frozenset(("A")): general_systems.eight_move_direction,
    frozenset(("D")): general_systems.eight_move_direction,
    frozenset(("A, W")): general_systems.eight_move_direction,
    frozenset(("D, W")): general_systems.eight_move_direction,
    frozenset(("A, S")): general_systems.eight_move_direction,
    frozenset(("D, S")): general_systems.eight_move_direction,
}

def func_start(prompt):
    if prompt in GAME_COMMANDS:
        GAME_COMMANDS[prompt]()