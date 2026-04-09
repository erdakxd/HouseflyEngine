import engine.core.exceptions as exceptions
from engine.systems.commands import get_command
import engine.utils.terminal as terminal
import engine.creators.character.character_creator as character_creator
import engine.creators.map.map_creator as map_creator
import engine.editors.map.map_editor as map_editor
import engine.editors.character.character_editor as character_editor

stack = []

class Menu:
    def run(self):
        pass

# ---------------------------------------------------------------------------------------------------------------------

# *****************
# *** MAIN MENU ***
# *****************

class MainMenu(Menu):
    def run(self):
        terminal.clear()
        while True:
            try:
                print("INFO: YOU CAN TYPE FIRST LETTER FROM OPTIONS AS A SHORTCUT.\nDOESN'T MATTER IF IT IS LOWER OR UPPER CASE.\n")
                while True:
                        
                        print("Choose: Creator/Editor")
                        choose = get_command("Which creator you want to use?:\n")
                        choose = choose.strip().upper()
                        print()

                        match choose:
                            case 'C' | 'CREATOR':
                                stack.append(CreatorsMenu())
                                return

                            case 'E' | 'EDITOR':
                                stack.append(EditorsMenu())
                                return

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

# *********************
# *** CREATORS MENU ***
# *********************

class CreatorsMenu(Menu):
    def __init__(self):
        self.game_map = None

    def run(self):
        while True:
            print("Choose: Character/Map")
            choose = get_command("Which creator you want to use?:\n")
            choose = choose.strip().upper()

            match choose:
                case 'C' | 'CHARACTER':
                    stack.append(CharacterCreator())
                    return

                case 'M' | 'MAP':
                    self.game_map = map_creator.GameMap
                    self.game_map.y = None
                    self.game_map.x = None
                    self.game_map.game_map = {}
                    stack.append(MapCreator(self.game_map))
                    return

                case _:
                    print(f"'{choose}' is a incorrect choose. Please choose only character or map.")

# ***************
# *** EDITORS ***
# ***************

class EditorsMenu(Menu):
    def run(self):
        print("Choose: Map/Players/Enemies")
        choose = get_command("Which editor you want to use?:\n")
        choose = choose.strip().upper()

        match choose:
            case 'M' | 'MAP':
                stack.append(MapEditor())
                return
            
            case 'P' | 'PLAYERS':
                stack.append(CharacterEditor("engine/data/players/players.json"))
                return

            case 'E' | 'ENEMIES':
                stack.append(CharacterEditor("engine/data/enemies/enemies.json"))
                return

            case _:
                print(f"'{choose}' is a incorrect choose. Please choose only character or map.")
    
# ^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^ CHARACTER EDITOR ^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^

class CharacterEditor(Menu):
    def __init__(self, path):
        self.check = True
        self.character_path = path

    def run(self):
        character_dict = character_editor.load_map(self.character_path)

        if self.check:
            terminal.clear()
            self.check = False

        choose = character_editor.set_edit(character_dict)
        stack.append(EditCharacter(character_dict, choose, self.character_path))
        return
        character_list = []
        for key in character_dict.keys():
            print(f"{key}")
            character_list.append(key)
        
        choose = get_command("Enter number or name of character you want to edit:\n")
        try:
            choose = int(choose)
            if choose in character_list:
                stack.append(EditCharacter(choose))
                return
            else:
                print("Wrong 'number' or 'name'.")
        except ValueError:
            choose = str(choose)
            if choose in character_list:
                stack.append(EditCharacter(choose))
                return
            else:
                print("Wrong 'number' or 'name'.")

# ^^^^^^^^^^^^^^^^^^
# ^^^ MAP EDITOR ^^^
# ^^^^^^^^^^^^^^^^^^

class MapEditor(Menu):
    def __init__(self):
        pass

    def run(self):
        terminal.clear()
        map_editor.load_map()
        print("Choose: Layer/Object/Tool/Map/Export")
        choose = get_command("What do you want to change?:\n")
        choose = choose.strip().upper()
        match choose:
            case 'L' | 'LAYER':
                stack.append(Layer())
                return
            case 'O' | 'OBJECT':
                stack.append(Texture())
                return
            case 'T' | 'TOOL':
                stack.append(Tool())
                return
            case 'M' | 'MAP':
                stack.append(GameMap())
                return
            case 'E' | 'EXPORT':
                stack.append(Export())
                return
            case _:
                print(f"\n{choose} is a incorrect choose.\n")
    
