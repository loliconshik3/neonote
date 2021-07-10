from datetime import datetime
from pyfzf import FzfPrompt
import json
import time
import os

def edit_config():
    global config
    for editor in config['ALL_EDITORS']:
        try:
            os.system(f"{editor} ./src/config.json")
            with open("./src/config.json", "r") as file:
                config = json.loads(file.read())
            return
        except:
            pass

def clear_notes():
    choice = input("Remove all your notes. Are you sure? (y/n) ")
    if choice == "y":
        note_dir_list = os.listdir(f'./notes')
        for note_filename in note_dir_list:
            os.remove(f"./notes/{note_filename}")
            print(f"SYSTEM: Remove {note_filename}")

#==========
def note_remove():
    note_list = []
    note_list.append("SYSTEM | Return")

    note_dir_list = os.listdir(f'./notes')
    note_dir_list.sort()
    note_list+=note_dir_list

    target = fzf.prompt(note_list)[0]

    if target != "SYSTEM | Return":
        os.remove(f"./notes/{target}")

    note_continue()

def note_save():
    for editor in config['ALL_EDITORS']:
        try:
            os.system(f"cd ./notes && {editor}")
            return
        except:
            pass
#==========

def note_list_print():
    note_list = {}
    note_list["SYSTEM | Exit"] = None
    note_list["SYSTEM | Edit config"] = None
    note_list["SYSTEM | Clear notes"] = None
    note_list["SYSTEM | Remove note"] = None
    note_list["SYSTEM | Add note"] = None
    #Creating note list

    note_dir_list = os.listdir(f'./notes')
    note_dir_list.sort()
    for note_filename in note_dir_list:
        with open(f"./notes/{note_filename}", "r") as note_file:
            note_text = note_file.read()
            note_date = os.path.getmtime(f"./notes/{note_filename}")
            note_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(note_date)) 

            note_list[note_filename] = {"text" : note_text, "date" : note_date}            

    target = fzf.prompt(note_list.keys())[0]

    if target == "SYSTEM | Exit": exit()
    elif target == "SYSTEM | Edit config": edit_config()
    elif target == "SYSTEM | Clear notes": clear_notes()    
    elif target == "SYSTEM | Remove note": note_remove()
    elif target == "SYSTEM | Add note": note_save()
    else:
        os.system("clear")
        choice = fzf.prompt(['SYSTEM | Read', 'SYSTEM | Edit'])[0]
        if choice == "SYSTEM | Read":
            print(f"\nNOTE: {target} | {note_list[target]['date']}\n")
            print(f"{note_list[target]['text']}")
        elif choice == "SYSTEM | Edit":
            for editor in config['ALL_EDITORS']:
                try:
                    os.system(f"{editor} ./notes/{target}")
                    break
                except:
                    pass

    note_continue()

def note_continue():
    input("Input enter for continue...")
    os.system("clear")
    note_list_print()

if __name__ == "__main__":
    config = None
    with open("./src/config.json", "r") as file:
        config = json.loads(file.read())
        
    fzf = FzfPrompt()
    note_list_print()
