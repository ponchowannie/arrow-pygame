import pygame
from .constants import WINDOW_WIDTH, WINDOW_HEIGHT, ROAD_LINE_COLOR, ROAD_LINE_WIDTH, ROAD_LINE_HEIGHT

class RoadLine:
    def __init__(self):  # Allow setting initial distance
        self.width = ROAD_LINE_WIDTH
        self.x = 0  # Initialize x; it will be set by recenter_horizontally
        self.y = 290  # Start just above the screen
        self.height = ROAD_LINE_HEIGHT
        self.distance = 0
        self.recenter_horizontally()  # Center the road line initially

    def recenter_horizontally(self):
        """Recalculate and set the x position to center the road line."""
        self.x = WINDOW_WIDTH // 2 - self.width // 2 + 5

    def update_object(self):
        self.y += self.distance  # Move vertically based on distance
        self.width *= 1.004  # Increase width exponentially
        self.recenter_horizontally()  # Re-center after width change

    def draw(self, screen):
        pygame.draw.rect(screen, ROAD_LINE_COLOR, (self.x, self.y, self.width, self.height))