# ^^^^^^^^^^^^^^^^^^^^^^^^^
# ^^^ CHARACTER CREATOR ^^^
# ^^^^^^^^^^^^^^^^^^^^^^^^^

class CharacterCreator(Menu):
    def __init__(self):
        self.character = None

    def run(self):
        while True:
            print(f'Choose: Player/Enemy')
            choose = get_command("Enter a character you want to create:\n")
            choose = choose.strip().upper()
            match choose:
                case 'P' | 'PLAYER':
                    self.character = character_creator.Player
                    self.character.name = "None"
                    self.character.symbol = "None"
                    self.character.vision = 7
                    stack.append(Character(self.character))
                    return
            
                case 'E' | 'ENEMY':
                    self.character = character_creator.Enemy
                    self.character.name = "None"
                    self.character.symbol = "None"
                    self.character.vision = 7
                    stack.append(Character(self.character))
                    return
                
                case _:
                    print(f"'{choose}' is not correct choose. Please choose player or enemy.\n")

# ----------------------
# --- EDIT CHARACTER ---
# ----------------------

class EditCharacter(Menu):
    def __init__(self, character_dict, character, file_path):
        self.character_dict = character_dict
        self.character = character
        self.file_path = file_path
        self.check = True
    def run(self):
        if self.check:
            terminal.clear()
            self.check = False

        choose = character_editor.character_edit(self.character, self.character_dict)
        if choose in ('s', 'save'):
            stack.append(SaveForEdit(self.character_dict, self.character, self.file_path))
        else:
            stack.append(Edit(choose, self.character, self.character_dict))
        return

# -------------------------
# --- CHARACTER CREATOR ---
# -------------------------

class Character(Menu):
    def __init__(self, character):
        self.character = character
        self.check = True

    def run(self):
        if self.check:
            terminal.clear()
            self.check = False
        while True:
            print("Choose: Name/Sy-Symbol/Vision/Dictionary/Sa-Save/Clear/Export")
            choose = get_command("What do you want to change?:\n")
            choose = choose.strip().upper()
            match choose:
                case 'N' | 'NAME':
                    stack.append(Name(self.character))
                    return
                case 'SY' | 'SYMBOL':
                    stack.append(Symbol(self.character))
                    return
                case 'V' | 'VISION':
                    stack.append(Vision(self.character))
                    return
                case 'D' | 'DICTIONARY':
                    stack.append(ShowDict(self.character))
                    return
                case 'SA' | 'SAVE':
                    stack.append(Save(self.character))
                    return
                case 'C' | 'CLEAR':
                    stack.append(Clear(self.character))
                    return
                case 'E' | 'EXPORT':
                    stack.append(Export(self.character))
                    return
                case _:
                    print(f"\n{choose} is a incorrect choose.\n")

# -------------------
# --- MAP CREATOR ---
# -------------------

class MapCreator(Menu):
    def __init__(self, game_map):
        self.game_map = game_map
        self.check = True

    def run(self):
        if self.check:
            terminal.clear()
            self.check = False
        
        while True:
            print("Choose: Layers/Size/Game Map/Clear/Export")
            choose = get_command("What do you want to change?:\n")
            choose = choose.strip().upper()
            match choose:
                case 'L' | 'LAYERS':
                    stack.append(Layer(self.game_map))
                    return
                case 'S' | 'SIZE':
                    stack.append(Size(self.game_map))
                    return
                case 'G' | 'GAME MAP':
                    stack.append(ShowDict(self.game_map))
                    return
                case 'C' | 'CLEAR':
                    stack.append(Clear(self.game_map))
                    return
                case 'E' | 'EXPORT':
                    stack.append(Export(self.game_map))
                    return
                case _:
                    print(f"\n{choose} is a incorrect choose.\n")

# --- GENERAL CLASSES ---

