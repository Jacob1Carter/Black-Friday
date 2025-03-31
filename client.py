import socket
import time
import sys
import struct
from gameclient import Game
from tools import fprint
fprint("client.py")

class Client:

    class SERVER_SETTINGS:
        def __init__(self, max_clients=4, tick_rate=30):
            self.MAX_CLIENTS = 4
            self.TICK_RATE = 30
            self.TICK_INTERVAL = 1 / self.TICK_RATE

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
        message = f"request-server-settings"
        data = self.prep_single_data(message=message)
        self.send_data(data)
        fprint(f"Sent server settings request to {self.server_address}")
        time.sleep(1)

        self.receive_data()
    
    def prep_single_data(self, message):
        data_type = 2
        message_length = len(message)
        data = struct.pack('!B H', data_type, message_length) + message.encode('utf-8')
        return data

    def prep_tick_data(self, game):
        data_type = 1
        
        data = struct.pack(
            '!B 12H 2H 3B',
            data_type,
            game.inputdata["keys"]["w"],
            game.inputdata["keys"]["a"],
            game.inputdata["keys"]["s"],
            game.inputdata["keys"]["d"],
            game.inputdata["keys"]["SPACE"],
            game.inputdata["keys"]["SHIFT"],
            game.inputdata["keys"]["e"],
            game.inputdata["keys"]["f"],
            game.inputdata["keys"]["r"],
            game.inputdata["keys"]["q"],
            game.inputdata["keys"]["ESC"],
            game.inputdata["keys"]["CTRL"],
            game.inputdata["mouse_pos"]["x"],
            game.inputdata["mouse_pos"]["y"],
            game.inputdata["mouse_buttons"]["left"],
            game.inputdata["mouse_buttons"]["right"],
            game.inputdata["mouse_buttons"]["middle"],
        )
        return data

    def receive_data(self, game=None):
        try:
            data, address = self.udp_socket.recvfrom(1024)
            fprint(f"Received data of length {len(data)} from {address}")
            data_type = struct.unpack('!B', data[:1])[0]

            if data_type == 0:  # Server settings
                expected_size = struct.calcsize('!I f')
                if len(data[1:]) == expected_size:
                    max_clients, tick_rate = struct.unpack('!I f', data[1:])
                    fprint(f"Received server settings")
                    self.SERVER_SETTINGS = self.SERVER_SETTINGS(max_clients=max_clients, tick_rate=tick_rate)
                else:
                    fprint(f"Error: Received data size {len(data[1:])} does not match expected size {expected_size}")

            elif data_type == 1:  # Tick data
                if game is None:
                    fprint("Game instance is not provided for tick data")
                    return
                else:
                    offset = 1
                    num_entities = struct.unpack('!I', data[offset:offset+4])[0]
                    offset += 4
                    entities = []
                    for _ in range(num_entities):
                        # Unpack the entity data in the new format
                        ip_address = socket.inet_ntoa(data[offset:offset+4])  # Convert 4-byte binary IP back to string
                        offset += 4
                        sprite_length = struct.unpack('!H', data[offset:offset+2])[0]
                        offset += 2
                        sprite = struct.unpack(f'!{sprite_length}s', data[offset:offset+sprite_length])[0].decode('utf-8')
                        offset += sprite_length
                        width, height, angle, scale, x, y = struct.unpack('!I I f f f f', data[offset:offset+24])
                        offset += 24
                        entities.append({
                            "id": ip_address,
                            "sprite": sprite,
                            "dimensions": {"width": width, "height": height},
                            "position": {"x": x, "y": y},
                            "scale": scale,
                            "angle": angle
                        })
                    game.entities = entities  # Update the game entities with the received data
                    # fprint(f"Received game state: entities={entities}")
                    # ! We have the data of the entities, now display them

                # Now unpack player data
                expected_size = struct.calcsize('!f f f f I f')
                if len(data[offset:]) == expected_size:
                    player_data = struct.unpack('!f f f f I f', data[offset:])
                    player_info = {
                        "x": player_data[0],
                        "y": player_data[1],
                        "angle": player_data[2],
                        "scale": player_data[3],
                        "health": player_data[4],
                        "ability_1_cooldown": player_data[5]
                    }
                    # fprint(f"Received player data: {player_info}")
                else:
                    fprint(f"Error: Received data size {len(data[offset:])} does not match expected size {expected_size}")

            elif data_type == 2:  # Confirmation message or other simple string
                message_length = struct.unpack('!H', data[1:3])[0]
                if len(data[3:3+message_length]) == message_length:
                    message = data[3:3+message_length].decode('utf-8')
                    fprint(f"Received message from {address}: {message}")
                else:
                    fprint(f"Error: Received data size {len(data[3:3+message_length])} does not match expected size {message_length}")

            else:
                fprint(f"Unknown data type received from {address}")

        except socket.timeout:
            pass
        except Exception as e:
            fprint(f"Error receiving message: {e}")

    def send_data(self, data):
        self.udp_socket.sendto(data, self.server_address)
        fprint(f"Sent data of length {len(data)} to {self.server_address}")

    def exit(self):
        # send disconnection message to server
        message = f"{self.username} is disconnecting"
        data = self.prep_single_data(message=message)
        self.send_data(data)
        fprint("Client shutting down.")

def main(username, ip):
    fprint(f"Client starting with username: {username}, IP: {ip}")
    client = Client(username=username, ip=ip)
    game = Game()

    run = True
    while run:
        
        for event in game.pygame.event.get():
            if event.type == game.pygame.QUIT:
                run = False

        client.receive_data(game)

        game.update()

        client.send_data(client.prep_tick_data(game))
        client.elapsed_time = time.time() - client.start_time

        time.sleep(max(0, client.SERVER_SETTINGS.TICK_INTERVAL - client.elapsed_time % client.SERVER_SETTINGS.TICK_INTERVAL))

    client.exit()
    game.pygame.quit()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        fprint("Invalid data provided.")
        sys.exit(1)
    else:
        main(username=sys.argv[1], ip=sys.argv[2])