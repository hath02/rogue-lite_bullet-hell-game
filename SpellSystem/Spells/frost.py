import pygame, math

from SpellSystem.spell import Spell
from Systems.Behaviors.area import AreaBehavior
from Systems.targeting import NearestEnemy
from SpellSystem.effects import Slow

class Frost(Spell):
    def __init__(self):
        super().__init__()
        
        self.targeting = NearestEnemy(
            max_range = 300
        )
        
        # Changed stats
        self.stats.damage = 2
        self.stats.cooldown = 8.0
        self.stats.duration = 4.0      
          
        # Frost stats
        self.radius = 150
        self.slow_multiplier = 0.5
        
        # Visual stats
        self.field_size = 300

        # Animation
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/frost/frost{i}.png"
                ).convert_alpha(),
                (self.field_size, self.field_size)
            )
            for i in range(1, 5)
        ]
        
    def cast(self, context):
        player = context.player

        result = self.targeting.select(context)

        if result is None:
            return None

        # Direction from player to enemy
        direction = (
            result.position - player.position
        )

        if direction.length() != 0:
            direction = direction.normalize()

        # Spawn frost in front of player
        cast_distance = 120

        position = (
            player.position
            + direction * cast_distance
        )
        
        return FrostField(
            position,
            direction,
            self.stats,
            self.radius,
            self.slow_multiplier,
            self.frames
        )    
        
class FrostField(AreaBehavior):        
    def __init__(
        self,
        position,
        direction,
        stats,
        radius,
        slow_multiplier,
        frames
    ):
        super().__init__(
            position,
            radius,
            stats.duration
        )
        
        self.collision_type = "area"
        
        # Visual
        self.on_ground = True
                
        self.direction = direction

        self.damage = 0
        self.damage_interval = 1.0
        
        self.radius = radius
        
        self.slow_multiplier = slow_multiplier
        
        self.hit_timers = {}
        
        # Animation
        self.frames = frames
        
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.15
    
    def on_hit(self, enemy):
        enemy.apply_effect(
            Slow(
                duration = 0.5,
                multiplier = self.slow_multiplier
            )
        )
        
    def update(self, dt):
        super().update(dt)
        
        # Animation
        if self.animation_frame < len(self.frames) - 1:
            self.animation_timer += dt

            if self.animation_timer >= self.animation_speed:
                self.animation_timer -= self.animation_speed
                self.animation_frame += 1
                   
    def draw(self, screen, camera):
        if not self.alive:
            return

        frame = self.frames[self.animation_frame]

        angle = math.degrees(
            math.atan2(
                -self.direction.y,
                self.direction.x
            )
        )

        frame = pygame.transform.rotate(
            frame,
            angle - 90
        )

        screen_position = camera.apply(self.position)

        rect = frame.get_rect(
            center=(
                int(screen_position.x),
                int(screen_position.y)
            )
        )

        screen.blit(frame, rect)