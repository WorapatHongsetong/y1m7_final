import numpy as np
from typing import Tuple, List
import logging
import pygame

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

"""
TODO:
    adding angle constant
    edit the Snake and Testit
"""

class Snake:
    # Constant value
    SEGMENT_SPACE = 20

    def __init__(self, head: List[int], segment_num: int=3) -> None:
        self.head = head
        self.segment = [[0, 0] for _ in range(segment_num)]
        self.segment_raduis = [5-i for i in range(segment_num+1)]

    def maintain_point(self, 
                       point1: List[int], 
                       point2: List[int]) -> List[int]:
        
        dx, dy = point2[0] - point1[0], point2[1] - point1[1]
        current_distance = np.sqrt(dx**2 + dy**2)

        if current_distance != self.SEGMENT_SPACE:
            scale = self.SEGMENT_SPACE / current_distance  
            point2[0] = point1[0] + dx * scale
            point2[1] = point1[1] + dy * scale

        return point2
    
    def maintain_distance(self) -> None:
        self.segment[0] = self.maintain_point(self.head, self.segment[0])
        
        for i in range(1, len(self.segment)):
            self.segment[i] = self.maintain_point(self.segment[i-1], self.segment[i])

    def get_segment_postion(self) -> List[int]:
        pass

    def get_segment_radius(self) -> List[int]:
        return self.segment_raduis

############### Testing Implement simple procedural animation ##############
class Testing:
    WIDTH, HEIGHT = 800, 600
    SEGMENT_RADIUS = 50

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.player = Snake(
            head=(self.WIDTH//2, self.HEIGHT//2)
        )
        

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Update the position of point_b and maintain the distance
            self.player.maintain_distance()

            # Render everything
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def draw(self):
        segment_radius = self.player.get_segment_radius() 
        segment_position = self.player.get_segment_postion()

        for i in range(len(segment_radius)):
            pygame.draw.circle(self.screen, 
                               (0, 255, 0), 
                               ((int(segment_position[i][0]), int(segment_position[i][1]))), 
                               radius=segment_radius[i])

    # def maintain_distance(self):
    #     mouse_pos = pygame.mouse.get_pos() 
    #     self.head = pygame.Vector2(mouse_pos[0], mouse_pos[1])  
        
    #     self.segment[0] = self.maintain_point(self.head, self.segment[0])
        
    #     for i in range(1, len(self.segment)):
    #         self.segment[i] = self.maintain_point(self.segment[i-1], self.segment[i])

    # def maintain_point(self, point1: pygame.Vector2, point2: pygame.Vector2) -> pygame.Vector2:
    #     dx, dy = point2.x - point1.x, point2.y - point1.y
    #     current_distance = np.sqrt(dx**2 + dy**2)

    #     if current_distance != self.SEGMENT_RADIUS:
    #         scale = self.SEGMENT_RADIUS / current_distance  
    #         point2.x = point1.x + dx * scale
    #         point2.y = point1.y + dy * scale

    #     return point2

if __name__ == "__main__":
    test = Testing()
    test.run()