import pygame

class PlayerGraphicBasic:
    def __init__(self, chain_position: list[tuple[float, float, float]], screen: pygame.Surface, color: str = "aliceblue") -> None:        
        self.screen = screen
        self.skeleton = chain_position
        self.color = color

    def body_draw(self):
        for bone in self.skeleton:
            pygame.draw.circle(surface=self.screen, color=self.color, center=(bone[0], bone[1]), radius=bone[2])

        

class Fruits:
    def __init__(self, positions: list[tuple[float, float]], screen: pygame.Surface) -> None:
        self.positions = positions
        self.screen = screen

    def body_draw(self, radius:float = 10) -> None:
        for fruit_pos in self.positions:
            pygame.draw.circle(surface=self.screen, color="darkgoldenrod1", center=fruit_pos, radius=radius)

class GameEngine:
    def __init__(self, screen_size: tuple[int, int]) -> None:
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(screen_size)
        self.player_lst = []
        self.fruits = None

    def reg_players(self, player_lst: list[PlayerGraphicBasic]) -> None:
        self.player_lst = player_lst

    def reg_fruits(self, fruit_lst: Fruits) -> None:
        self.fruits = fruit_lst

    def run(self) -> None:
        running = True
        while running:
            self.screen.fill("black")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for player in self.player_lst:
                player.body_draw()
            
            if self.fruits:
                self.fruits.body_draw()



            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit() 

if __name__ == "__main__":
    GAME = GameEngine((800,600))

    EXAMPLE_CHAIN = [(100, 150, 50), (200, 170, 45), (300, 180, 35), (400, 200, 20)]
    PLAYER1 = PlayerGraphicBasic(EXAMPLE_CHAIN, GAME.screen)
    PLAYER_LST = [PLAYER1]
    FRUITS_LST = Fruits([(6, 9), (20, 12), (32, 64), (100, 200)], GAME.screen)

    GAME.reg_players(PLAYER_LST)
    GAME.reg_fruits(FRUITS_LST)

    GAME.run()
