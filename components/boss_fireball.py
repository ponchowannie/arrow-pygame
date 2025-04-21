import pygame
from core.game_object import GameObject
from .constants import GAME_SPEED

FIREBALL_IMAGE = pygame.image.load('./components/images/fireball.png')

class BossFireball(GameObject):
    def __init__(self, x, y=0):
        # Initialize the base GameObject with appropriate values
        base_width = 30
        base_height = 30
        start_position = (x, y)
        base_movement_speed = GAME_SPEED + 5
        super().__init__(base_width, base_height, start_position, base_movement_speed)

        # Load and scale the fireball image
        self.image = FIREBALL_IMAGE
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.get_rect()  # Initialize the rect attribute

    def update(self):
        """Update the fireball's position and size."""
        self.y += self.base_movement_speed  # Move the fireball downward
        self.update_size(power=2)  # Update the size based on distance
        self.rect = self.get_rect()  # Ensure the rect is updated with the new position and size

    def draw(self, screen):
        """Draw the fireball on the screen."""
        scaled_image = pygame.transform.scale(self.image, (self.width, self.height))
        screen.blit(scaled_image, (self.x, self.y))

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)
