import pygame
import sys
from components.constants import *

pygame.font.init()

LIGHT_BLUE = (0, 150, 255)
FONT = pygame.font.Font(None, 48)

class Button:
    def __init__(self, text, x, y, width, height, callback):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = BLUE
        self.hover_color = LIGHT_BLUE
        self.callback = callback

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = FONT.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.callback()

def show_start_screen(screen, background, clock):
    start_button = Button("Start Game", WINDOW_WIDTH//2 - 100, WINDOW_HEIGHT//2 - 40, 200, 80, lambda: None)
    start_screen_active = True

    while start_screen_active:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.check_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button.rect.collidepoint(event.pos):
                start_screen_active = False

        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)