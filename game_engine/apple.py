from typing import Tuple


class Apple:
    def __init__(self, position: Tuple[int, int]) -> None:
        self.position = position
        self.score = 3
        self.effect = "NORMAL"
        self.radius = 9 

    def get_score(self) -> int:
        return self.score

    def get_effect(self) -> str:
        return self.effect

    def get_position(self) -> int:
        return self.position

    def get_radius(self) -> int:
        return self.radius


class GoldenApple(Apple):
    # Immortal for a while
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__(position)
        self.score = 10
        self.effect = "GOLDEN"


class LazerApple(Apple):
    def __init__(self, position: Tuple[int, int]) -> None:
        super().__init__(position)
        self.score = 5
        self.effect = "LAZER"
