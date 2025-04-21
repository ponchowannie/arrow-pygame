import pygame
from components.constants import WINDOW_WIDTH, WINDOW_HEIGHT, BROWN

class ResultScreen:
    def __init__(self, message, font_path="./components/fonts/western.ttf", font_size=72):
        self.message = message
        self.font = pygame.font.Font(font_path, font_size)
        self.text = self.font.render(self.message, True, BROWN)
        self.text_rect = self.text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100))

    def apply_transparent_mask(self, screen):
        # Apply a transparent grey mask over the entire screen
        mask = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        mask.fill((0, 0, 0, 200))  # RGBA: 128 for transparency
        screen.blit(mask, (0, 0))

    def display(self, screen):
        screen.blit(self.text, self.text_rect)
