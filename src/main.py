from notes import notes_manager
import json

if __name__ == "__main__":
    config = None
    with open("./src/config.json", "r") as file:
        config = json.loads(file.read())
    
    neonote = notes_manager(config=config)
    neonote.main_screen()
