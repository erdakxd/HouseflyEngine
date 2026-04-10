import engine.core.exceptions as exceptions
# import engine.core.navigation as navigation 
# --- TRY SYS MODULE ---

# VARIABLES
running = True

def debugger(command):
    while True:
        command = input("\nType command:\n")
        print()
        if command in GLOBAL_COMMANDS:
            command = GLOBAL_COMMANDS[command]()
            return command
        else:
            print("Wrong command")
            print()

# NOT WORKING
def exit_loop():
    global running
    print("Exit looper")
    running = False
    return running

def next_line():
    next(get_command())
# --------------------------

def back_menu():
    raise exceptions.Back()

def exit_program():
    print("Satan is real!")
    exit()

def exit_debugger():
    print("Cheese!\n")
    raise exceptions.ExitDebugger()


GLOBAL_COMMANDS = {
    "break": exit_loop,
    "step": next_line,
    "back": back_menu,
    "exit": exit_program,
    "c mouse": exit_debugger
}

def get_command(prompt="> "):
    global command
    command = input(prompt)
    if command == "c housefly":
        debugger(command)
    elif command == 'exit menu':
        while True:
            print('\nChoose: Yes/No')
            choose = input('Do you want to back to menu?:\n')
            choose = choose.upper()
            match choose:
                case 'Y' | 'YES':
                    raise exceptions.ExitTool()

                case 'N' | 'NO':
                    return command

                case _:
                    print(f"'{choose}' is a incorrect choose. Please choose yes or no.")
    else:
        return command
    
if __name__ == '__main__':
    value = debugger(None)
    print(running)