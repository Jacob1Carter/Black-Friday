
class SERVER_SETTINGS:
    def __init__(self):
        self.MAX_CLIENTS = 4
        self.TICK_RATE = 30
        self.TICK_INTERVAL = 1 / self.TICK_RATE

SERVER_SETTINGS = SERVER_SETTINGS()