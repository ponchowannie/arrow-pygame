import pygame
import random
from .constants import *
from core.game_object import GameObject

class Gate(GameObject):
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)

    def __init__(self, side, pair_id):
        super().__init__(base_width=80, base_height=40, start_position=Gate.__startPosition, base_movement_speed=0.3)
        self.side = side
        self.value = random.randint(-10, 10)  # Random value to display
        self.pair_id = pair_id  # Identifier for the gate pair
        self.collected = False  # Track if this gate has been collected
        self.update_position()

    def update_position(self, power=1.5):
        super().update_position(power)

        # Update x position to keep the appropriate side touching the center line
        if self.side == "LEFT":
            self.x = self.center_x - self.width  # Right side touches center
        else:  # RIGHT
            self.x = self.center_x  # Left side touches center

    def draw(self, screen):
        # Create a surface for the transparent rectangle
        gate_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Choose colors based on collected status
        fill_color = TRANSPARENT_GREY if self.collected else TRANSPARENT_BLUE
        outline_color = NEON_GREY if self.collected else NEON_BLUE

        # Draw the transparent fill
        pygame.draw.rect(gate_surface, fill_color, (0, 0, self.width, self.height))

        # Draw the neon outline
        outline_width = 3
        pygame.draw.rect(gate_surface, outline_color, (0, 0, self.width, self.height), outline_width)

        # Draw the transparent surface
        screen.blit(gate_surface, (self.x, self.y - self.height // 2))

        # Draw the value text in white for better contrast against the neon
        self.draw_text(screen, self.value, WHITE, (self.x + self.width // 2, self.y))