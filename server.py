import socket
from tools import backup_project


def main(port):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    # Bind the socket to the server address and port
    server_address = ('localhost', port)
    udp_socket.bind(server_address)
    
    print(f"Server started on port {port}... Waiting for clients.")
    
    # Listen for two clients
    clients = 0
    while clients < 2:
        # Wait for a message from a client
        data, address = udp_socket.recvfrom(4096)
        print(f"Received message from {address}: {data.decode()}")
        
        clients += 1
        print(f"Client {clients} connected.")
    
    # Close the socket
    udp_socket.close()
    print("Server shutting down.")


if __name__ == "__main__":
    backup_project()
    main(5001)
