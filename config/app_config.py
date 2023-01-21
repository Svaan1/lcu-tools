import json
from features.misc.data_dragon import DataDragon

preferences_file = open("config/preferences.json")
preferences = json.load(preferences_file)
data_dragon = DataDragon()

class ChampionSelectPreferences():
    def __init__(self, role):
        options = preferences["champion_select"]["preferences"][role]
        self.picks = [data_dragon.champions.by_id(champion) for champion in options["picks"]]
        self.bans = [data_dragon.champions.by_id(champion) for champion in options["bans"]]
        self.hover = self.picks[0]



