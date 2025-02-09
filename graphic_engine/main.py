import pygame
import math
import pprint

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
        # self.name = chain_position[0]
        self.skeleton = chain_position
        # self.color = chain_position[2][0]
        # self.score = chain_position[3]
        # print(self.skeleton)

    def body_draw(self, color):
        self.color = color
        skeleton_vectors = []
        left_bones = []
        right_bones = []
        for i, bone in enumerate(self.skeleton):
            print(bone)
            bone = [bone[0][0], bone[0][1], bone[1]]
            # pygame.draw.circle(surface=self.screen, color=self.color, center=(bone[0], bone[1]), radius=bone[2])
            # pygame.draw.circle(surface=self.screen, color="black", center=(bone[0], bone[1]), radius=bone[2] - 1)

            if i == 0:
                if self.skeleton[1][0][0]-bone[0] == 0:
                    direction = math.pi/2
                else:
                    direction = math.atan2((self.skeleton[1][0][1]-bone[1]), (self.skeleton[1][0][0]-bone[0]))
                pygame.draw.line(surface=self.screen, color="white", start_pos=self.skeleton[1][0], end_pos=(bone[0], bone[1]), width=4)

            if i <= len(self.skeleton) - 2:
                if (self.skeleton[i+1][0][0]-bone[1]) == 0:
                    direction = math.pi/2
                else:
                    direction = math.atan2((self.skeleton[i+1][0][1] - bone[0]), (self.skeleton[i+1][0][0]-bone[1]))

            bone_left = (-math.cos(direction + math.pi/2) * bone[2] + bone[0],
                         -math.sin(direction + math.pi/2) * bone[2] + bone[1])
            left_bones.append(bone_left)
            bone_right = (-math.cos(direction - math.pi/2) * bone[2] + bone[0],
                          -math.sin(direction - math.pi/2) * bone[2] + bone[1])
            right_bones.append(bone_right)

        left_bones_b = bezier(left_bones)
        right_bones_b = bezier(right_bones)

        # for point in left_bones_b + right_bones_b:
        #     pygame.draw.circle(surface=self.screen, color="white", center=point, radius=5)

        pygame.draw.lines(surface=self.screen, color=self.color , closed=False, points=left_bones_b, width=5)
        pygame.draw.lines(surface=self.screen, color=self.color , closed=False, points=right_bones_b, width=5)
        # pygame.draw.lines(surface=self.screen, color=self.color , closed=False, points=left_bones, width=5)
        # pygame.draw.lines(surface=self.screen, color=self.color , closed=False, points=right_bones, width=5)
        pygame.draw.circle(surface=self.screen, color="white", center=left_bones[1], radius=11)
        pygame.draw.circle(surface=self.screen, color="white", center=right_bones[1], radius=11)
        pygame.draw.circle(surface=self.screen, color="black", center=left_bones[1], radius=6)
        pygame.draw.circle(surface=self.screen, color="black", center=right_bones[1], radius=6)


        

class Fruits:
    def __init__(self, positions: list[tuple[float, float]], screen: pygame.Surface) -> None:
        self.positions = positions
        self.screen = screen

    def body_draw(self, radius:float = 10) -> None:
        for fruit_pos in self.positions:
            pygame.draw.circle(surface=self.screen, color="darkgoldenrod1", center=fruit_pos, radius=radius)

class GraphicEngine:
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

    def update(self) -> None:
        running = True
        while running:
            self.screen.fill("white")

            for player in self.playerblack:
                player.body_draw()
            
            if self.fruits:
                self.fruits.body_draw()



            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit() 

def extract_json(json_data: dict, screen: pygame.surface):
    DATA = json_data
    pprint.pprint(DATA)
    print(type(DATA))
    game_leader_board = DATA.get("game")
    print("113", type(game_leader_board))
    game_leader_board = game_leader_board.get("leaderboard")
    game_state = DATA.get("game").get("state")

    players_lst = []
    for player in DATA.get("players"):
        p1 = DATA.get("players")
        players_lst.append(PlayerGraphicBasic([p1.get(player).get("name"), p1.get(player).get("segments"),p1.get(player).get("color"),p1.get(player).get("score")],
                                              screen=screen))
    fruit_pos = DATA.get("fruits").get("position")

    return game_state, game_leader_board, players_lst, fruit_pos

if __name__ == "__main__":
    GAME = GraphicEngine((800,600))

    EXAMPLE_CHAIN = [(100, 150, 50), (200, 170, 45), (300, 180, 35), (400, 200, 20)]
    PLAYER1 = PlayerGraphicBasic(EXAMPLE_CHAIN, GAME.screen)
    PLAYER_LST = [PLAYER1]
    FRUITS_LST = Fruits([(6, 9), (20, 12), (32, 64)], GAME.screen)

    GAME.reg_players(PLAYER_LST)
    GAME.reg_fruits(FRUITS_LST)

    GAME.run()
