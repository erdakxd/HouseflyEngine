import json

class Quest:
    def __init__(self, name):
        self.name = name
        Quest.desc = ""
        Quest.quest_giver = ""
        Quest.condition = ""
        Quest.reward = ""

quest_number = 0
dictionary_of_quests = {}
    
if __name__ == '__main__':

    while True:
        name = str(input("Enter name for quest: "))
        quest = Quest(name)
        quest.quest_giver = str(input("Enter name for quest giver: "))
        quest.condition = str(input("Enter condition to complete a quest: "))
        quest.reward = str(input("Enter reward for completing quest: "))
        quest.desc = str(input("Enter a description for quest:\n"))
        quest_number += 1
        dictionary_of_quests[quest_number] = [{'name': quest.name}, {'quest_giver': quest.quest_giver},
                                                    {'condition': quest.condition}, {'reward': quest.reward},
                                                    {'description': quest.desc}]
        print(f"Current dictionary of quests:\n{dictionary_of_quests}")
        more_quests = str(input("Do you want to make more quests? (Yes/No/Delete/Clear): ")).upper()
        match more_quests:
            case "Y" | "YES":
                pass
            case "N" | "NO":
                break
            case "D" | "DELETE":
                try:
                    print(f"You delete a {quest.name} quest.")
                    dictionary_of_quests.popitem()
                    quest_number -= 1
                    continue
                except KeyError:
                    print("Dictionary 'quests' is empty!")
                    continue
            case "C" | "CLEAR":
                print("You clear whole dictionary of quests.")
                quest_number = 0
                dictionary_of_quests.clear()
                continue
            case _:
                print("Wrong answer. Please write: Yes, No, Delete or Clear.")
    file_path = "Projects/Fly Engine/data/quests.json"

    try:
        with open(file=file_path, mode="w") as file:
            json.dump(dictionary_of_quests, file, indent=4)
            print("Json file was created.")
    except Exception:
        print("Somethin went wrong.")
