import pygame
from components.constants import WHITE

hat_image = pygame.image.load("./components/images/cowboy_hat.png")
hat_image = pygame.transform.scale(hat_image, (70, 70))

class Button:
    def __init__(self, text, x, y, width, height, callback, color, hover_color, font, isHat=False):
        self._text = text  # Encapsulated property
        self._rect = pygame.Rect(x, y, width, height)  # Encapsulated property
        self._color = color
        self._hover_color = hover_color
        self._callback = callback
        self._font = font
        self.hat_image = hat_image if isHat else None

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self._hover_color if self._rect.collidepoint(mouse_pos) else self._color
        pygame.draw.rect(surface, color, self._rect)
        text_surface = self._font.render(self._text, True, WHITE)
        text_rect = text_surface.get_rect(center=self._rect.center)
        surface.blit(text_surface, text_rect)
        if self.hat_image:
            hat_rect = self.hat_image.get_rect()
            hat_rect.midbottom = (text_rect.left, text_rect.top + 18)
            surface.blit(self.hat_image, hat_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self._rect.collidepoint(event.pos):
            self._callback()
