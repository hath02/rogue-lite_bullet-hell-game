import random

class Targeting:
    def select(self, context):
        pass

class TargetResult:
    def __init__(
        self,
        position = None,
        enemy = None,
        direction = None
    ):
        self.position = position
        self.enemy = enemy
        self.direction = direction
        
    def has_position(self):
        return self.position is not None
    
    def has_enemy(self):
        return self.enemy is not None
        
class NearestEnemy(Targeting):
    def __init__(self, max_range = None):
        self.max_range = max_range
        
    def select(self, context):
        player = context.player
        
        nearest = None
        nearest_distance = float("inf")
        
        for enemy in context.enemies:
            if not enemy.alive:
                continue
            
            distance = player.position.distance_to(
                enemy.position
            )
            
            if self.max_range:
                if distance > self.max_range:
                    continue
                
            if distance < nearest_distance:
                nearest = enemy
                nearest_distance = distance
                
        if nearest:
            return TargetResult(
                enemy = nearest,
                position = nearest.position
            )
        
        return None
    
class EnemyCluster(Targeting):
    def __init__(self, radius, max_range):
        self.radius = radius
        self.max_range = max_range
        
    def select(self, context):
        player = context.player
        
        enemies = []
        
        for enemy in context.enemies:
            if not enemy.alive:
                continue
            
            if self.max_range is not None:
                distance = player.position.distance_to(
                    enemy.position
                )
                
                if distance > self.max_range:
                    continue
                
            enemies.append(enemy)
            
        if not enemies:
            return None
        
        best_position = None
        highest_count = 0
        
        for enemy in enemies:
            count = 0
            
            for other in enemies:
                if enemy.position.distance_to(
                    other.position
                ) <= self.radius:
                    count += 1
                    
            if count > highest_count:
                highest_count = count
                best_position = enemy.position
                
        return TargetResult(
            position = best_position
        )

class RandomEnemy(Targeting):
    def __init__(self, max_range = None):
        self.max_range = max_range
        
    def select(self, context):
        player = context.player
        
        available = []
        
        for enemy in context.enemies:
            if not enemy.alive:
                continue
            
            if self.max_range:
                distance = (
                    player.position
                    .distance_to(enemy.position)
                )
                
                if distance > self.max_range:
                    continue
                
            available.append(enemy)
            
        if not available:
            return None
        
        target = random.choice(
            available
        )
        
        return TargetResult(
            enemy = target,
            position = target.position
        )
            
class PlayerDirection(Targeting):
    def select(self, context):
        return TargetResult(
            direction = context.player.facing_direction
        )
    