import pygame
from components.constants import WHITE, BLUE

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self._text = text  # Encapsulated property
        self._rect = pygame.Rect(x, y, width, height)  # Encapsulated property
        self._color = BLUE
        self._hover_color = (0, 150, 255)
        self._callback = callback
        self._font = pygame.font.Font(None, 48)

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self._hover_color if self._rect.collidepoint(mouse_pos) else self._color
        pygame.draw.rect(surface, color, self._rect)
        text_surface = self._font.render(self._text, True, WHITE)
        text_rect = text_surface.get_rect(center=self._rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self._rect.collidepoint(event.pos):
            self._callback()
