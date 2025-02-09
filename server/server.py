import socket
import json
import threading
import queue
from game_engine.game_engine import Game

# DEBUG Tool
from pprint import pprint
import logging
from logging.handlers import RotatingFileHandler

HOST = "0.0.0.0"
PORT = 5505


# logging
logger = logging.getLogger()
filehandler = RotatingFileHandler("./logs/server.log",
                                  mode="w",
                                  maxBytes=1*1024*1024)
filehandler.setLevel(logging.INFO)

# formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
filehandler.setFormatter(formatter)

logger.setLevel(logging.INFO)
logger.addHandler(filehandler)


class Client:
    def __init__(self, client_socket: socket.socket, id: str) -> None:
        self.client_socket = client_socket
        self.id = id
        self.ready_event = threading.Event()

    def send_data(self, data: dict) -> None:
        try:
            json_form = json.dumps(data)
            self.client_socket.sendall((json_form + '\n').encode())

        except Exception as e:
            logging.error("error to send data: %s", e)


class Server():
    MAX_CLIENT_NUMBER = 2
    SCREEN = (1200, 750)

    PLAYER_RADIUS = 50
    PLAYER1_CENTER = (SCREEN[0]//4, SCREEN[1]//2)
    PLAYER2_CENTER = (SCREEN[0] * 3 // 4, SCREEN[1]//2)

    def __init__(self) -> None:
        self.clients = {}
        self.input_queue = queue.Queue()

        self.game_state = {
            "state": 0,
            "players": [],
            "coin_position": []
        }

        self.player_data = {}
        self.fruit_data = {}

        self.lock = threading.Lock()

        self.game_engine = Game()

    def broadcast(self) -> None:
        """ Update to every player """

        while True:
            with self.lock:
                # get user_input from queue
                while not self.input_queue.empty():
                    user_input = self.input_queue.get()
                    self.game_state = self.game_engine.get_game_data()

                    # Waiting
                    if self.game_state.get("game").get("state") == 0:
                        if user_input.get("name"):
                            try:
                                self.game_engine.set_players_name(
                                    name=user_input.get("name"),
                                    player_id=user_input.get("id")
                                )
                            except Exception as e:
                                logger.error("Error to set player name %s", e)

                        if len(self.clients) == 2:
                            self.game_engine.set_state("PLAYING")

                    # Playing
                    elif self.game_state.get("game").get("state") == 1:
                        logger.warning("Game state %s", self.game_state.get("game").get("state"))
                        self.game_engine.playing_state(
                            player_id=user_input.get("id"),
                            player_mouse=user_input.get("input").get("mouse_pos")
                        )

                self.game_engine.update()
                try:
                    data = self.game_engine.get_game_data()
                except Exception as e:
                    logger.error(f"Error getting game data: {e}")
                    continue 
              
                # Sending data part
                for client_id, client in list(self.clients.items()):
                    if client:
                        try:
                            client.send_data(data)
                            logger.info(f"Sent game_state to player {client_id}")
                        except Exception as e:
                            logger.error(f"Error broadcasting to {client_id}: {e}")
                            if client_id in self.clients:
                                self.clients.pop(client_id)
                                try:
                                    client.client_socket.close()
                                except Exception as e:
                                    logger.error(f"Error closing socket for client {client_id}: {e}")
            threading.Event().wait(0.016)

    def handle_client(self, client: Client) -> None:
        """ Handle data from each client """
        try:
            # send player an id
            id_dict = {"id": client.id}
            client.client_socket.send(
                (json.dumps(id_dict) + '\n').encode('utf-8'))

            # recieve data parts
            while True:
                buffer = b""
                while True:
                    data = client.client_socket.recv(32)
                    if data:
                        buffer += data
                        if buffer.endswith(b'\n'):
                            break
                    else:
                        print(f"{client.id} has disconnected")
                        logger.info("%s has disconnected", client.id)
                        raise ConnectionError

                # When we have recieved some data
                if buffer:
                    try:
                        json_data = json.loads(buffer.strip())

                        # put user input to queue
                        self.input_queue.put(json_data)
                        
                        logger.info("Received data from %s: %s",
                                    client.id, json_data)

                    except json.JSONDecodeError as e:
                        logger.error("Error to decode JSON data: %s", e)

        except ConnectionError:
            logger.info("%s left the game", client.id)

        finally:
            with self.lock:
                if client.id in self.clients:
                    self.clients.pop(client.id)
                client.client_socket.close()

    def run_server(self) -> None:
        """ run main server """

        # initial server
        try:
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print("Socket created")
        except OSError as msg:
            server = None
            print(f"Error creating socket: {msg}")
            exit(1)

        try:
            server.bind((HOST, PORT))
            server.listen()
            print(f"Socket bound and server is listening on {HOST}:{PORT}")
        except OSError as msg:
            print(f"Error binding/listening!: {msg}")
            server.close()
            exit(1)

        # main loop
        while True:
            client_socket, client_address = server.accept()

            # Check whether players are full now
            if len(self.clients) >= self.MAX_CLIENT_NUMBER:
                client_socket.send("Server Room is full now".encode())
                client_socket.shutdown(socket.SHUT_RDWR)
                continue

            # add player to list
            id = len(self.clients) + 1
            print(f"players {id} joinned")
            logger.info("%s is joined set to player %s",
                        client_address, id)
            self.clients[id] = Client(client_socket, id)

            # Create new Thread for each player
            client_thread = threading.Thread(
                target=self.handle_client, args=(self.clients[id], ))
            broadcast_thread = threading.Thread(target=self.broadcast)

            broadcast_thread.start()
            client_thread.start()


if __name__ == '__main__':
    server = Server()
    server.run_server()
