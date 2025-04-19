import pygame
import random
from .constants import WINDOW_HEIGHT, WINDOW_WIDTH
from core.game_object import GameObject


CACTUS1_ORIGINAL = pygame.image.load('./components/images/cactus2.png')
CACTUS2_ORIGINAL = pygame.image.load('./components/images/cactus2.png')
CACTUS1 = pygame.transform.scale_by(pygame.image.load('./components/images/cactus2.png'), 0.05)
CACTUS2 = pygame.transform.scale(pygame.image.load('./components/images/cactus2.png'), CACTUS1.get_size())

class BackgroundObject(GameObject):
    def __init__(self):
        # Randomly choose between cactus1 and cactus2
        choice = random.randint(1, 2)
        self.image = CACTUS1 if choice == 1 else CACTUS2
        self.original_image = CACTUS1_ORIGINAL if choice == 1 else CACTUS2_ORIGINAL # Store the original image for scaling

        side = random.choice(["LEFT", "RIGHT"])  # Randomly decide the side
        x = random.randint(40, 140) if side == "LEFT" else random.randint(250, 360)  # Set initial x position
        y = 290 - self.image.get_height()  # Position the bottom of the image at y = 283
        base_movement_speed = 0.1  # Base vertical movement speed

        # Initialize using the superclass
        super().__init__(base_width=self.image.get_width(), base_height=self.image.get_height(), 
                         start_position=(x, y), base_movement_speed=base_movement_speed)

        self.side = side
        self.speed_x = 0.01
        self.old_width = self.width

    def update_object(self):
        super().update_position(power=2)
        super().update_size(power=1.5)
        

        width_change = (self.width - self.old_width) * 3
        # Adjust x position based on side and scaling
        offset = self.speed_x * (1 + self.distance ** 3) + width_change

        if self.side == "LEFT":
            self.x -= offset
        else:  # RIGHT
            self.x += offset

        # Update distance to track movement
        self.distance += 0.003 # Increment distance for scaling and movement
        self.old_width = self.width

        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))

    def draw(self, screen):
        # Draw the object on the screen
        screen.blit(self.image, (self.x, self.y))
