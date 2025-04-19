import pygame
from components.constants import WINDOW_WIDTH, WINDOW_HEIGHT

# Initialize Pygame
pygame.init()

# Load the background image
BACKGROUND_IMAGE = pygame.image.load('./components/images/background.png')
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Set up the screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mouse Tracker")

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check if the mouse is pressed
    mouse_pressed = pygame.mouse.get_pressed()
    if any(mouse_pressed):  # Check if any mouse button is pressed
        mouse_x, mouse_y = pygame.mouse.get_pos()
        print(f"Mouse Position: ({mouse_x}, {mouse_y})")

    # Draw the background
    screen.blit(BACKGROUND_IMAGE, (0, 0))

    # Draw a circle at the mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (255, 0, 0), (mouse_x, mouse_y), 5)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
