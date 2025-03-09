import socket
import time
import sys
print("client.py")


class Client:

    def __init__(self, username, ip):
        # client details
        self.username = username
        self.ip = ip
        self.port = 5011
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (ip, self.port)

        # elapsed time counter
        self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time

        # send connection confirmation to server
        confirmation = f"{self.username} connected".encode()
        self.udp_socket.sendto(confirmation, self.server_address)
        print(f"Sent connection confirmation to {self.server_address}")
    
    def exit(self):
        # send disconnection message to server
        confirmation = f"{self.username} is disconnecting".encode()
        self.udp_socket.sendto(confirmation, self.server_address)
        self.udp_socket.close()
        print("Client shutting down.")


def main(username, ip):

    client = Client(username=username, ip=ip)
    #client.exit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Invalid data provided.")
        sys.exit(1)
    else:
        main(username=sys.argv[1], ip=sys.argv[2])