class Edit(Menu):
    def __init__(self, choose, character, dictionary):
        self.choose = choose
        self.character = character
        self.dictionary = dictionary

    def run(self):
        edit_choose = character_editor.edit(self.choose, self.character, self.dictionary)
        self.dictionary[self.character][self.choose] = edit_choose
        stack.pop()
        print('Works')
        return

class Name(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.name = character_creator.get_name('player')
        elif self.character == character_creator.Enemy:
            self.character.name = character_creator.get_name('enemy')
        stack.pop()
        terminal.clear()
        return

class Symbol(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.symbol = character_creator.get_symbol('player')
        elif self.character == character_creator.Enemy:
            self.character.symbol = character_creator.get_symbol('enemy')
        stack.pop()
        terminal.clear()
        return

class Vision(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            self.character.vision = character_creator.get_vision('player')
        elif self.character == character_creator.Enemy:
            self.character.vision = character_creator.get_vision('enemy')
        stack.pop()
        terminal.clear()
        return
    
class SaveForEdit(Menu):
    def __init__(self, dictionary, character, file_path):
        self.dictionary = dictionary
        self.character = character
        self.file_path = file_path

    def run(self):
        check = character_editor.save(self.dictionary, self.character, self.file_path)
        if check:
            stack.pop()
        stack.pop()
        return
    
class Save(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        try:
            if self.character == character_creator.Player:
                character_creator.Player(self.character.name, self.character.symbol, self.character.vision)
            elif self.character == character_creator.Enemy:
                character_creator.Enemy(self.character.name, self.character.symbol, self.character.vision)
            self.character.name = None
            self.character.symbol = None
            self.character.vision = 7
        except AttributeError:
            terminal.clear
            print("They are some none element characters. Please set every element for character")
            stack.pop()
            return
        stack.pop()
        terminal.clear()
        return

class Delete(Menu):
    pass

class Clear(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        print("Choose: Yes/No")
        choose = get_command("Do you want to clear dictionary?:\n")
        choose = choose.strip().upper()
        match choose:
            case 'Y' | 'YES':
                if self.character == map_creator.GameMap:
                    self.character.game_map.clear()
                else:
                    self.character.characters.clear()
                terminal.clear()
            case 'N' | 'NO':
                terminal.clear()
            case _:
                terminal.clear()
                print("Wrong choose.\n")
        stack.pop()
        return

class ShowDict(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == map_creator.GameMap:
            map_creator.render_map()
        else: 
            character_creator.get_character_dict(self.character.characters)
        stack.pop()
        return

class Export(Menu):
    def __init__(self, character):
        self.character = character

    def run(self):
        terminal.clear()
        if self.character == character_creator.Player:
            character_creator.get_export('players', character_creator.Player.characters)    
        elif self.character == character_creator.Enemy:
            character_creator.get_export('enemies', character_creator.Enemy.characters)
        elif self.character == map_creator.GameMap:
            map_creator.get_export('game_map', self.character.game_map)
        stack.pop()
        return

class Size(Menu):
    def __init__(self, game_map):
        self.game_map = game_map

    def run(self):
        if self.game_map == map_creator.GameMap:
            self.game_map.y = map_creator.map_position_xy('y')
            self.game_map.x = map_creator.map_position_xy('x')
            map_creator.game_size('0')
        stack.pop()
        terminal.clear()
        return

class Layer(Menu):
    def __init__(self, game_map):
        self.game_map = game_map

    def run(self):
        if self.game_map == map_creator.GameMap:
            map_creator.get_layer()

        else:
            self.editor.layer = map_editor.set_layer()
        stack.pop()
        terminal.clear()
        return

class Texture(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.texture = map_editor.set_texture()
        stack.pop()
        return

class Tool(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.tool = map_editor.set_tool()
        stack.pop()
        return

class GameMap(Menu):
    def __init__(self, editor):
        self.editor = editor

    def run(self):
        self.editor.game_map = map_editor.edit_map()
        stack.pop()
        return

# ************
# *** MAIN ***
# ************

def main():
    stack.append(MainMenu())

    while stack:
        try:
            current = stack[-1]
            current.run()

        except exceptions.Back:
            stack.pop()
        except exceptions.ExitDebugger:
            pass
        except exceptions.NoJsonFile:
            print('No Json File.')
            stack.pop()

if __name__ == '__main__':
    main()