import pygame
from components.constants import *
from components.game import Game

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arrow Perspective Game")
clock = pygame.time.Clock()

def main():
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
        
        # Draw everything
        game.draw(screen)
        
        # Cap the framerate
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main() 