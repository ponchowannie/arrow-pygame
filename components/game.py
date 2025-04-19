import pygame
import random
from .constants import *
from .player import Player
from .gate import Gate
from .obstacle import Obstacle

class Game:
    def __init__(self):
        print("Initializing game...")
        self.player = Player()
        self.gates = []
        self.obstacles = []
        self.spawn_timer = 0
        self.obs_timer = -SPAWN_DELAY/2
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
                    # Update arrow count based on gate value
                    new_count = self.player.arrow_count + gate.value
                    if new_count > 0:  # Ensure we don't go below 1 arrow
                        self.player.arrow_count = new_count
                    self.player.score += gate.value
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
        print(f"Drawing game state - Gates: {len(self.gates)}, Player arrows: {self.player.arrow_count}")
        
        # Draw gates and obstacles
        for gate in self.gates:
            gate.draw(screen)
        for obstacle in self.obstacles:
            obstacle.draw(screen)
            

        # Draw player
        self.player.draw(screen)
        
        pygame.display.flip() 