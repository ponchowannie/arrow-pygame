import pygame
import pygwidgets
import random
from .constants import *

class Obstacle(pygame.sprite.Sprite):
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)
    OBSTACLE_IMAGE = pygame.image.load('./components/images/sample_monster.png')

    def __init__(self, position):
        self.distance = 0  # Distance from player (0 to 1)
        self.base_width = 40
        self.base_height = 20
        self.position = position # -2 to 2
        self.center_x = Obstacle.__startPosition[0]
        self.x = Obstacle.__startPosition[0]
        self.y = Obstacle.__startPosition[1]
        self.base_movement_speed = 0.3
        self.obs_health = 5 # random.randint(1, 10)
        self.font = pygame.font.Font(None, 36)
        self.update_position()
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height//2, self.width, self.height)
    
    def update_position(self):
        # Use quadratic scaling for smoother size increase
        scale_factor = 1 + (self.distance * self.distance)
        self.width = self.base_width * scale_factor
        self.height = self.base_height * scale_factor
        
        # Update x position to keep the appropriate side touching the center line
        self.x = self.center_x + self.position
            
        # Scale movement speed with distance (faster as it gets closer)
        self.y += (self.base_movement_speed * (1 + self.distance)) * 2
    
    def draw(self, screen):
        self.images = pygwidgets.ImageCollection(screen, (self.x-(self.width/2), self.y), {'obs1':Obstacle.OBSTACLE_IMAGE}, 'obs1')
        self.images.draw()