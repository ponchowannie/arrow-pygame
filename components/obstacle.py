import pygame
import random
from .constants import *
from core.game_object import GameObject

pygame.font.init() # Font initialize to make pygame.font.SysFont work

OBSTACLE_IMAGE = pygame.image.load('./components/images/cowboy.png') # Use sample downloaded monster
FONT = pygame.font.SysFont('Arial', 18, True)

class Obstacle(GameObject):
    __base_width = 30
    __base_height = 30
    __startY = 290 - __base_height // 2
    __startX = WINDOW_WIDTH // 2 + 5

    def __init__(self, pos):
        super().__init__(base_width=Obstacle.__base_width, base_height=Obstacle.__base_height, 
                         start_position=(Obstacle.__startX, Obstacle.__startY), base_movement_speed=0.3)
        
        self.obs_health = random.randint(1, 10)  # Health 1-10
        self.damage = self.obs_health  # Damage same as obstacle health
        self.original_image = pygame.transform.scale(OBSTACLE_IMAGE, (self.base_width, self.base_height))
        self.image = self.original_image

        self.pos = pos  # Random spawn position (0, 1, 2, or 3)

        self.x_offset = [-50, -15, 15, 50]  # Random x variation for movement
        self.update_object()

    def update_object(self):
        super().update_position()
        super().update_size(power=1.1)  # Increase size

        # Set x and y based on the position chosen
        spread_multiplier = 1.5
        self.x = self.center_x + int(self.x_offset[self.pos] * self.distance * spread_multiplier)

        # Adjust y as well to simulate movement
        self.y = Obstacle.__startY + (self.y - Obstacle.__startY)
        self.distance += 0.01

        # Ensure the image size is updated with the new size
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def draw(self, screen):
        # Draw the image of the obstacle at the updated position
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        
        # Optionally, draw the damage text above the obstacle for clarity
        damage_text = FONT.render(f"-{self.damage}", True, (255, 0, 0))
        screen.blit(damage_text, (self.x - damage_text.get_width() // 2, self.y - self.height // 2 - 20))

    def get_rect(self):
        # Make sure the hitbox is properly aligned with the obstacle's position and size
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)