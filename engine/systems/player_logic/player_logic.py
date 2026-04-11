import engine.systems.player_logic.player_func as player_func

GAME_COMMANDS = {}

EIGHT_MOVE_DIRECTION_COMMANDS = {
    frozenset(("W")): player_func.eight_move_direction,
    frozenset(("S")): player_func.eight_move_direction,
    frozenset(("A")): player_func.eight_move_direction,
    frozenset(("D")): player_func.eight_move_direction,
    frozenset(("A, W")): player_func.eight_move_direction,
    frozenset(("D, W")): player_func.eight_move_direction,
    frozenset(("A, S")): player_func.eight_move_direction,
    frozenset(("D, S")): player_func.eight_move_direction,
}

def func_start(prompt):
    if prompt in GAME_COMMANDS:
        GAME_COMMANDS[prompt]()