import pygame
import random
from .constants import *
from .player import Player
from .gate import Gate
from .obstacle import Obstacle
from .background_object import BackgroundObject  # Import the BackgroundObject class
from .road_line import RoadLine  # Import the RoadLine class

class Game:
    def __init__(self):
        print("Initializing game...")
        self.player = Player()
        self.gates = []
        self.obstacles = []
        self.background_objects = []  # List to store background objects
        self.road_lines = []  # List to store road line objects
        self.spawn_timer = 0
        self.obs_timer = -SPAWN_DELAY/2
        self.bg_timer = 0  # Timer for spawning background objects
        self.road_line_timer = 0  # Timer for spawning road lines
        self.spawn_delay = SPAWN_DELAY
        self.game_speed = GAME_SPEED
        self.collected_pairs = set()  # Track which gate pairs have been collected
        print("Game initialized")

    def check_collisions(self):
        player_rect = self.player.get_rect()
        for gate in self.gates:
            if player_rect.colliderect(gate.get_rect()) and not gate.collected:
                # Only process collision if the pair hasn't been collected yet
                if gate.pair_id not in self.collected_pairs:
                    # Update arrow count and score based on gate value
                    if gate.operation == "ADD":
                        new_count = self.player.score + gate.value
                    elif gate.operation == "MULTIPLY":
                        new_count = self.player.score * gate.value

                    if new_count > 0:  # Ensure we don't go below 1 arrow
                        self.player.arrow_count = new_count
                    self.player.score = new_count  # Update score to calculated value
                    self.collected_pairs.add(gate.pair_id)
                    # Mark both gates in the pair as collected
                    for g in self.gates:
                        if g.pair_id == gate.pair_id:
                            g.collected = True
        for obstacle in self.obstacles[:]:
            if player_rect.colliderect(obstacle.get_rect()):
                self.player.score -= obstacle.damage
                print(f"Hit obstacle! -{obstacle.damage} points. New score: {self.player.score}")
                self.obstacles.remove(obstacle)  # Remove after hit

    def spawn_objects(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            # Generate a new pair ID
            pair_id = current_time
            # Spawn a pair of gates
            self.gates.append(Gate("LEFT", pair_id))
            self.gates.append(Gate("RIGHT", pair_id))
            self.spawn_timer = current_time
            print(f"Spawned new gate pair. Total gates: {len(self.gates)}")
        if current_time - self.obs_timer > self.spawn_delay:
            enemy_count = random.randint(0, 3)  # Random number of enemies
            for _ in range(enemy_count):
                obstacle = Obstacle()
                # Randomize horizontal position across screen
                obstacle.x = random.randint(obstacle.width, WINDOW_WIDTH - obstacle.width)
                self.obstacles.append(obstacle)
            self.obs_timer = current_time
            if enemy_count > 0:
                print(f"Spawned {enemy_count} obstacle(s)")
        if current_time - self.bg_timer > CACTUS_SPAWN_DELAY:  # Spawn background objects less frequently
            bg_object = BackgroundObject()
            self.background_objects.append(bg_object)
            self.bg_timer = current_time
            print(f"Spawned background object. Total: {len(self.background_objects)}")
        if current_time - self.road_line_timer > ROAD_LINE_SPAWN_DELAY:  # Spawn road lines periodically
            road_line = RoadLine() 
            self.road_lines.append(road_line)
            self.road_line_timer = current_time
            print(f"Spawned road line. Total: {len(self.road_lines)}")

    def update(self):
        # Update object positions
        for gate in self.gates[:]:
            gate.distance += self.game_speed
            gate.update_object()
            if gate.y > WINDOW_HEIGHT:  # Increased to allow gates to grow larger
                self.gates.remove(gate)

        for obstacle in self.obstacles[:]:
            obstacle.distance += self.game_speed
            obstacle.update_object()
            if obstacle.distance > 1:
                self.obstacles.remove(obstacle)

        for bg_object in self.background_objects[:]:
            bg_object.distance += self.game_speed  # Background objects move slower
            bg_object.update_object()
            if bg_object.x + bg_object.width < -20 or bg_object.x > WINDOW_WIDTH:  # Remove if completely out of the screen (left or right)
                self.background_objects.remove(bg_object)

        for road_line in self.road_lines[:]:
            road_line.distance += self.game_speed  # Move road lines
            road_line.update_object()
            if road_line.y > WINDOW_HEIGHT:  # Remove if completely out of the screen
                self.road_lines.remove(road_line)

        self.spawn_objects()
        self.check_collisions()

    def draw(self, screen):
        # Draw background objects in reverse order
        for bg_object in reversed(self.background_objects):
            bg_object.draw(screen)

        # Draw road lines in reverse order
        for road_line in reversed(self.road_lines):
            road_line.draw(screen)

        # Draw gates and obstacles in reverse order
        for gate in reversed(self.gates):
            gate.draw(screen)
        for obstacle in reversed(self.obstacles):
            obstacle.draw(screen)

        # Draw player
        self.player.draw(screen)
        
        pygame.display.flip()