import pygame
import math

class PlayerGraphicBasic:
    def __init__(self, chain_position: list[tuple[float, float, float]], screen: pygame.Surface, color: str = "aliceblue") -> None:        
        self.screen = screen
        self.skeleton = chain_position
        self.color = color

    def body_draw(self):
        skeleton_vectors = []
        left_vectors = []
        right_vectors = []
        for i, bone in enumerate(self.skeleton):
            pygame.draw.circle(surface=self.screen, color=self.color, center=(bone[0], bone[1]), radius=bone[2])
            print(i)

            if i <= len(self.skeleton) - 2:
                print(i)
                direction = math.atan(self.skeleton[i+1][1] - bone[1])/(self.skeleton[i+1][0])


            bone_left = (math.cos(direction + math.pi/2) * bone[2] + bone[0],
                         math.sin(direction + math.pi/2) * bone[2] + bone[1])
            bone_right = (math.cos(direction - math.pi/2) * bone[2] + bone[0],
                          math.sin(direction - math.pi/2) * bone[2] + bone[1])

            if i >= 1:
                skeleton_vectors.append(((bone[0], bone[1]),(previous_bone[0], previous_bone[1])))
                pygame.draw.line(surface=self.screen, color=self.color, start_pos=previous_bone_left, end_pos=bone_left)
                pygame.draw.line(surface=self.screen, color=self.color, start_pos=previous_bone_right, end_pos=bone_right)
                
                if i == 1:
                    pygame.draw.circle(surface=self.screen, color="white", center=previous_bone_left, radius=15)
                    pygame.draw.circle(surface=self.screen, color="white", center=previous_bone_right, radius=15)
                    pygame.draw.circle(surface=self.screen, color="black", center=previous_bone_left, radius=10)
                    pygame.draw.circle(surface=self.screen, color="black", center=previous_bone_right, radius=10)

            previous_bone = (bone[0], bone[1], bone[2])
            previous_bone_left = (math.cos(direction + math.pi/2) * previous_bone[2] + previous_bone[0],
                                  math.sin(direction + math.pi/2) * previous_bone[2] + previous_bone[1])
            previous_bone_right = (math.cos(direction - math.pi/2) * previous_bone[2] + previous_bone[0],
                                   math.sin(direction - math.pi/2) * previous_bone[2] + previous_bone[1])

            


        

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
