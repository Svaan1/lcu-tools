class ReadyCheck():
    def __init__(self, connector, timer=6):
        self.timer = timer if 0 <= timer <= 12 else 0 #maybe remove this if parse the number on gui
        self.connector = connector
        self.register_websockets()

    def register_websockets(self):
        connector = self.connector
        
        @connector.ws.register('/lol-matchmaking/v1/ready-check', event_types=('UPDATE',))
        async def ready_check_accepter(connection, event):
            # Goes from 0 to 12
            if event.data['playerResponse'] == 'None' and event.data['timer'] >= self.timer:
                await connection.request('post', '/lol-matchmaking/v1/ready-check/accept')
    
