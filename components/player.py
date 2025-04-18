import pygame
from .constants import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 100
        self.width = 40  # Thin width for the line
        self.height = 80  # Height for the line
        self.angle = 90  # Angle in degrees
        self.speed = 8
        self.score = 0
        self.arrow_count = 1  # Number of lines to display
        self.font = pygame.font.Font(None, 36)
        self.arrow_spacing = -20  # Space between arrows in the same layer
        self.layer_height = -60  # Vertical space between layers

        self.arrow_image = pygame.image.load("./components/images/arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (self.width, self.height))

    def update_arrow_count(self):
        self.arrow_count = max(1, self.score // 10 + 1)
        arrow_count = min(self.arrow_count, 15)
        self.arrow_count = arrow_count

    def move(self, direction):
        if direction == 'left':
            self.x = max(self.width, self.x - self.speed)
        elif direction == 'right':
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def draw(self, screen):
        self.update_arrow_count()

        # Create a surface for the arrows with transparency
        arrow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        arrows_remaining = self.arrow_count
        row = 0
        rows = []

        while arrows_remaining > 0 and row < 5:
            arrows_in_row = min(5 - row, arrows_remaining)
            rows.append(arrows_in_row)
            arrows_remaining -= arrows_in_row
            row += 1

        # Overlap settings
        horiz_overlap = self.arrow_spacing
        vert_overlap = self.layer_height
        row_spacing = self.height + vert_overlap

        base_y = self.y

        for row_index, arrows_in_row in enumerate(rows):  # No reverse — biggest row first
            y_pos = base_y + row_index * row_spacing

            total_row_width = self.width + (arrows_in_row - 1) * (self.width + horiz_overlap)
            start_x = self.x - total_row_width // 2

            for i in range(arrows_in_row):
                x_pos = start_x + i * (self.width + horiz_overlap)
                arrow_rect = self.arrow_image.get_rect(center=(x_pos, y_pos))
                arrow_surface.blit(self.arrow_image, arrow_rect.topleft)

        screen.blit(arrow_surface, (0, 0))

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def get_rect(self):
        self.update_arrow_count()

        arrows_remaining = self.arrow_count
        row = 0
        rows = []

        while arrows_remaining > 0 and row < 5:
            arrows_in_row = min(5 - row, arrows_remaining)
            rows.append(arrows_in_row)
            arrows_remaining -= arrows_in_row
            row += 1

        horiz_overlap = -20
        vert_overlap = -30
        row_spacing = self.height + vert_overlap

        max_row_width = max(rows) if rows else 1
        total_width = self.width + (max_row_width - 1) * (self.width + horiz_overlap)
        total_height = len(rows) * row_spacing

        return pygame.Rect(
            self.x - total_width // 2,
            self.y - self.height // 2,
            total_width,
            total_height
        )