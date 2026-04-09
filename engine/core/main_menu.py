import engine.utils.terminal as terminal
from engine.systems.commands import get_command
import engine.core.exceptions as exceptions
import engine.creators.character.character_creator as character_creator
import engine.creators.map.map_creator as map_creator
import engine.editors.map.map_editor as map_editor
import engine.data as data

def main():
    terminal.clear()
    while True:
        creator = False
        editor = False
        try:
            print("INFO: YOU CAN TYPE FIRST LETTER FROM OPTIONS AS A SHORTCUT.\nDOESN'T MATTER IF IS IT LOWER OR UPPER CASE.\n")
            while True:

                    print("Choose: Creator/Editor")
                    choose = get_command("Which creator you want to use?:\n")
                    choose = choose.strip().upper()
                    print()

                    match choose:
                        case 'C' | 'CREATOR':
                            creator = True
                            break

                        case 'E' | 'EDITOR':
                            editor = True
                            break

                        case _:
                            print(f"'{choose}' is a incorrect choose. Please choose only character or map.")

            while creator:

                    print("Choose: Character/Map")
                    choose = get_command("Which creator you want to use?:\n")
                    choose = choose.strip().upper()
                    print()

                    match choose:
                        case 'C' | 'CHARACTER':
                            character_creator.main()

                        case 'M' | 'MAP':
                            map_creator.main()

                        case _:
                            print(f"'{choose}' is a incorrect choose. Please choose only character or map.")

            while editor:

                    print("Choose: Map")
                    choose = get_command("Which editor you want to use?:\n")
                    choose = choose.strip().upper()
                    print()

                    match choose:
                        case 'M' | 'MAP':
                            map_editor.main()

                        case _:
                            print(f"'{choose}' is a incorrect choose. Please choose only character or map.")
        except exceptions.ExitTool:
            terminal.clear()
            print("Returning to main menu.\n")
            continue
        except exceptions.NoJsonFile:
            terminal.clear()
            print("No json file in data!\n")
            continue

if __name__ == '__main__':
    main()