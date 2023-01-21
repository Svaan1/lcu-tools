from weakref                    import WeakValueDictionary
from config.app_config                 import ChampionSelectPreferences
from features.misc.summoner     import Summoner
from features.misc.data_dragon  import DataDragon

class ChampionSelect:
    def __init__(self, connector):
        global session
        session = None
        self.connector = connector
        self.register_websockets()

    def register_websockets(self):
        connector = self.connector

        @connector.ws.register('/lol-champ-select/v1/session', event_types=('CREATE', 'UPDATE',))
        async def champion_select(connection, event):
            session = await ChampionSelectSession(connection).refresh(event)

class ChampionSelectSession:
    def __init__(self, connection):
        self.connection = connection
        self.game_id = None

    def new_game(self):
        self.complete_phases = []
        self.game_id = self.data["gameId"]
        for teammate in self.data["myTeam"]:
            if teammate["cellId"] == self.data["localPlayerCellId"]:
                self.preferences = ChampionSelectPreferences(teammate["assignedPosition"])

    async def refresh(self, event):
        self.data = event.data
        if self.data["gameId"] != self.game_id:
            self.new_game()

        current_phase = self.data["timer"]["phase"]
        if current_phase == "PLANNING" and "PLANNING" not in self.complete_phases:
            await self.pre_hover()
        elif current_phase == "BAN_PICK" and "BANNING" not in self.complete_phases:
            await self.pre_ban()
        elif current_phase == "BAN_PICK" and "PICKING" not in self.complete_phases:
            await self.pre_pick()
    
        return self
        
    async def pre_hover(self):
        for actions in self.data['actions']:
            for action in actions:
                if (action['type'] == "pick" and action['actorCellId'] == self.data["localPlayerCellId"]):
                    return await self.hover(action['id'], self.preferences.hover)

    async def hover(self, action_id, champion_id):
        await self.connection.request('patch', f'/lol-champ-select/v1/session/actions/{action_id}',
                                data={"championId": champion_id})
        self.complete_phases.append("PLANNING")

    async def pre_ban(self):
        ally_champs = []
        for actions in self.data['actions']:
            for action in actions:
                if action['type'] == "ban" and action['actorCellId'] == self.data["localPlayerCellId"] and action['isInProgress']:
                    available_champions = [champion for champion in self.preferences.bans if champion.id not in ally_champs]
                    print(f"AVAILABLE_CHAMPIONS = {available_champions}")
                    return await self.ban(action['id'], available_champions[0].key)
                if action['type'] == "pick" and action['actorCellId'] // 5 == self.data["localPlayerCellId"] // 5:
                    if action['championId'] != 0:
                        ally_champs.append(action['championId'])
                        print(f"ALLY CHAMPION = {action['championId']} --- {ally_champs}")

    async def ban(self, action_id, champion_id):
        await self.connection.request('patch', f'/lol-champ-select/v1/session/actions/{action_id}',
                                    data={"championId": champion_id, "completed": True})
        self.complete_phases.append("BANNING")

    async def pre_pick(self):
        unavailable_champions = []
        for actions in self.data['actions']:
            for action in actions:
                if action['type'] == "pick" and action['actorCellId'] == self.data["localPlayerCellId"] and action['isInProgress']:
                    available_champions = [champion for champion in self.preferences.picks if champion.id not in unavailable_champions]
                    print(f"AVAILABLE CHAMPIONS = {available_champions}")
                    return await self.pick(action['id'], available_champions[0].key)
                if action['type'] == "pick" and action['actorCellId'] != self.data["localPlayerCellId"] and action['completed'] or action['type'] == "ban" and action['completed']:
                    unavailable_champions.append(str(action['championId']))
                    print(f"UNAVAILABLE CHAMPIONS = {str(action['championId'])} --- {unavailable_champions}")

    async def pick(self, action_id, champion_id):
        await self.connection.request('patch', f'/lol-champ-select/v1/session/actions/{action_id}',
                                    data={"championId": champion_id, "completed": True})
        self.complete_phases.append("PICKING")