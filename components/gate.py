import pygame
import random
from .constants import *
from core.game_object import GameObject

class Gate(GameObject):
    __base_width = 40
    __base_height = 20
    __startPosition = (WINDOW_WIDTH // 2 + 5, 290 - __base_height // 2)  # Centered horizontally, adjusted vertically

    def __init__(self, side, pair_id):
        super().__init__(base_width=Gate.__base_width, base_height=Gate.__base_height, start_position=Gate.__startPosition, base_movement_speed=0.3)
        self.side = side
        self.operation = random.choice(["ADD", "MULTIPLY"])  # Randomly choose operation
        if self.operation == "ADD":
            self.value = random.randint(1, 10)  # Addition range
        else:  # MULTIPLY
            self.value = random.randint(2, 4)  # Multiplication range
        self.pair_id = pair_id  # Identifier for the gate pair
        self.collected = False  # Track if this gate has been collected
        self.update_object()

    def update_object(self):
        super().update_position(power=1.5)
        super().update_size(power=2)

        # Update x position to keep the appropriate side touching the center line
        if self.side == "LEFT":
            self.x = self.center_x - self.width  # Right side touches center
        else:  # RIGHT
            self.x = self.center_x  # Left side touches center
        self.distance += 0.01  # Increment distance for scaling

    def draw(self, screen):
        # Create a surface for the transparent rectangle
        gate_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Choose colors based on operation and collected status
        fill_color = TRANSPARENT_GREY if self.collected else TRANSPARENT_BLUE
        outline_color = NEON_GREY if self.collected else NEON_BLUE

        # Draw the transparent fill
        pygame.draw.rect(gate_surface, fill_color, (0, 0, self.width, self.height))

        # Draw the neon outline
        outline_width = 3
        pygame.draw.rect(gate_surface, outline_color, (0, 0, self.width, self.height), outline_width)

        # Draw the transparent surface
        screen.blit(gate_surface, (self.x, self.y - self.height // 2))

        # Draw the value text along with the operation type
        operation_symbol = "+" if self.operation == "ADD" else "x"
        text = f"{operation_symbol} {self.value}"
        self.draw_text(screen, text, WHITE, (self.x + self.width // 2, self.y))