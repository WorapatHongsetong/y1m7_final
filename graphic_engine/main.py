import pygame

class PlayerGraphicBasic:
    def __init__(self, chain_position: list[tuple[float, float, float]], screen: pygame.Surface) -> None:        
        self.screen = screen
        self.skeleton = chain_position

    def draw(self):
        for bone in self.skeleton:
            pygame.draw.circle(surface=self.screen, color="aliceblue", center=(bone[0], bone[1]), radius=bone[2])

def game_engine(screen_size: tuple[int, int]) -> pygame.Surface:
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    return screen

if __name__ == "__main__":
    EXAMPLE_CHAIN = [(100, 150, 50), (200, 170, 45), (300, 180, 35), (400, 200, 20)]
    SCREEN = game_engine((500, 500))

    player1 = PlayerGraphicBasic(EXAMPLE_CHAIN, SCREEN)
    clock = pygame.time.Clock()

    running = True
    while running:
        SCREEN.fill("black")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player1.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
