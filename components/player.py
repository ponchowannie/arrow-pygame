import pygame
from .constants import *
import math

class Player:
    pygame.font.init()
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 100
        self.width = 20  # Arrow width
        self.height = 60  # Arrow height
        self.speed = 8
        self.score = 1
        self.arrow_count = 1  # Number of arrows
        self.font = pygame.font.SysFont("Comic Sans MS", 24) # Font to use
        self.arrow_spacing = -5 # Space between arrows in same level
        self.layer_height = -50  # Space between arrows in different level

        self.arrow_image = pygame.image.load("./components/images/arrow.png").convert_alpha()
        self.arrow_image = pygame.transform.scale(self.arrow_image, (self.width, self.height))

    def update_arrow_count(self):
        if self.score > 0:
            self.arrow_count = max(1, int(math.log10(self.score) // 1) + 1) # Minimum of 1 arrow showing
        else:
            self.arrow_count = 1
        arrow_count = min(self.arrow_count, 15) # Maximum of 15 arrow showing (pyramid)
        self.arrow_count = arrow_count

    def move(self, direction):
        if direction == 'left':
            self.x = max(self.width, self.x - self.speed)
        elif direction == 'right':
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)
        elif direction == 'up':
            self.y = max(self.height, self.y - self.speed)

    def draw(self, screen):
        self.update_arrow_count()

        arrow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        # For arrow formation
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

        for row_index, arrows_in_row in enumerate(rows):
            y_pos = base_y + row_index * row_spacing

            total_row_width = self.width + (arrows_in_row - 1) * (self.width + horiz_overlap)
            start_x = self.x - total_row_width // 2

            for i in range(arrows_in_row):
                x_pos = start_x + i * (self.width + horiz_overlap)
                arrow_rect = self.arrow_image.get_rect(center=(x_pos, y_pos))
                arrow_surface.blit(self.arrow_image, arrow_rect.topleft)

        screen.blit(arrow_surface, (0, 0))

        # Draw score below player
        score_text = self.font.render(f"Arrow x{self.score}", True, BLACK)
        text_rect = score_text.get_rect(center=(self.x, self.y + 60))
        screen.blit(score_text, text_rect)

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