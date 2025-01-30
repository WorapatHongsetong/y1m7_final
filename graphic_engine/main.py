import pygame
import math

def bezier(points, num_points=100):
    n = len(points) - 1
    curve_points = []
    for t in range(num_points + 1):
        t /= num_points
        x = sum(
            points[i][0] * (1 - t) ** (n - i) * t ** i * math.comb(n, i)
            for i in range(n + 1)
        )
        y = sum(
            points[i][1] * (1 - t) ** (n - i) * t ** i * math.comb(n, i)
            for i in range(n + 1)
        )
        curve_points.append((x, y))
    return curve_points

class PlayerGraphicBasic:
    def __init__(self, chain_position: list[tuple[float, float, float]], screen: pygame.Surface, color: str = "aliceblue") -> None:        
        self.screen = screen
        self.skeleton = chain_position
        self.color = color

    def body_draw(self):
        skeleton_vectors = []
        left_bones = []
        right_bones = []
        for i, bone in enumerate(self.skeleton):
            pygame.draw.circle(surface=self.screen, color=self.color, center=(bone[0], bone[1]), radius=bone[2])
            pygame.draw.circle(surface=self.screen, color="black", center=(bone[0], bone[1]), radius=bone[2] - 1)

            if i <= len(self.skeleton) - 2:
                direction = math.atan(self.skeleton[i+1][1] - bone[1])/(self.skeleton[i+1][0])

            bone_left = (math.cos(direction + math.pi/2) * bone[2] + bone[0],
                         math.sin(direction + math.pi/2) * bone[2] + bone[1])
            left_bones.append(bone_left)
            bone_right = (math.cos(direction - math.pi/2) * bone[2] + bone[0],
                          math.sin(direction - math.pi/2) * bone[2] + bone[1])
            right_bones.append(bone_right)

        left_bones = bezier(left_bones)
        right_bones = bezier(right_bones)
        right_bones.reverse()

        pygame.draw.lines(surface=self.screen, color=self.color , closed=True, points=left_bones + right_bones)
        # pygame.draw.lines(surface=self.screen, color=self.color , closed=False, points=right_bones)
        pygame.draw.circle(surface=self.screen, color="white", center=left_bones[0], radius=15)
        pygame.draw.circle(surface=self.screen, color="white", center=right_bones[-1], radius=15)
        pygame.draw.circle(surface=self.screen, color="black", center=left_bones[0], radius=10)
        pygame.draw.circle(surface=self.screen, color="black", center=right_bones[-1], radius=10)


        

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
    FRUITS_LST = Fruits([(6, 9), (20, 12), (32, 64)], GAME.screen)

    GAME.reg_players(PLAYER_LST)
    GAME.reg_fruits(FRUITS_LST)

    GAME.run()
