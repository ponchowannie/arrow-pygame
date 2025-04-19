import pygame
from components.constants import *

class GameObject:
    def __init__(self, base_width, base_height, start_position, base_movement_speed):
        self.distance = 0  # Distance from player (0 to 1)
        self.base_width = base_width
        self.base_height = base_height
        self.center_x = start_position[0]
        self.x = start_position[0]
        self.y = start_position[1]
        self.base_movement_speed = base_movement_speed
        self.width = base_width
        self.height = base_height
        self.font = pygame.font.Font(None, 36)

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)

    def update_position(self, power=1.5):
        # Scale movement speed with distance (faster as it gets closer)
        self.y += (self.base_movement_speed * (1 + self.distance)) * 2

    def update_size(self, power=1.5):
        # Use power-based scaling for smoother size increase
        scale_factor = 1 + (self.distance ** power)
        self.width = self.base_width * scale_factor
        self.height = self.base_height * scale_factor

    def draw_text(self, screen, text, color, center):
        rendered_text = self.font.render(str(text), True, color)
        text_rect = rendered_text.get_rect(center=center)
        screen.blit(rendered_text, text_rect)