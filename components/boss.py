import pygame
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT
from core.game_object import GameObject

boss_image = pygame.image.load("./components/images/boss.png")

class Boss(GameObject):
    def __init__(self):
        # Initialize the base GameObject with appropriate values
        base_width = boss_image.get_width() * 0.15
        base_height = boss_image.get_height() * 0.15
        start_position = (WINDOW_WIDTH // 2, 290 - base_height)
        base_movement_speed = 2
        super().__init__(base_width, base_height, start_position, base_movement_speed)

        # Load and scale the boss image
        self.image = pygame.transform.scale_by(boss_image, 0.15)
        self.rect = self.get_rect()
        
        # Additional Boss-specific attributes
        self.health = 100  # Boss health
        self.speed = base_movement_speed  # Horizontal movement speed

    def update_object(self):
        # Move horizontally and reverse direction at screen edges
        self.x += self.speed
        if self.x <= 0 or self.x + self.width >= WINDOW_WIDTH:
            self.speed = -self.speed  # Reverse direction

    def draw(self, screen):
        # Update rect position based on x and y
        self.rect = self.get_rect()
        screen.blit(self.image, (self.x, self.y))
        # Always draw the updated health bar
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 10, self.width * (self.health / 100), 5))
        pygame.draw.rect(screen, (255, 0, 0), (self.x + self.width * (self.health / 100), self.y - 10, self.width * (1 - self.health / 100), 5))
