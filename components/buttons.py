import pygame
from components.constants import WINDOW_WIDTH, WINDOW_HEIGHT, FPS, WHITE, BLUE

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
        screen.fill((0, 0, 0))  # Clear the screen
        restart_button.draw(screen)
        pygame.display.flip()

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            restart_button.check_click(event)

        clock.tick(FPS)
