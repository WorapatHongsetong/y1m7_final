import socket
import threading
import json
import pygame
import logging
from logging.handlers import RotatingFileHandler

# DEBUG
from pprint import pprint

log_directory = "./logs"
log_file = "client.log"
max_log_size = 1 * 1024 * 1024

logger = logging.getLogger("GameClientLogger")
logger.setLevel(logging.DEBUG)

log_file_path = log_directory + "/" + log_file
handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


class Client:
    def __init__(self, name: str, id: int) -> None:
        self.id = id
        self.name = name


class MainGame:
    HOST = '127.0.0.1'
    PORT = 5505

    def __init__(self) -> None:
        pygame.init()

        self.connecting_status = True
        self.is_first_join = True
        self.share_data = {}
        self.ready_get_id = threading.Event()

        self.client = None

    def send_message(self, server_socket: socket.socket) -> None:
        """ send a message to server """

        try:
            while self.connecting_status:
                mouse_pos = pygame.mouse.get_pos()
                keys = pygame.key.get_pressed()
                key_data = {}

                if key_data:  # If there's any key pressed
                    data = {
                        'id': self.client.id,
                        "name": self.client.name,
                        "input": {
                            "keyboard_input": key_data['key'],
                            "mouse_pos": mouse_pos
                        }
                    }
                    server_socket.sendall((json.dumps(data) + "\n").encode())
                pygame.time.delay(100)  # Small delay to reduce network load

        except Exception as e:
            print(f"Error in send_key_presses: {e}")
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
                                self.client = Client(json_data.get("id"))
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

                        except json.JSONDecodeError as e:
                            logger.error("Failed to decode JSON: %s, message: %s", e, json_message)

        except (ConnectionAbortedError, OSError):
            logger.info("Socket Closed")

        finally:
            self.connecting_status = False
            logger.info("Existing Client...")

    def run_game(self) -> None:
        pass

    def connect_to_server(self) -> None:
        """ Open socket to connect the server """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((self.HOST, self.PORT))
            print("Connected to server")
            
            name = input("Enter the name:")

            # Thread for send a message
            send_thread = threading.Thread(
                target=self.send_message, args=(sock,))
            receive_thread = threading.Thread(
                target=self.receive_data, args=(sock,))

            # start Thread
            send_thread.start()
            receive_thread.start()

            # main_game
            self.run_game()

        print("Client Closed")


if __name__ == "__main__":
    game = MainGame()
    game.connect_to_server()
