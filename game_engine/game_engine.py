"""
TODO:
    Player (snake)
        can bite other player tail make them shoter and decrease score
    Object (apple)
        normal_apple: score 
        golden_appel: more score 
        lazer_apple: can shoot lazer from the eyes

    Game components:
        Game State:
            Waiting -> waiting for players ready
            Playing
            Dead
            END
        Scoreboard -> Show player scoreboard
"""
from apple import *
from player import Snake
from enum import Enum
from typing import Dict, Tuple
import time
import numpy as np


class State(Enum):
    WAITING = 0
    PLAYING = 1
    DEAD = 2


class Game:
    # Constant Value
    WIDTH, HEIGHT = 1200, 750
    APPLE_NUMS = 20
    GENERATE_TIME = 10

    def __init__(self) -> None:

        self.ready_status = [False, False]

        self.player1 = Snake(
            head=(self.WIDTH // 2 - 50, self.HEIGHT // 2)
        )

        self.player2 = Snake(
            head=(self.WIDTH // 2 + 50, self.HEIGHT // 2)
        )

        self.game_state = State.WAITING
        self.scoreboard = [0, 0]  # player1, player2

        self.apples = []
        self.prev_generate_time = time.time()

    def waiting_state(self, player1_input: str = None, player2_input: str = None) -> None:
        if self.game_state != State.WAITING:
            return

        # TODO: check player input here
        while self.ready_status != [True, True]:
            if player1_input == "space":
                self.ready_status[0] = True

            if player2_input == "space":
                self.ready_status[1] = True

        self.game_state = State.PLAYING

    def generate_apples(self) -> None:
        current_time = time.time()

        apple_types = [Apple, GoldenApple, LazerApple]
        weight = [0.7, 0.1, 0.2]

        if current_time - self.prev_generate_time >= self.GENERATE_TIME:

            left_apples = self.APPLE_NUMS - len(self.apples)

            if left_apples == 0:
                return

            for _ in range(left_apples):
                random_apple = np.random.choice(apple_types, p=weight)
                rand_x, rand_y = np.random.randint(
                    50, self.WIDTH - 50), np.random.randint(50, self.HEIGHT - 50)
                self.apples.append(random_apple(
                    position=(rand_x, rand_y)
                ))

    def update(self) -> None:
        if self.game_state != State.PLAYING:
            return

        apples = self.apples

        self.player1.move_forward()
        self.player2.move_forward()
        self.player1.maintain_distance()
        self.player2.maintain_distance()

        for i, apple in enumerate(self.apples):
            if self.player1.check_collision_with(apple):
                self.player1.update_score(apple.get_score())
                apples.pop(i)

            if self.player2.check_collision_with(apple):
                self.player2.update_score(apple.get_score())
                apples.pop(i)

        self.apples = apples

        self.scoreboard[0] = self.player1.get_score()
        self.scoreboard[1] = self.player2.get_score()

    def playing_state(self,
                      player1_mouse: Tuple[int, int] = None,
                      player2_mouse: Tuple[int, int] = None) -> None:
        if self.game_state != State.PLAYING:
            return

        # TODO: check collision with an apple
        self.player1.rotate_to_target(player1_mouse)
        self.player2.rotate_to_target(player2_mouse)
        self.update()

    # Access data
    def get_game_state(self) -> Dict:
        data = {
            "game": {
                "leaderboard": [
                    ["player1", self.scoreboard[0]],
                    ["player2", self.scoreboard[1]]
                ],
                "state": self.game_state
            }
        }
        return data

    def get_player_data(self) -> Dict:
        data = {
            "players": {
                "player1": {
                    "segments": zip(self.player1.get_segment_postion(), self.player1.get_segment_radius()),
                    "color": ["blue"] + ["green" for _ in range(len(self.player1.get_segment_postion()))],
                    "score": self.player1.get_score()
                },
                "player2": {
                    "segments": zip(self.player2.get_segment_postion(), self.player2.get_segment_radius()),
                    "color": ["red"] + ["green" for _ in range(len(self.player2.get_segment_postion()))],
                    "score": self.player2.get_score()
                }
            }
        }

        return data

    def get_fruit_data(self) -> Dict:
        position = []

        for apple in self.apples:
            res = []
            res.append(apple.get_position()[0])
            res.append(apple.get_position()[1])
            res.append(apple.get_effect())
            position.append(res)

        data = {
            "friuts": {
                "position": position,
                "score": [apple.get_score() for apple in self.apples]
            }
        }

        return data


if __name__ == "__main__":
    pass
