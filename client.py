import socket
import time
from tools import backup_project
from globaldata import SERVER_SETTINGS


class Client:

    def __init__(self, username, ip, port):
        self.username = username
        self.ip = ip
        self.port = port
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip, port)

        self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time

        confirmation = f"{self.username} connected".encode()
        self.udp_socket.sendto(confirmation, self.server_address)
    
    def exit(self):
        confirmation = f"{self.username} is disconnecting".encode()
        self.udp_socket.sendto(confirmation, self.server_address)
        self.udp_socket.close()
        print("Client shutting down.")


def main(username, ip, port):
    client = Client(username=username, ip=ip, port=port)
    
    run = True
    while run:
        example_data = "Hello, World!".encode()
        client.udp_socket.sendto(example_data, client.server_address)

        client.elapsed_time = time.time() - client.start_time
        time.sleep(max(0, SERVER_SETTINGS.TICK_INTERVAL - client.elapsed_time))

    client.exit()

if __name__ == "__main__":
    backup_project()
    main(username="testuser", ip="192.168.0.191", port=5011)