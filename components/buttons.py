import pygame
from components.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS
from core.button import Button  # Import Button from core/button.py

class RestartButton(Button):
    def __init__(self, callback):
        super().__init__("Main Menu", WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2, 200, 50, callback)

def apply_transparent_mask(screen):
    # Apply a transparent grey mask over the entire screen
    mask = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    mask.fill((0, 0, 0, 200))  # RGBA: 128 for transparency
    screen.blit(mask, (0, 0))
    pygame.display.flip()

def show_restart_button(screen, clock):
    # Display the restart button and wait for the player to press it
    def restart_callback():
        nonlocal running
        running = False

    restart_button = RestartButton(restart_callback)
    running = True

    while running:
        restart_button.draw(screen)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            restart_button.check_click(event)

