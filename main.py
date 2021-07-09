from pyfzf import FzfPrompt
import notecrypt
import os

crypt = notecrypt.Crypt()

def start():
    note_list_print()

def note_save():
    note_name = crypt.encrypt(str_to_enc=input("SYSTEM: Please, input name for your note\n"), str_key=password)
    note_description = crypt.encrypt(str_to_enc=input("SYSTEM: Please, input description for your note\n"), str_key=password)

    note_count = len(os.listdir(f'./notes'))

    #notecrypt.cryptname(note_name, password)
    with open(f"./notes/{note_count+1}", "w") as note_file:
        total_note = note_name + "\n\n" + note_description
        note_file.write(total_note)

    note_continue()

def note_list_print():
    note_list = {}
    note_list["SYSTEM | Exit"] = None
    note_list["SYSTEM | Add note"] = None
    #Creating note list

    note_dir_list = os.listdir(f'./notes')
    for note_filename in note_dir_list:
        with open(f"./notes/{note_filename}", "r") as note_file:
            note_lines = note_file.readlines()
            try:
                note_name = crypt.decrypt(enc_str=note_lines[0].replace('\n', ''), str_key=password)
                note_description = crypt.decrypt(enc_str=note_lines[2], str_key=password)
            except:
                note_name = note_lines[0].replace('\n', '')
                note_description = note_lines[2]
            #note_name = note_lines[0].replace('\n', '')
            #note_description = note_lines[2]
            #note_date = str(note_file.datetime)

            note_list[note_name] = {"description": note_description}#, "date": note_date}

    target = fzf.prompt(note_list.keys())[0]

    if target == "SYSTEM | Exit":
        exit()
    elif target == "SYSTEM | Add note":
        note_save()
    else:
        os.system("clear")
        print(f"\nNOTE: {target}\n")
        print(f"{note_list[target]['description']}")

    note_continue()

def note_continue():
    input("\nSYSTEM: Input enter for continue")
    os.system("clear")
    note_list_print()

if __name__ == "__main__":
    password = input('SYSTEM: Please, write master-password with 16 or 32 letters\n')
    while len(password) < 16:
        password+=password
    password = password[:16]
    fzf = FzfPrompt()
    start()
