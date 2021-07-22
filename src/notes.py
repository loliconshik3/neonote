from datetime import datetime
from pyfzf import FzfPrompt
import json
import time
import os

class notes_manager():

    def __init__(self, config):
        self.config = config
        self.fzf = FzfPrompt()

    def clear(self):
        choice = input("Remove all your notes. Are you sure? (y/n) ")
        if choice == "y":
            note_dir_list = os.listdir(f'./notes')
            for note_filename in note_dir_list:
                os.remove(f"./notes/{note_filename}")
                print(f"SYSTEM: Remove {note_filename}")

    def remove(self):
        note_list = ["SYSTEM | Return"]

        note_dir_list = os.listdir(f'./notes')
        note_dir_list.sort()
        note_list+=note_dir_list

        target = self.fzf.prompt(note_list)[0]

        if target != "SYSTEM | Return":
            os.remove(f"./notes/{target}")

        self.continue_screen()

    def add(self):
        for editor in self.config['ALL_EDITORS']:
            try:
                os.system(f"cd ./notes && {editor}")
                return
            except:
                pass

    def continue_screen(self):
        input("Input enter for continue...")
        os.system("clear")
        self.main_screen()

    def main_screen(self):
        note_list = {
            "SYSTEM | Exit" : None,
            "SYSTEM | Edit config" : None,
            "SYSTEM | Clear notes" : None,
            "SYSTEM | Remove note" : None,   
            "SYSTEM | Add note" : None
        }
        #Creating note list

        note_dir_list = os.listdir(f'./notes')
        note_dir_list.sort()
        for note_filename in note_dir_list:
            with open(f"./notes/{note_filename}", "r") as note_file:
                note_text = note_file.read()
                note_date = os.path.getmtime(f"./notes/{note_filename}")
                note_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(note_date)) 

                note_list[note_filename] = {"text" : note_text, "date" : note_date}            

        target = self.fzf.prompt(note_list.keys())[0]

        if target == "SYSTEM | Exit": exit()
        elif target == "SYSTEM | Edit config": self.edit_config()
        elif target == "SYSTEM | Clear notes": self.clear()    
        elif target == "SYSTEM | Remove note": self.remove()
        elif target == "SYSTEM | Add note": self.add()
        else:
            os.system("clear")
            choice = self.fzf.prompt(['SYSTEM | Read', 'SYSTEM | Edit'])[0]

            if choice == "SYSTEM | Read":
                print(f"\nNOTE: {target} | {note_list[target]['date']}\n")
                print(f"{note_list[target]['text']}")

            elif choice == "SYSTEM | Edit":
                for editor in self.config['ALL_EDITORS']:
                    try:
                        os.system(f"{editor} './notes/{target}'")
                        break
                    except:
                        pass

        self.continue_screen()

    def edit_config(self):
        for editor in self.config['ALL_EDITORS']:
            try:
                os.system(f"{editor} ./src/config.json")
                with open("./src/config.json", "r") as file:
                    self.config = json.loads(file.read())
                return
            except:
                pass