import pygame
import sys
from components.constants import *
from components.buttons import Button

def show_start_screen(screen, background, clock):
    start_button = Button("Start Game", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 40, 200, 80, lambda: None)
    start_screen_active = True

    while start_screen_active:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            start_button.check_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and start_button._rect.collidepoint(event.pos):
                start_screen_active = False

        start_button.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)