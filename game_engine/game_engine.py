"""
TODO:
    Player (snake)
        can bite other player tail make them shoter and decrease score
    Object (apple)
        normal_apple: coin 
        special_apple: can shoot lazer from the eyes

    Game components:
        Game State:
            Waiting  
            Playing
            Dead
            END
        Scoreboard 
"""
from player import Snake

class Game:
    # Constant Value
    WIDTH, HEIGHT = 1200, 750 

    def __init__(self) -> None:
        self.player1 = Snake()