from lcu_driver import Connector
from features.ready_check import ReadyCheck
from features.champion_select import ChampionSelect
from features.misc.summoner import SummonerRunes
from features.misc.data_dragon import DataDragon

connector = Connector()

@connector.ready
async def connect(connection):
    print("Ready")

ReadyCheck(connector)

connector.start()
