"""
TODO:
    Player (snake)
        can bite other player tail make them shoter and decrease score
        name: 
    Object (apple)
        generate_apples:
        normal_apple: score 
        golden_appel: more score 
        lazer_apple: can shoot lazer from the eyes <-- might not finish

    Game components:
        Game State:
            Waiting -> waiting for players ready
            Playing
            Dead
            END
        Scoreboard -> Show player scoreboard
"""
from game_engine.apple import *
from game_engine.player import Snake
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
    EFFECT_TIME = 5

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
        self.prev_effect_time = [None, None]

    def waiting_state(self,
                      player_input: str = None) -> None:
        if self.game_state != State.WAITING:
            return

        # TODO: check player input here
        if player_input == "space":
            self.game_state = State.PLAYING

    def generate_apples(self) -> None:
        current_time = time.time()

        if current_time - self.prev_generate_time >= self.GENERATE_TIME:
            self.prev_generate_time = current_time

            left_apples = self.APPLE_NUMS - len(self.apples)
            if left_apples <= 0:
                return

            apple_types = [Apple, GoldenApple]
            weight = [0.9, 0.1]

            for _ in range(left_apples):
                random_apple = np.random.choice(apple_types, p=weight)
                rand_x = np.random.randint(50, self.WIDTH - 50)
                rand_y = np.random.randint(50, self.HEIGHT - 50)
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

        current_time = time.time()

        for i in range(2):
            if self.prev_effect_time[i] and current_time - self.prev_effect_time[i] >= self.EFFECT_TIME:
                if i == 0 and self.player1.get_status() != "NORMAL":
                    self.player1.set_status("NORMAL")
                    self.prev_effect_time[i] = current_time

                elif i == 1 and self.player2.get_status() != "NORMAL":
                    self.player2.set_status("NORMAL")
                    self.prev_effect_time[i] = current_time

        for i, apple in enumerate(self.apples):
            if self.player1.check_collision_with(apple):
                if apple.get_effect() == "GOLDEN":
                    self.player1.set_status(apple.get_effect())
                    self.prev_effect_time[0] = time.time()
                self.player1.update_score(apple.get_score())
                apples.pop(i)

            if self.player2.check_collision_with(apple):
                if apple.get_effect() == "GOLDEN":
                    self.player2.set_status(apple.get_effect())
                    self.prev_effect_time[1] = time.time()
                self.player2.update_score(apple.get_score())
                apples.pop(i)

        self.apples = apples

        if self.player1.check_collision_with(self.player2):
            if self.player2.get_status() == "NORMAL":
                self.player2.shorten_tail()
                self.player1.update_score(30)

        if self.player2.check_collision_with(self.player1):
            if self.player1.get_status() == "NORMAL":
                self.player1.shorten_tail()
                self.player2.update_score(30)

        self.scoreboard[0] = self.player1.get_score()
        self.scoreboard[1] = self.player2.get_score()

        self.player1.grow()
        self.player2.grow()

    def playing_state(self,
                      player_id: int,
                      player_input: str) -> None:
        if self.game_state != State.PLAYING:
            return

        self.generate_apples()

        if player_id == 1:
            if player_input == "left":
                self.player1.rotation_points(-5)
            elif player_input == "right":
                self.player1.rotation_points(5)
        elif player_id == 2:
            if player_input == "left":
                self.player2.rotation_points(-5)
            elif player_input == "right":
                self.player2.rotation_points(5)

    def set_players_name(self, player_id: int, name: str) -> None:
        if player_id == 1:
            self.player1.set_name(name)
        if player_id == 2:
            self.player2.set_name(name)

    def set_state(self, state: str) -> None:
        if state == "PLAYING":
            self.game_state = State.PLAYING
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
                    "segments": list(zip(self.player1.get_segment_postion(), self.player1.get_segment_radius())),
                    "color": ["blue"] + ["green" for _ in range(len(self.player1.get_segment_postion()))],
                    "score": self.player1.get_score()
                },
                "player2": {
                    "segments": list(zip(self.player2.get_segment_postion(), self.player2.get_segment_radius())),
                    "color": ["red"] + ["green" for _ in range(len(self.player2.get_segment_postion()))],
                    "score": self.player2.get_score()
                }
            }
        }

        return data

    def get_fruit_data(self) -> Dict:

        data = {
            "fruits": {
                "position": [[apple.get_position()[0], apple.get_position()[1], apple.get_effect()] for apple in self.apples],
                "score": [apple.get_score() for apple in self.apples]
            }
        }

        return data

    def get_game_data(self) -> Dict:
        return {
            "game": {
                "leaderboard": [
                    ["player1", self.scoreboard[0]],
                    ["player2", self.scoreboard[1]]
                ],
                "state": self.game_state.value
            },
            "players": {
                "player1": {
                    "name": self.player1.get_name(),
                    "segments": list(zip(self.player1.get_segment_postion(), self.player1.get_segment_radius())),
                    "color": ["blue"] + ["green"] * (len(self.player1.get_segment_postion()) - 2) + ['orange' if self.player1.get_status() == "NORMAL" else 'green'],
                    "score": self.player1.get_score()
                },
                "player2": {
                    "name": self.player2.get_name(),
                    "segments": list(zip(self.player2.get_segment_postion(), self.player2.get_segment_radius())),
                    "color": ["red"] + ["green"] * (len(self.player2.get_segment_postion()) - 2) + ['orange' if self.player2.get_status() == "NORMAL" else 'green'],
                    "score": self.player2.get_score()
                }
            },
            "fruits": {
                "position": [[apple.get_position()[0], apple.get_position()[1], apple.get_color()] for apple in self.apples],
                "score": [apple.get_score() for apple in self.apples]
            }
        }


if __name__ == "__main__":
    pass
