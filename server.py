import socket
import time
import sys
import struct
from entities import PlayerEntity
from gamehost import Game
from tools import fprint
fprint("server.py")

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
        self.client_addresses = []
        self.clients = len(self.client_addresses)

        # confirmation message
        fprint(f"Server started at {self.server_address}")
    
    def receive_data(self, game=None):
        try:
            data, address = self.udp_socket.recvfrom(1024)
            # fprint(f"Received data of length {len(data)} from {address}")
            if address not in self.client_addresses:
                self.client_addresses.append(address)
                self.clients = len(self.client_addresses)
                fprint(f"New connection from {address}. Total clients: {self.clients}")
            data_type = struct.unpack('!B', data[:1])[0]

            if data_type == 1:  # Key and mouse inputs
                if not game:
                    fprint("Game instance not provided for input handling.")
                    return
                else:
                    expected_size = struct.calcsize('!12H 2H 3B')
                    if len(data[1:]) == expected_size:
                        unpacked_data = struct.unpack('!12H 2H 3B', data[1:])
                        keys = {
                            "w": unpacked_data[0],
                            "a": unpacked_data[1],
                            "s": unpacked_data[2],
                            "d": unpacked_data[3],
                            "SPACE": unpacked_data[4],
                            "SHIFT": unpacked_data[5],
                            "e": unpacked_data[6],
                            "f": unpacked_data[7],
                            "r": unpacked_data[8],
                            "q": unpacked_data[9],
                            "ESC": unpacked_data[10],
                            "CTRL": unpacked_data[11]
                        }
                        mouse_pos = {"x": unpacked_data[12], "y": unpacked_data[13]}
                        mouse_buttons = {
                            "left": unpacked_data[14],
                            "right": unpacked_data[15],
                            "middle": unpacked_data[16],
                        }
                        game.update_entity(address, keys, mouse_buttons, mouse_pos)
                    else:
                        fprint(f"Error: Received data size {len(data[1:])} does not match expected size {expected_size}")

            elif data_type == 2:  # Confirmation message or other simple string
                message_length = struct.unpack('!H', data[1:3])[0]
                if len(data[3:3+message_length]) == message_length:
                    message = data[3:3+message_length].decode('utf-8')
                    if message == "request-server-settings":
                        fprint(f"Received server settings request from {address}")
                        server_data = self.prep_server_data()
                        self.send_data(server_data, client_address=address)
                        fprint(f"Sent server settings to {address}")
                    else:
                        fprint(f"Received message from {address}: {message}")
                else:
                    fprint(f"Error: Received data size {len(data[3:3+message_length])} does not match expected size {message_length}")

            else:
                fprint(f"Unknown data type received from {address}")

        except socket.timeout:
            pass
        except Exception as e:
            fprint(f"Error receiving message: {e}")

    def prep_server_data(self):
        # Prepare data about the server to send to the client using self.SERVER_SETTINGS
        data_type = 0  # Server data type
        max_clients = self.SERVER_SETTINGS.MAX_CLIENTS
        tick_rate = self.SERVER_SETTINGS.TICK_RATE
        data = struct.pack('!B I f', data_type, max_clients, tick_rate)
        return data

    def prep_entity_data(self, game):
        """
        Prepares entity data to send to the client in the new format.
        """
        entities = game.entities
        entity_data = struct.pack('!I', len(entities))  # Include the number of entities
    
        for entity in entities:
            # Ensure the image string is no more than 32 characters
            sprite = entity.image[:32]
            sprite_encoded = sprite.encode('utf-8')
            sprite_length = len(sprite_encoded)
    
            # Ensure entity.id is a string IP address
            if isinstance(entity.id, tuple):
                ip_address = entity.id[0]  # Extract the IP address from the tuple
            else:
                ip_address = entity.id
    
            # Pack the entity data
            entity_data += struct.pack(
                f'!4s H {sprite_length}s I I f f f',
                socket.inet_aton(ip_address),  # Convert IP address to 4-byte binary format
                sprite_length,
                sprite_encoded,
                entity.width,
                entity.height,
                entity.angle,
                entity.x,
                entity.y
            )
    
        return entity_data

    def prep_player_data(self, client):
        # Prepare data about a client to send to the client
        player_data = {
            "x": 50.0,
            "y": 75.0,
            "angle": 0.0,
            "scale": 1.0,
            "health": 100,
            "ability_1_cooldown": 5.0
        }
        data = struct.pack(
            '!f f f f I f',
            player_data["x"],
            player_data["y"],
            player_data["angle"],
            player_data["scale"],
            player_data["health"],
            player_data["ability_1_cooldown"]
        )
        return data

    def send_tick_data(self, game):
        # Prepare data to send to the client about the game state
        data_type = 1  # Tick data type
        entity_data = self.prep_entity_data(game)
        for client_addr in self.client_addresses:
            player_data = self.prep_player_data(client=client_addr)
            total_data = struct.pack('!B', data_type) + entity_data + player_data
            total_data_length = len(total_data)
            self.send_data(total_data, client_address=client_addr)

    def send_data(self, data, client_address=None):
        self.udp_socket.sendto(data, client_address or self.server_address)
        # fprint(f"Sent data of length {len(data)} to {client_address or 'all clients'}")

    def exit(self):
        self.udp_socket.close()
        fprint("Server shutting down.")


def main():
    fprint("Server is starting...")
    server = Server()
    game = Game()
    
    run = True
    while run:
        server.receive_data()

        for client in server.client_addresses:
            safe = False
            for entity in game.entities:
                if entity.id == client:
                    safe = True
                    break
            if not safe:
                game.entities.append(PlayerEntity(client))
        
        server.send_tick_data(game)
        
        server.elapsed_time = time.time() - server.start_time

        time.sleep(max(0, server.SERVER_SETTINGS.TICK_INTERVAL - server.elapsed_time % server.SERVER_SETTINGS.TICK_INTERVAL))
    
    server.exit()


if __name__ == "__main__":
    main()