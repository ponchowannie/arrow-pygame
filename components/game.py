import pygame
import random
from .constants import *
from .player import Player
from .gate import Gate
from .obstacle import Obstacle
from .background_object import BackgroundObject  # Import the BackgroundObject class
from .road_line import RoadLine  # Import the RoadLine class
from .boss import Boss  # Import the Boss class

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
        self.enemy_die = pygame.mixer.Sound("./components/sounds/enemy-die.mp3")
        self.gate_passed_sound = pygame.mixer.Sound("./components/sounds/gate-passed-sound.mp3")
        self.boss = None  # Initialize boss as None
        self.boss_active = False  # Flag to indicate if the boss is active
        self.gate_pair_count = 0  # Counter for the number of gate pairs spawned
        self.boss_beaten = False  # Track if the boss has been beaten
        print("Game initialized")

    def check_collisions(self):
        player_rect = self.player.get_rect()
        for gate in self.gates:
            if player_rect.colliderect(gate.get_rect()) and not gate.collected:
                self.gate_passed_sound.play()
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
                self.enemy_die.play()
                print(f"Hit obstacle! -{obstacle.damage} points. New score: {self.player.score}")
                self.obstacles.remove(obstacle)  # Remove after hit

        if self.boss and self.boss_active:  # Check collisions with the boss
            if player_rect.colliderect(self.boss.get_rect()):
                if self.player.score >= self.boss.health:
                    print("Player wins!")
                    self.boss.health = 0  # Update boss health to 0
                    self.boss_beaten = True  # Mark the boss as beaten
                elif self.player.score < self.boss.health:
                    print("Player loses!")
                    self.boss.health -= self.player.score  # Reduce boss health by player's score
                    self.player.score = 0  # Set player score to 0
                    self.boss_beaten = True  # Mark the boss as beaten

    def spawn_objects(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_timer > self.spawn_delay:
            # Generate a new pair ID
            pair_id = current_time
            # Spawn a pair of gates
            self.gates.append(Gate("LEFT", pair_id))
            self.gates.append(Gate("RIGHT", pair_id))
            self.spawn_timer = current_time
            self.gate_pair_count += 1  # Increment the gate pair counter
            print(f"Spawned new gate pair. Total pairs spawned: {self.gate_pair_count}")

        # Check if 5 pairs of gates have been spawned and the boss is not active
        if not self.boss_active and self.gate_pair_count >= 5:
            self.player.move("up")  # Move the player up
            self.boss = Boss()  # Create a new boss instance
            self.boss_active = True
            print("Boss has appeared!")

        if current_time - self.obs_timer > self.spawn_delay:
            enemy_count = random.randint(0, 3)  # Random number of enemies
            positions = [0, 1, 2, 3]
            enemy_positions = random.sample(positions, enemy_count)
            for enemy_no in range(enemy_count):
                self.obstacles.append(Obstacle(enemy_positions[enemy_no]))
            self.obs_timer = current_time
            if enemy_count > 0:
                print(f"Spawned {enemy_count} obstacle(s)")
        if current_time - self.bg_timer > CACTUS_SPAWN_DELAY:  # Spawn background objects less frequently
            bg_object = BackgroundObject()
            self.background_objects.append(bg_object)
            self.bg_timer = current_time
            # print(f"Spawned background object. Total: {len(self.background_objects)}")
        if current_time - self.road_line_timer > ROAD_LINE_SPAWN_DELAY:  # Spawn road lines periodically
            road_line = RoadLine() 
            self.road_lines.append(road_line)
            self.road_line_timer = current_time
            # print(f"Spawned road line. Total: {len(self.road_lines)}")

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
            if obstacle.y > WINDOW_HEIGHT:
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

        if self.boss and self.boss_active:  # Update the boss if active
            self.player.move("up")  # Ensure player moves up when boss is active
            self.boss.update_object()
            if self.boss.health <= 0:  # Check if the boss is defeated
                print("Boss defeated!")
                self.boss_active = False
                self.boss = None

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

        # Draw the boss if active
        if self.boss and self.boss_active:  
            self.boss.draw(screen)
        elif not self.boss and not self.boss_active and self.boss_beaten:
            self.boss.draw(screen)

        # Draw player
        self.player.draw(screen)
        
        pygame.display.flip()