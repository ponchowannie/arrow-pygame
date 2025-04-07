import pygame
import random
from .constants import *

class Gate:
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)

    def __init__(self, side, pair_id):
        self.distance = 0  # Distance from player (0 to 1)
        self.base_width = 80
        self.base_height = 40
        self.side = side
        self.center_x = Gate.__startPosition[0]
        self.x = Gate.__startPosition[0]
        self.y = Gate.__startPosition[1]
        self.base_movement_speed = 0.3
        self.value = random.randint(-10, 10)  # Random value to display
        self.font = pygame.font.Font(None, 36)  # Font for text
        self.pair_id = pair_id  # Identifier for the gate pair
        self.collected = False  # Track if this gate has been collected
        self.update_position()

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height//2, 
                         self.width, self.height)

    def update_position(self):
        # Use power-based scaling for smoother size increase
        power = 1.5  # Adjust this value for more realistic scaling
        scale_factor = 1 + (self.distance ** power)
        self.width = self.base_width * scale_factor
        self.height = self.base_height * scale_factor

        # Update x position to keep the appropriate side touching the center line
        if self.side == "LEFT":
            self.x = self.center_x - self.width  # Right side touches center
        else:  # RIGHT
            self.x = self.center_x  # Left side touches center

        # Scale movement speed with distance (faster as it gets closer)
        self.y += (self.base_movement_speed * (1 + self.distance)) * 2

    def draw(self, screen):
        # Create a surface for the transparent rectangle
        gate_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Choose colors based on collected status
        fill_color = TRANSPARENT_GREY if self.collected else TRANSPARENT_BLUE
        outline_color = NEON_GREY if self.collected else NEON_BLUE
        
        # Draw the transparent fill
        pygame.draw.rect(gate_surface, fill_color, 
                        (0, 0, self.width, self.height))
        
        # Draw the neon outline
        outline_width = 3
        pygame.draw.rect(gate_surface, outline_color, 
                        (0, 0, self.width, self.height), outline_width)
        
        # Draw the transparent surface
        screen.blit(gate_surface, 
                   (self.x, self.y - self.height//2))
        
        # Draw the value text in white for better contrast against the neon
        text = self.font.render(str(self.value), True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y))
        screen.blit(text, text_rect)