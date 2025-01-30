import socket
import json
import threading
from math import pi
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
                                  mode="a",
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

    def update_user(self, data: dict) -> None:
        try:
            json_form = json.dumps(data)
            self.client_socket.sendall((json_form + '\n').encode())

        except Exception as e:
            logging.error("error to update user: %s", e)


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

        self.lock = threading.Lock()

        self.game = Game()

    def broadcast(self) -> None:
        """ Update to every player """

        while True:
            with self.lock:

                # get user_input from queue
                while not self.input_queue.empty():
                    user_input = self.input_queue.get()

                for id in list(self.clients.keys()):
                    # Safely get the client object
                    client = self.clients.get(id)
                    if not client:
                        continue

                    # Wait untill player got an ID
                    if not client.ready_event.is_set():
                        continue

                    try:
                        client.update_user(self.game_state)
                        logger.info("Send game_state to player")

                    except Exception as e:
                        print(f"error broadcasting to {id}: {e}")
                        logger.error("error broadcastring to %d: %s", id, e)

                        # Handle if client not appear in clients
                        if id in self.clients:
                            self.clients.pop(id)
                            client.client_socket.close()
            threading.Event().wait(0.016)

    def handle_client(self, client: Client) -> None:
        """ Handle data from each client """
        try:
            # send player an id
            id_dict = {"id": client.id}
            client.client_socket.send(
                (json.dumps(id_dict) + '\n').encode('utf-8'))

            client.ready_event.set()  # Send signal to be ready

            while True:
                buffer = b""

                # receiving user input
                while True:
                    data = client.client_socket.recv(32)

                    # receive data as bytes
                    if data:
                        buffer += data

                        if buffer.endswith(b'\n'):
                            break
                    else:
                        print(f"{client.id} has disconnected")
                        logger.info("%s has disconnected", args=(client.id))
                        raise ConnectionError

                # When we have recieved some data
                if buffer:
                    try:
                        # Update data of Client
                        print(f"Upddating player {client.id}'s data")  # DEBUG
                        # client.client_socket.send("Data recieved".encode()) # DEBUG

                        json_data = json.loads(buffer.strip())
                        # put user input to queue
                        self.input_queue.put(json_data)
                        logger.info("Received data from %s: %s",
                                    client.id, json_data)

                        # DEBUG
                        print(f"Player {client.id}'s data updated")

                    except json.JSONDecodeError as e:
                        print(f"Error to decode JSON data: {e}")
                        logger.error("Error to decode JSON data: %s", e)

        except ConnectionError:
            # Show on the server and send it to everyone
            print(f"{client.id} left the game!")
            logger.info("%s left the game", client.id)

        finally:
            # clear and remove everything
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
