import os
import json

STORAGE_FILE="dotfiled.json"

class dotfiler:
    def __init__(self):
        self.target = None
        self.source = None
        with open(STORAGE_FILE, "r") as f:
                self.json = json.load(f)

    def store(self):
        with open(STORAGE_FILE, "w") as f:
            json.dump(self.json, f)

    def add(self, source: str, target: str):
        try:
            os.replace(source, target)
            os.link(target, source)
            self.json[target] = source
            print(f"Added {target} to dotfiles\n");
        except Exception as e:
            print(e);

