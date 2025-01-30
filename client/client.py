import socket
import threading
import json
import pygame
import logging
from logging.handlers import RotatingFileHandler
from graphic_engine import main as gp

# DEBUG
from pprint import pprint

log_directory = "./logs"
log_file = "client.log"
max_log_size = 1 * 1024 * 1024

logger = logging.getLogger("GameClientLogger")
logger.setLevel(logging.DEBUG)

log_file_path = log_directory + "/" + log_file
handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, mode="w")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class Client:
    def __init__(self, name: str, player_id: int) -> None:
        self.id = player_id 
        self.name = name
    
    def get_id(self) -> int:
        return self.id

    def get_name(self) -> str:
        return self.name


class MainGame:
    HOST = '127.0.0.1'
    PORT = 5505

    def __init__(self) -> None:
        pygame.init()

        self.clock = pygame.time.Clock()

        self.connecting_status = True
        self.is_first_join = True
        self.share_data = {}
        self.ready_get_id = threading.Event()

        self.client = None
        
        self.enter_name = ""

    def send_message(self, server_socket: socket.socket) -> None:
        """ send a message to server """

        try:
            while self.connecting_status:
                mouse_pos = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()
                key_data = {}

                if keys[pygame.K_SPACE]:
                    key_data['key'] = 'space'

                data = {
                    'id': self.client.get_id(),
                    "name": self.client.get_name(),
                    "input": {
                        "keyboard_input": key_data.get('key', None),
                        "mouse_pos": mouse_pos
                    }
                }
                server_socket.sendall((json.dumps(data) + "\n").encode())
                
                self.clock.tick(60)

        except Exception as e:
            logger.error("Error in send_key_presses: %s", e)
            self.connecting_status = False

    def receive_data(self, sock: socket.socket) -> None:
        buffer = bytearray()
        try:
            # receiving messages
            while self.connecting_status:
                message_received = b""
                while True:
                    buffer = sock.recv(32)
                    if buffer:
                        message_received += buffer
                        if message_received.endswith(b"\n"):
                            break
                    else:
                        print("Connection lost!")
                        self.connecting_status = False
                        break
                

                # Process each JSON object separated by '\n'
                for json_message in message_received.split(b"\n"):
                    if json_message.strip():  # Skip empty lines
                        try:
                            json_data = json.loads(json_message)
                            
                            # First join: create a Client object
                            if self.is_first_join:
                                self.client = Client(player_id=json_data.get("id"),
                                                      name=self.enter_name)
                                self.is_first_join = False
                                continue

                            # Update screen data
                            try:
                                self.share_data.update(json_data)

                                # Already get an id
                                if self.ready_get_id.is_set():
                                    continue
                                self.ready_get_id.set()
                            except Exception as e:
                                logger.error("Error updating data: %s", e)
                                logger.info(self.share_data)

                        except json.JSONDecodeError as e:
                            logger.error(
                                "Failed to decode JSON: %s, message: %s", e, json_message)

        except (ConnectionAbortedError, OSError):
            logger.info("Socket Closed")

        finally:
            self.connecting_status = False
            logger.info("Existing Client...")

    def run_game(self) -> None:
        SCREEN = (1200, 750)

        graphic = gp.GraphicEngine(SCREEN)

        running = True
        
        while running:

            game_state, leader_board, player_lst, fruits_lst = gp.extract_json(self.share_data)
            graphic.reg_players(player_lst)
            graphic.reg_fruits(fruits_lst)

            graphic.screen.fill("black")

            for player in graphic.player_lst:
                player.body_draw()
            
            if graphic.fruits:
                graphic.fruits.body_draw()

            pygame.display.flip()
            graphic.clock.tick(60)
        
        pygame.quit()

        

    def connect_to_server(self) -> None:
        """ Open socket to connect the server """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST, self.PORT))
            print("Connected to server")

            self.enter_name = input("Enter the name:")

            # Thread for send a message
            send_thread = threading.Thread(
                target=self.send_message, args=(sock,))
            receive_thread = threading.Thread(
                target=self.receive_data, args=(sock,))

            receive_thread.start()
            while not self.ready_get_id:  
                continue
            send_thread.start()
            
            self.run_game()

        print("Client Closed")


if __name__ == "__main__":
    game = MainGame()
    game.connect_to_server()
