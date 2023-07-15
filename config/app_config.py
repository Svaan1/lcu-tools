import json

class Config:
    def __init__(self):
        file = open("config/preferences.json", "r")
        self.preferences = json.load(file)
        file.close()

    def save_changes(self):
        file = open("config/preferences.json", "w")
        json.dump(self.preferences, file, indent=4)
        file.close()

config = Config()
