import requests
from config.app_config import config

class Champion():
    def __init__(self, id, key):
        self.id = id
        self.key = key
    
    def __str__(self):
        return f"Name: {self.id}\nId: {self.key}"

class LeagueChampions():
    def __init__(self, version):
        self.version = version
        self.all = self.get_all()
    
    def get_all(self):
        return requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/champion.json").json()

    def by_id(self, id):
        try:
            key = self.all["data"][id]['key']
            return Champion(id, key)
        except:
            return None

    def by_key(self, key):
        champions = self.all["data"]
        for name in champions:
            if champions[name]["key"] == str(key):
                id = champions[name]['id']
                return Champion(id, key)

class SummonerSpell(): #WIP
    def __init__(self):
        pass

class LeagueSummonerSpells():
    def __init__(self, version):
        self.version = version
        self.all = self.get_all()

    def get_all(self):
        spells = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{self.version}/data/en_US/summoner.json").json()
        return spells
    
    def by_name(self, name):
        name = name.capitalize()
        spell_list = self.all["data"]
        for spell in spell_list:
            if spell_list[spell]["name"] == name:
                return spell_list[spell]
    
    def by_id(self, key):
        spell_list = self.all["data"]
        for spell in spell_list:
            if spell_list[spell]["key"] == str(key):
                return spell_list[spell]    

class DataDragon():
    def __init__(self):
        self.version = self.get_league_version()
        self.champions = LeagueChampions(self.version)
        self.spells = LeagueSummonerSpells(self.version)
    
    def get_league_version(self):
        try:
            version = requests.get("https://ddragon.leagueoflegends.com/api/versions.json").json()[0]
            config.preferences["last_known_version"] = version
            config.save_changes()
        except:
            version = config.preferences["last_known_version"]

        return version

data_dragon = DataDragon()