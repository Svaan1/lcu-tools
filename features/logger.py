from datetime import datetime

class Logs:
    def __init__(self, file_name):
        self.log_file = open("logs/" + file_name + ".txt", 'a', encoding="utf-8")
        self.log_file.truncate(0)

    def add(self, text):
        text = str(text)
        current_time = '[' + str(datetime.now()) + '] '
        self.log_file.write(current_time + text + "\n")
        self.log_file.flush()

class Logger:
    def __init__(self, connector, file_name="logs", uri='/', event_types=('CREATE', 'UPDATE', 'DELETE',)):
        self.connector = connector
        self.event_types = event_types
        self.uri = uri
        self.register_websockets()
        self.logs = Logs(file_name)

    def register_websockets(self):
        connector = self.connector
        
        @connector.ws.register(self.uri, event_types=self.event_types)
        async def log(connection, event):
            self.logs.add(f"[{event.type}] {event.uri} - {event.data}")

