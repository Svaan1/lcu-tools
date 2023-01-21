from lcu_driver import Connector
from features.misc.data_dragon import DataDragon
from features.ready_check import ReadyCheck
from features.champion_select import ChampionSelect

connector = Connector()

@connector.ready
async def connect(connection):
    print("Ready")
    
ChampionSelect(connector)
ReadyCheck(connector)

connector.start()
