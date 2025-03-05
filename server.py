import socket
import time
from tools import backup_project
from globaldata import SERVER_SETTINGS


class Server:
    def __init__(self, port):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('localhost', port)
        self.udp_socket.bind(self.server_address)
        print(f"Server started on port {port}... Waiting for clients.")

        self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time
        
        self.clients = 0
        self.client_addresses = []
    
    def exit(self):
        self.udp_socket.close()
        print("Server shutting down.")


def main(port):
    
    server = Server(port)
    
    run = True
    while run:

        server.elapsed_time = time.time() - server.start_time
        time.sleep(max(0, SERVER_SETTINGS.TICK_INTERVAL - server.elapsed_time))

    server.exit()


if __name__ == "__main__":
    backup_project()
    main(5011)
