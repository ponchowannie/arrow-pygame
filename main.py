import pygame
from components.constants import *
from components.game import Game
from components.start_screen import show_start_screen
from components.buttons import apply_transparent_mask, RestartButton

# Initialize Pygame
pygame.init()

# Loag the background image
BACKGROUND_IMAGE = pygame.image.load('./components/images/background.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arrow Perspective Game")
clock = pygame.time.Clock()

def show_restart_button(screen, clock):
    restart_button = RestartButton(lambda: None)
    while True:
        restart_button.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            restart_button.check_click(event)
            if event.type == pygame.MOUSEBUTTONDOWN and restart_button._rect.collidepoint(event.pos):
                return

        clock.tick(FPS)

def main():
    while True:  # Loop to allow restarting the game
        show_start_screen(screen, BACKGROUND_IMAGE, clock)
        game = Game()
        running = True

        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Handle continuous key presses
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                game.player.move('left')
            if keys[pygame.K_RIGHT]:
                game.player.move('right')
            if keys[pygame.K_UP]:
                game.player.move('up')

            # Update game state
            game.update()

            # Draw the background
            screen.blit(BACKGROUND_IMAGE)

            # Draw everything else
            game.draw(screen)

            # Check if the boss has been beaten
            if game.boss_beaten:
                apply_transparent_mask(screen)
                show_restart_button(screen, clock)
                break  # Exit the running loop to restart the game

            # Cap the framerate
            clock.tick(FPS)

if __name__ == "__main__":
    main()