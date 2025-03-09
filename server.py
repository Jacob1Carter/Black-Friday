# filepath: c:\Users\Jacob\Main\Projects\Python\Black-Friday\server.py
import socket
import time
import sys
print("server.py")

class Server:

    # server settings
    class SERVER_SETTINGS:
        def __init__(self):
            self.MAX_CLIENTS = 4
            self.TICK_RATE = 30
            self.TICK_INTERVAL = 1 / self.TICK_RATE

    def __init__(self):
        self.SERVER_SETTINGS = self.SERVER_SETTINGS()
        # server details
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = ('0.0.0.0', 5011)  # Bind to all available network interfaces
        self.udp_socket.bind(self.server_address)

        # elapsed time counter
        self.start_time = time.time()
        self.elapsed_time = time.time() - self.start_time
        
        # client list
        self.clients = 0
        self.client_addresses = []

        # confirmation message
        print(f"Server started at {self.server_address}")
    
    def receive_messages(self):
        try:
            data, address = self.udp_socket.recvfrom(1024)
            print(f"Received message from {address}: {data.decode()}")
        except socket.timeout:
            pass
        except Exception as e:
            print(f"Error receiving message: {e}")
    
    def exit(self):
        self.udp_socket.close()
        print("Server shutting down.")

def main():
    print("Server is starting...")
    server = Server()
    
    run = True
    while run:
        server.receive_messages()

        server.elapsed_time = time.time() - server.start_time
        time.sleep(max(0, server.SERVER_SETTINGS.TICK_INTERVAL - server.elapsed_time))

    server.exit()

if __name__ == "__main__":
    main()