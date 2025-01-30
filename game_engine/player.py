import numpy as np
from typing import Tuple, List, Union, Self
import logging
import pygame
from game_engine.apple import Apple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class Snake:
    # Constant value
    SEGMENT_SPACE = 20
    MAX_BODY_TURN = np.radians(60)

    def __init__(self,
                 head: List[int],
                 segment_num: int = 3,
                 velocity: Union[int, float] = 5,
                 name: str="player") -> None:
        self.head = head
        self.segment = [[head[0], head[1]-i*self.SEGMENT_SPACE] for i in range(1, segment_num)]
        self.segment_raduis = [max(20-i, 5) for i in range(segment_num+1)]

        self.velocity = velocity
        self.direction_to_target = [0, 0]
        self.heading_vector = [self.head[0],
                               self.head[0] + self.segment_raduis[0]]
        
        self.name = name
        self.status = "NORMAL"
        
        self.score = 0
        self.grow_thershold = 30

    def maintain_point(self,
                       point1: List[int],
                       point2: List[int],
                       prev_angle: float = None) -> List[int]:

        dx, dy = point2[0] - point1[0], point2[1] - point1[1]
        current_distance = np.hypot(dx, dy) 

        if current_distance != self.SEGMENT_SPACE:
            scale = self.SEGMENT_SPACE / current_distance
            dx *= scale
            dy *= scale

            if prev_angle is not None:
                current_angle = np.arctan2(dy, dx)
                angle_diff = current_angle - prev_angle

                angle_diff = (angle_diff + np.pi) % (2 * np.pi) - np.pi

                if abs(angle_diff) > self.MAX_BODY_TURN:
                    angle_diff = np.clip(
                        angle_diff, -self.MAX_BODY_TURN, self.MAX_BODY_TURN)
                    current_angle = prev_angle + angle_diff

                    dx = np.cos(current_angle) * self.SEGMENT_SPACE
                    dy = np.sin(current_angle) * self.SEGMENT_SPACE

            point2[0] = point1[0] + dx
            point2[1] = point1[1] + dy
        return point2, np.arctan2(dy, dx)

    def maintain_distance(self) -> None:
        self.segment[0], prev_angle = self.maintain_point(
            self.head, self.segment[0])

        for i in range(1, len(self.segment)):
            self.segment[i], prev_angle = self.maintain_point(
                self.segment[i-1], self.segment[i], prev_angle)

    def rotation_points(self, angle: int | float) -> None:
        vector = self.heading_vector

        # Change theta_1 to radians
        # and intialize rotate matrix
        theta_1 = np.radians(angle)
        rotate_matrix = [
            [np.cos(theta_1), -np.sin(theta_1)],
            [np.sin(theta_1), np.cos(theta_1)]
        ]

        new_point = [0, 0]
        for i in range(2):
            res = 0
            for j in range(2):
                res += rotate_matrix[i][j] * vector[j]
            new_point[i] = res

        self.heading_vector = new_point

    def move_forward(self) -> None:
        angle = np.atan2(self.heading_vector[1], self.heading_vector[0])
        move_x = self.velocity * np.cos(angle)
        move_y = self.velocity * np.sin(angle)

        new_point = (self.head[0] + move_x, self.head[1] + move_y)
        self.head = new_point

    def rotate_to_target(self, target: List[int]) -> None:

        v_head_t = [
            target[0] - self.head[0],
            target[1] - self.head[1]
        ]

        vector_angle = np.atan2(self.heading_vector[1], self.heading_vector[0])
        target_angle = np.atan2(v_head_t[1], v_head_t[0])
        diff_angle = target_angle - vector_angle

        max_turn_rate = 0.5

        if diff_angle > np.pi:
            diff_angle -= 2 * np.pi
        elif diff_angle < -np.pi:
            diff_angle += 2 * np.pi

        if abs(diff_angle) > max_turn_rate:
            diff_angle = max_turn_rate if diff_angle > 0 else -max_turn_rate

        self.rotation_points(np.degrees(diff_angle))

    def shorten_tail(self) -> None:
        if len(self.segment) > 3:
            self.segment.pop()
            self.segment_raduis.pop()
            self.score -= 30

    def check_collision_with(self, other: Union[Apple, Self]) -> bool:
        head_x, head_y = self.head
        x, y = None, None

        if isinstance(other, Apple):
            x, y = other.get_position()
            radius = other.get_radius()
            
        elif isinstance(other, Snake):
            x, y = other.get_segment_postion()[-1]
            radius = other.get_segment_radius()[-1]

        if x and y:
            distance = np.hypot((head_x - x), (head_y - y))
            return distance < radius + self.segment_raduis[0]
        return False

    def calculate_segment_radius(self, index: int) -> None:
        head_radius = 20  
        radius_decrement = 1 
        return max(head_radius - index * radius_decrement, 5) 

    def grow(self) -> None:
        if self.score >= self.grow_thershold:
            self.grow_thershold += 30

            last_segment = self.segment[-1]
            new_segment = [last_segment[0] - self.SEGMENT_SPACE, last_segment[1]]
            
            self.segment.append(new_segment)
            self.segment_raduis.append(self.calculate_segment_radius(len(self.segment)))

            self.grow() 

    # Update part
    def update_score(self, score: int) -> None:
        self.score += score

    # Set part
    def set_head(self, pos: List[int]) -> None:
        self.head = pos        
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def set_status(self, status:str) -> None:
        self.status = status
    
    # Access part
    def get_segment_postion(self) -> List[List[int]]:
        return [self.head] + self.segment

    def get_segment_radius(self) -> List[int]:
        return self.segment_raduis

    def get_direction(self,
                      other: Union[List[int], Tuple[int, int]]) -> Tuple[int, int]:
        return [other[0] - self.head[0], other[1] - self.head[1]]
    
    def get_score(self) -> int:
        return self.score

    def get_name(self) -> str:
        return self.name

    def get_status(self) -> str:
        return self.status
############### Testing Implement simple procedural animation ##############


class Testing:
    WIDTH, HEIGHT = 1200, 750 

    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.clock = pygame.time.Clock()

        self.player = Snake(
            head=(self.WIDTH//2, self.HEIGHT//2),
            segment_num=20
        )

    def run(self) -> None:
        running = True
        prev_time = 0
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            mouse_pos = pygame.mouse.get_pos()
            self.player.move_forward()
            self.player.rotate_to_target(mouse_pos)
            self.player.maintain_distance()
          
            # Render everything
            self.screen.fill((0, 0, 0))
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

        pygame.quit()

    def draw(self):
        segment_position = self.player.get_segment_postion()
        segment_radius = self.player.get_segment_radius()

        for i in range(len(segment_radius)):
            pygame.draw.circle(self.screen,
                               (0, 255, 0),
                               ((int(segment_position[i][0]), int(
                                   segment_position[i][1]))),
                               radius=segment_radius[i])

import time
if __name__ == "__main__":
    test = Testing()
    test.run()
    
    # Test grow
