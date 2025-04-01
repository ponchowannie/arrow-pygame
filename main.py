import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
TRANSPARENT_BLUE = (0, 0, 255, 180)  # Blue with 70% opacity

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Arrow Perspective Game")
clock = pygame.time.Clock()

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 100
        self.width = 4  # Thinner width for the line
        self.height = 40  # Taller height for the line
        self.angle = 90  # Angle in degrees
        self.speed = 5
        self.score = 0
        self.arrow_count = 1  # Number of lines to display
        self.font = pygame.font.Font(None, 36)

    def move(self, direction):
        if direction == 'left':
            self.x = max(self.width, self.x - self.speed)
        elif direction == 'right':
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def draw(self, screen):
        # Draw multiple lines based on arrow_count
        for i in range(self.arrow_count):
            offset = i * (self.width + 2)  # Space between lines (very close together)
            pygame.draw.rect(screen, BLUE, 
                           (self.x + offset, self.y - self.height//2,
                            self.width, self.height))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def get_rect(self):
        # Return a rectangle that covers all lines
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                         self.width * self.arrow_count + (self.arrow_count - 1) * 2, 
                         self.height)

class Gate:
    __startPosition = (WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - WINDOW_HEIGHT // 3)

    def __init__(self, side):
        self.distance = 0  # Distance from player (0 to 1)
        self.base_width = 30
        self.base_height = 60
        self.side = side
        self.center_x = Gate.__startPosition[0]
        self.x = Gate.__startPosition[0]
        self.y = Gate.__startPosition[1]
        self.base_movement_speed = 0.3
        self.value = random.randint(-10, 10)  # Random value to display
        self.font = pygame.font.Font(None, 36)  # Font for text
        self.update_position()

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height//2, 
                         self.width, self.height)

    def update_position(self):
        # Use quadratic scaling for smoother size increase
        scale_factor = 1 + (self.distance * self.distance)
        self.width = self.base_width * scale_factor
        self.height = self.base_height * scale_factor
        
        # Update x position to keep the appropriate side touching the center line
        if self.side == "LEFT":
            self.x = self.center_x - self.width  # Right side touches center
        else:  # RIGHT
            self.x = self.center_x  # Left side touches center
            
        # Scale movement speed with distance (faster as it gets closer)
        self.y += (self.base_movement_speed * (1 + self.distance)) * 2

    def draw(self, screen):
        # Create a surface for the transparent rectangle
        gate_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(gate_surface, TRANSPARENT_BLUE, 
                        (0, 0, self.width, self.height))
        
        # Draw the transparent surface
        screen.blit(gate_surface, 
                   (self.x, self.y - self.height//2))
        
        # Draw the value text in black for better contrast
        text = self.font.render(str(self.value), True, BLACK)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y))
        screen.blit(text, text_rect)

class Game:
    def __init__(self):
        self.player = Player()
        self.gates = []
        self.obstacles = []
        self.spawn_timer = 0
        self.spawn_delay = 2000  # milliseconds
        self.game_speed = 0.003  # Reduced speed for smoother movement

    def check_collisions(self):
        player_rect = self.player.get_rect()
        for gate in self.gates[:]:
            if player_rect.colliderect(gate.get_rect()):
                # Update arrow count based on gate value
                new_count = self.player.arrow_count + gate.value
                if new_count > 0:  # Ensure we don't go below 1 arrow
                    self.player.arrow_count = new_count
                self.player.score += gate.value
                self.gates.remove(gate)

    def spawn_objects(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            # Randomly spawn either a gate or an obstacle
            self.gates.append(Gate("LEFT"))
            self.gates.append(Gate("RIGHT"))
            self.spawn_timer = current_time

    def update(self):
        # Update object positions
        for gate in self.gates[:]:
            gate.distance += self.game_speed
            gate.update_position()
            if gate.distance > 2:  # Increased to allow gates to grow larger
                self.gates.remove(gate)

        for obstacle in self.obstacles[:]:
            obstacle.distance += self.game_speed
            obstacle.update_position()
            if obstacle.distance > 1:
                self.obstacles.remove(obstacle)

        self.spawn_objects()
        self.check_collisions()

    def draw(self, screen):
        screen.fill(WHITE)  # Changed from BLACK to WHITE
        
        # Draw gates and obstacles
        for gate in self.gates:
            gate.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            
        # Draw player
        self.player.draw(screen)
        
        pygame.display.flip()

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