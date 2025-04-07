import pygame
import random
from .constants import *
from core.game_object import GameObject

# Load the obstacle image
OBSTACLE_IMAGE = pygame.image.load('./components/images/sample_monster.png')

class Obstacle(GameObject):
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)

    def __init__(self):
        super().__init__(base_width=50, base_height=50, start_position=Obstacle.__startPosition, base_movement_speed=0.45)
        self.obs_health = random.randint(1, 10)  # Random health value
        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.base_width, self.base_height))
        self.update_position()

    def update_position(self, power=1.5):
        super().update_position(power)

        # Scale the image to match the new dimensions
        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.width, self.height))

    def draw(self, screen):
        # Draw the obstacle image
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))