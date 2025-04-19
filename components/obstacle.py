import pygame
import random
from .constants import *
from core.game_object import GameObject

pygame.font.init() # Font initialize to make pygame.font.SysFont work

OBSTACLE_IMAGE = pygame.image.load('./components/images/sample_monster.png') # Use sample downloaded monster
FONT = pygame.font.SysFont('Arial', 18, True)

class Obstacle(GameObject):
    __startY = WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 6 # Adjust where to summon obstacle

    def __init__(self):
        start_x = WINDOW_WIDTH // 2
        super().__init__(base_width=50, base_height=50, start_position=(start_x, Obstacle.__startY), base_movement_speed=0.45)

        self.obs_health = random.randint(1, 10) # Health 1-10
        self.damage = self.obs_health # Damage same as obstacle health
        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.base_width, self.base_height))
        
        self.x_offset = random.randint(-100, 100) # Random x

        self.update_object()

    def update_object(self, power=1.5):
        super().update_position(power)
        super().update_size(power)

        spread_multiplier = 2.5
        self.x = WINDOW_WIDTH // 2 + int(self.x_offset * self.distance * spread_multiplier)

        self.image = pygame.transform.scale(OBSTACLE_IMAGE, (self.width, self.height))

    def draw(self, screen):
        screen.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        damage_text = FONT.render(f"-{self.damage}", True, (255, 0, 0))
        screen.blit(damage_text, (self.x - damage_text.get_width() // 2, self.y - self.height // 2 - 10))

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)