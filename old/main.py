from datetime import datetime
from pyfzf import FzfPrompt
import notecrypt
import utils
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

def note_remove():
    note_list = {}
    note_list["SYSTEM | Return"] = None

    note_dir_list = os.listdir(f'./notes')
    note_dir_list.sort()
    for note_filename in note_dir_list:
        with open(f"./notes/{note_filename}", "r") as note_file:
            note_lines = note_file.readlines()
            try:
                note_name = crypt.decrypt(enc_str=note_lines[0].replace('\n', ''), str_key=password)

                note_list[note_name] = {"filename": note_filename}
            except:
                pass

    target = fzf.prompt(note_list.keys())[0]

    if target != "SYSTEM | Return":
        os.remove(f"./notes/{note_list[target]['filename']}")

    note_continue()

#==========
def note_save():
    #filename = input("SYSTEM: Please, input name for your note\n")
    for editor in config['ALL_EDITORS']:
        try:
            os.system(f"cd ./notes && {editor}")
            return
        except:
            pass
#==========

#def note_save():
#    filename = input("SYSTEM: Please, input name for your note\n")
#    note_name = crypt.encrypt(str_to_enc=filename, str_key=password)
#    os.system("clear")
#    print("SYSTEM: Please, input description for your note")
#    note_description = crypt.encrypt(str_to_enc="\n".join(iter(input, "")), str_key=password)
#    os.system("clear")
#    #note_description = crypt.encrypt(str_to_enc=input("SYSTEM: Please, input description for your note\n"), str_key=password)
#
#    #note_count = len(os.listdir(f'./notes'))
#
#    filename = str(datetime.now())#.strftime('%Y-%m-%d %H:%M:%S'))
#    with open(f"./notes/{filename}", "w+") as note_file:
#        total_note = note_name + "\n\n" + note_description
#        note_file.write(total_note)
#
#    note_continue()

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

        #with open(f"./notes/{note_filename}", "r") as note_file:
        #    note_lines = note_file.readlines()
        #    try:
        #        note_name = crypt.decrypt(enc_str=note_lines[0].replace('\n', ''), str_key=password)
        #        note_description = crypt.decrypt(enc_str=''.join(note_lines[2:]), str_key=password)
        #        note_date = os.path.getmtime(f"./notes/{note_filename}")
        #        note_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(note_date))
        #        
        #        if note_name in note_list.keys():
        #            os.remove(f"./notes/{note_list[note_name]['filename']}")

        #        note_list[note_name] = {"description": note_description, "date": note_date, "filename": note_filename}
        #    except:
        #        pass
                #note_name = note_lines[0].replace('\n', '')
                #note_description = note_lines[2]
                #note_date = "Undefind"
            

    target = fzf.prompt(note_list.keys())[0]

    if target == "SYSTEM | Exit": exit()
    elif target == "SYSTEM | Edit config": edit_config()
    elif target == "SYSTEM | Clear notes": clear_notes()    
    elif target == "SYSTEM | Remove note": note_remove()
    elif target == "SYSTEM | Add note": note_save()
    else:
        os.system("clear")
        print(f"\nNOTE: {target} | {note_list[target]['date']}\n")
        print(f"{note_list[target]['text']}")

    note_continue()

def note_continue():
    input("\nSYSTEM: Input enter for continue")
    os.system("clear")
    note_list_print()

if __name__ == "__main__":
    config = None
    with open("./src/config.json", "r") as file:
        config = json.loads(file.read())
        
#    password = input('SYSTEM: Please, write master-key with 16 or 32 letters\n')
#    while len(password) < 16:
#        password+=password
#    if len(password) != 32:
#        password = password[:16]

#    crypt = notecrypt.Crypt()
#    os.system("clear")
    fzf = FzfPrompt()
    note_list_print()
