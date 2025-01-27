import numpy as np
from typing import Tuple
import logging
import pygame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Snake:
    def __init__(self, head: Tuple[int, int], segment_num: int=7) -> None:
        self.head = head
        self.segment = segment_num

############### Implement simple procedural animation ##############
class Testing:
    WIDTH, HEIGHT = 800, 600
    SEGMENT_RADIUS = 50

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.head = pygame.Vector2(self.WIDTH // 2, self.HEIGHT // 2)  # Fixed point
        self.segment = [pygame.Vector2(0, 0) for _ in range(5)]

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the position of point_b and maintain the distance
            self.maintain_distance()

            # Render everything
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def draw(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (int(self.head.x), int(self.head.y)), radius=10)

    def maintain_distance(self):
        mouse_pos = pygame.mouse.get_pos() 
        self.head = pygame.Vector2(mouse_pos[0], mouse_pos[1])  
        
        for i in range(len(self.segment)):
            pass

    def maintain_point(self, point1: pygame.Vector2, point2: pygame.Vector2) -> pygame.Vector2:
        dx, dy = point2.x - point1.x, point2.y - point1.y
        current_distance = np.sqrt(dx**2 + dy**2)

        if current_distance != self.SEGMENT_RADIUS:
            scale = self.SEGMENT_RADIUS / current_distance  
            point2.x = point1.x + dx * scale
            point2.y = point1.y + dy * scale

        return point2

if __name__ == "__main__":
    test = Testing()
    test.run()