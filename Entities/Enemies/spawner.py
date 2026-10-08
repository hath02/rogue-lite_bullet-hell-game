import pygame, random

from Entities.Enemies.normal_enemy import Normal
from Entities.Enemies.range_enemy import Range
from Entities.Enemies.tank_enemy import Tank

class Spawner:
    def __init__(self):
        self.spawn_timer = 0
        self.base_spawn_interval = 2.0
    
    # Enemies spawn faster as time passes    
    def get_spawn_interval(self, elapsed_time):
        # Every minute reduce the spawn interval by 0.15s
        interval = self.base_spawn_interval - (
            elapsed_time / 60 * 0.15
        )
        
        # Never spawn faster than 0.3s
        return max(
            0.3,
            interval
        )  
    
    # Increase enemies spawned at once      
    def get_enemies_per_spawn(self, elapsed_time):
        minutes = elapsed_time / 60
        
        if minutes < 2:
            return 1
        
        elif minutes < 5:
            return 2
        
        elif minutes < 8:
            return 3
        
        elif minutes < 10:
            return 5
        
        else:
            return 6
    
    # Which enemy types can spawn and spawn probabilities    
    def get_enemy_pool(self, elapsed_time):
        # 0:00 - 1:30
        if elapsed_time < 90:
            return [
                (Normal, 100)
            ]
            
        # 1:30 - 3:00
        elif elapsed_time < 180:
            return [
                (Normal, 80),
                (Range, 20)
            ]
        
        # 3:00 - 5:00    
        elif elapsed_time < 300:
            return [
                (Normal, 80),
                (Range, 15),
                (Tank, 5)
            ]
            
        # 5:00 - 8:00
        elif elapsed_time < 480:
            return [
                (Normal, 70),
                (Range, 20),
                (Tank, 10)
            ]
        
        else:
            return [
                (Normal, 65),
                (Range, 20),
                (Tank, 15)
            ]   
    
    # Choose enemy
    def get_enemy_class(self, elapsed_time):
        pool = self.get_enemy_pool(elapsed_time)
        
        enemy_classes = [
            enemy[0]
            for enemy in pool
        ]      
        
        weights = [
            enemy[1]
            for enemy in pool
        ]
        
        return random.choices(
            enemy_classes,
            weights = weights,
            k = 1
        )[0]
        
    # Spawn enemy
    def spawn_enemy(self, player):
        # Random direction from player
        angle = random.uniform(
            0,
            2 * 3.14159265
        )    
        
        direction = pygame.Vector2(1, 0)
        
        # Distance outside of camera
        spawn_distance = 1000
        
        position = (
            player.position
            + direction.rotate_rad(angle)
            * spawn_distance
        )
        
        return position
    
    # Increase difficulty & exp reward
    def get_difficulty(self, elapsed_time):
        return 1 + (elapsed_time / 60 * 0.1)
    
    def get_exp_multiplier(self, elapsed_time):    
        return 1 + (elapsed_time / 60 * 0.05)
    
    def scale_enemy(self, enemy, elapsed_time):
        difficulty = self.get_difficulty(elapsed_time)
        exp_multiplier = self.get_exp_multiplier(elapsed_time)
        
        enemy.max_hp *= difficulty
        enemy.hp = enemy.max_hp
        
        enemy.damage *= difficulty

        enemy.exp_reward = int(enemy.exp_reward * exp_multiplier)
        
    def update(self, dt, player, enemies, elapsed_time):
        self.spawn_timer -= dt
        
        if self.spawn_timer > 0:
            return
        
        # Get how many enemies should spawn
        amount = self.get_enemies_per_spawn(elapsed_time)
        
        # Spawn enemies
        for _ in range(amount):
            enemy_class = self.get_enemy_class(elapsed_time)
            
            position = self.spawn_enemy(player)
            
            enemy = enemy_class(position)        
                        
            # Update difficulty
            self.scale_enemy(
                enemy,
                elapsed_time
            )
            
            enemies.append(enemy)
            
        # Reset timer
        self.spawn_timer = self.get_spawn_interval(elapsed_time)