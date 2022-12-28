from lcu_driver import Connector
from features.ready_check import ReadyCheck
from features.logger import Logger

connector = Connector()

@connector.ready
async def connect(connection):
    print("Connected")
    
Logger(connector,file_name="ready_check", uri="/lol-matchmaking/v1/ready-check")
ReadyCheck(connector)

connector.start()
