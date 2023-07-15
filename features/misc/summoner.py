from config.app_config import config
from features.misc.data_dragon import data_dragon

class ChampionSelectPreferences:
    def __init__(self, role):
        self.preferences = config.preferences["champion_select"]["preferences"][role]
        self.picks = [data_dragon.champions.by_id(champion) for champion in self.preferences["picks"]]
        self.bans = [data_dragon.champions.by_id(champion) for champion in self.preferences["bans"]]
        self.hover = self.picks[0]
        
class SummonerRunes():
    def __init__(self, connection):
        self.connection = connection

    async def get_current(self):
        response = await self.connection.request('get', '/lol-perks/v1/currentpage')
        return await response.json()
    
    async def delete_by_id(self, runepage_id):
        response = await self.connection.request('delete', f"/lol-perks/v1/pages/{runepage_id}")
        return response.status
    
    async def set_recommended(self, champion, rune_index=0):
        recommended_runes = await self.connection.request('get', f'/lol-perks/v1/recommended-pages/champion/{champion.key}/position/TOP/map/11')
        recommended_runes = await recommended_runes.json()
        recommended_runes = recommended_runes[rune_index]

        current_rune = await self.get_current()
        if current_rune.get("id"):
            deleted = await self.delete_by_id(current_rune["id"])

        new_runepage = {
            "name": f"{champion.id} -  {recommended_runes['primaryRecommendationAttribute'][1:]} and {recommended_runes['secondaryRecommendationAttribute'][1:]}",
            "primaryStyleId": recommended_runes["primaryPerkStyleId"],
            "subStyleId": recommended_runes["secondaryPerkStyleId"],     
            "selectedPerkIds": [perk["id"] for perk in recommended_runes["perks"]],
            "current": True
        }

        created = await self.connection.request('post', "/lol-perks/v1/pages", data=new_runepage)
        return {"rune_page": new_runepage, "spells": recommended_runes["summonerSpellIds"]}

class Summoner():
    def __init__(self, connection):
        self.runes = SummonerRunes(connection)
        # Implement more features, icons maybe
