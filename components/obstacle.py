import pygame
import random
from .constants import *

# Load the obstacle image
OBSTACLE_IMAGE = pygame.image.load('./components/images/sample_monster.png')

class Obstacle(pygame.sprite.Sprite):
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)

    def __init__(self):
        self.distance = 0  # Distance from player (0 to 1)
        self.base_width = 50
        self.base_height = 50
        self.center_x = Obstacle.__startPosition[0]
        self.x = random.randint(0, WINDOW_WIDTH)  # Random x position
        self.y = Obstacle.__startPosition[1]
        self.base_movement_speed = 0.45
        self.obs_health = random.randint(1, 10)  # Random health value
        self.font = pygame.font.Font(None, 36)

        # Scale the obstacle image to match the base dimensions
        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.base_width, self.base_height))
        self.update_position()

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)

    def update_position(self):
        # Use power-based scaling for smoother size increase
        power = 1.5  # Adjust this value for more realistic scaling
        scale_factor = 1 + (self.distance ** power)
        self.width = self.base_width * scale_factor
        self.height = self.base_height * scale_factor

        # Scale the image to match the new dimensions
        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.width, self.height))

        # Scale movement speed with distance (faster as it gets closer)
        self.y += (self.base_movement_speed * (1 + self.distance)) * 2

    def draw(self, screen):
        # Draw the obstacle image
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))