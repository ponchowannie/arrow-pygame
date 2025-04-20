import pygame
from components.constants import *
from components.game import Game
from components.start_screen import show_start_screen

# Initialize Pygame
pygame.init()

# Loag the background image
BACKGROUND_IMAGE = pygame.image.load('./components/images/background.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arrow Perspective Game")
clock = pygame.time.Clock()

def main():
    hat_image = pygame.image.load("./components/images/cowboy_hat.png")
    hat_image = pygame.transform.scale(hat_image, (70, 70))
    show_start_screen(screen, BACKGROUND_IMAGE, clock, hat_image)
    pygame.mixer.music.load("./components/sounds/bgm.mp3")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    game = Game()
    running = True

    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            game.player.move('left')
        if keys[pygame.K_RIGHT]:
            game.player.move('right')

        # Update game state
        game.update()

        # Draw the background
        screen.blit(BACKGROUND_IMAGE)

        # Draw everything else
        game.draw(screen)

        # Cap the framerate
        clock.tick(FPS)
    pygame.mixer.music.stop()
    pygame.quit()

if __name__ == "__main__":
    main()