import pygame
from components.constants import *
from components.game import Game
from components.buttons.start_screen import StartScreen 
from components.buttons.main_menu import apply_transparent_mask, show_restart_button
from components.screens.result_screen import ResultScreen

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
    pygame.mixer.music.load("./components/sounds/bgm.mp3")
    pygame.mixer.music.set_volume(0.2)
    
    while True:  # Loop to allow restarting the game
        start_screen = StartScreen(screen, BACKGROUND_IMAGE, clock)  # Instantiate StartScreen
        diff = start_screen.run()  # Call the run method
        game = Game(diff)
        running = True
        pygame.mixer.music.play(-1)
        while running:
            current_time = pygame.time.get_ticks()

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
            if keys[pygame.K_s]:
                if not hasattr(game, 'last_arrow_time') or current_time - game.last_arrow_time >= 200:
                    game.spawn_arrow(direction='up')  # Spawn arrows moving in -y direction
                    game.last_arrow_time = current_time
                
            # Update game state
            game.update()

            # Draw the background
            screen.blit(BACKGROUND_IMAGE)

            # Draw everything else
            game.draw(screen)

            # Check if the player's health is 0 or less
            if game.player.score <= 0:
                apply_transparent_mask(screen)
                result_screen = ResultScreen("You Lost!")
                result_screen.display(screen)
                show_restart_button(screen, clock)
                pygame.mixer.music.stop()
                break  # Exit the running loop to restart the game

            # Check if the boss has been beaten
            if game.boss_beaten:
                apply_transparent_mask(screen)
                result_screen = ResultScreen("You Win!")
                result_screen.display(screen)
                show_restart_button(screen, clock)
                pygame.mixer.music.stop()
                break  # Exit the running loop to restart the game

            # Cap the framerate
            clock.tick(FPS)
            
if __name__ == "__main__":
    main()