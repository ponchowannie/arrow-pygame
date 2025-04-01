import pygame
from .constants import *

class Player:
    def __init__(self):
        self.x = WINDOW_WIDTH // 2
        self.y = WINDOW_HEIGHT - 100
        self.width = 2  # Thin width for the line
        self.height = 40  # Height for the line
        self.angle = 90  # Angle in degrees
        self.speed = 8
        self.score = 0
        self.arrow_count = 1  # Number of lines to display
        self.font = pygame.font.Font(None, 36)
        self.arrow_spacing = 3  # Space between arrows in the same layer
        self.layer_height = 8  # Vertical space between layers

    def move(self, direction):
        if direction == 'left':
            self.x = max(self.width, self.x - self.speed)
        elif direction == 'right':
            self.x = min(WINDOW_WIDTH - self.width, self.x + self.speed)

    def draw(self, screen):
        # Create a surface for the arrows with transparency
        arrow_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        
        if self.arrow_count <= MAX_ARROWS_PER_LAYER:
            # For 12 or fewer arrows, stack them in a single layer
            # Calculate total width to center the arrows
            total_width = (self.arrow_count - 1) * self.arrow_spacing
            start_x = self.x - total_width // 2
            
            # Draw each arrow
            for i in range(self.arrow_count):
                x_pos = start_x + (i * self.arrow_spacing)
                # Draw transparent fill
                pygame.draw.rect(arrow_surface, (0, 0, 255, 128), 
                               (x_pos, self.y - self.height//2,
                                self.width, self.height))
                # Draw outline
                pygame.draw.rect(arrow_surface, BLUE, 
                               (x_pos, self.y - self.height//2,
                                self.width, self.height), 1)
        else:
            # For more than 12 arrows, create multiple layers
            arrows_per_layer = MAX_ARROWS_PER_LAYER
            num_layers = (self.arrow_count + arrows_per_layer - 1) // arrows_per_layer
            
            # Calculate total width for each layer
            layer_width = (arrows_per_layer - 1) * self.arrow_spacing
            start_x = self.x - layer_width // 2
            
            # Draw each layer
            for layer in range(num_layers):
                # Calculate how many arrows in this layer
                arrows_in_layer = min(arrows_per_layer, 
                                    self.arrow_count - (layer * arrows_per_layer))
                
                # Calculate layer width and starting position
                current_layer_width = (arrows_in_layer - 1) * self.arrow_spacing
                layer_start_x = self.x - current_layer_width // 2
                
                # Draw arrows in this layer
                for i in range(arrows_in_layer):
                    x_pos = layer_start_x + (i * self.arrow_spacing)
                    y_pos = self.y - self.height//2 - (layer * self.layer_height)
                    
                    # Draw transparent fill
                    pygame.draw.rect(arrow_surface, (0, 0, 255, 128), 
                                   (x_pos, y_pos,
                                    self.width, self.height))
                    # Draw outline
                    pygame.draw.rect(arrow_surface, BLUE, 
                                   (x_pos, y_pos,
                                    self.width, self.height), 1)
        
        # Draw the arrow surface onto the screen
        screen.blit(arrow_surface, (0, 0))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))

    def get_rect(self):
        # Calculate the total width and height needed for all arrows
        if self.arrow_count <= MAX_ARROWS_PER_LAYER:
            # For single layer, use the actual width of all arrows
            total_width = (self.arrow_count - 1) * self.arrow_spacing + self.width
            total_height = self.height
            return pygame.Rect(self.x - total_width//2, 
                             self.y - self.height//2,
                             total_width, 
                             total_height)
        else:
            # For multiple layers, create a rectangle that encompasses all layers
            arrows_per_layer = MAX_ARROWS_PER_LAYER
            num_layers = (self.arrow_count + arrows_per_layer - 1) // arrows_per_layer
            
            # Calculate the total width (using the maximum layer width)
            total_width = (arrows_per_layer - 1) * self.arrow_spacing + self.width
            
            # Calculate the total height including all layers
            total_height = self.height + (num_layers - 1) * self.layer_height
            
            # Return a rectangle centered on the player's position
            return pygame.Rect(self.x - total_width//2,
                             self.y - (total_height//2) - (num_layers - 1) * self.layer_height//2,
                             total_width,
                             total_height) 