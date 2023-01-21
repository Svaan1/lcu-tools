from datetime import datetime

class Logger:
    def __init__(self, connector, file_name="logs", uri='/', event_types=('CREATE', 'UPDATE', 'DELETE',)):

        self.connector = connector
        self.event_types = event_types
        self.uri = uri

        self.log_file = open("logs/" + file_name + ".txt", 'a', encoding="utf-8")
        self.log_file.truncate(0)

        self.register_websockets()

    def register_websockets(self):
        connector = self.connector
        
        @connector.ws.register(self.uri, event_types=self.event_types)
        async def log(connection, event):
            self.add_to_log(f"[{event.type}] {event.uri} - {event.data}")

    def add_to_log(self, text):
        current_time = '[' + str(datetime.now()) + '] '
        self.log_file.write(current_time + str(text) + "\n")
        self.log_file.flush()
