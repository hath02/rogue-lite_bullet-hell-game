import pygame

from SpellSystem.spell import Spell
from Systems.Behaviors.projectile import ProjectileBehavior
from Systems.targeting import NearestEnemy
from SpellSystem.effects import Burn
from settings import PROJECTILE_SIZE

class Fireball(Spell):
    def __init__(self):
        super().__init__()
        
        self.targeting = NearestEnemy(
            max_range = 600
        )

        # Visual
        self.on_ground = False
        
        # Sound
        self.sound = pygame.mixer.Sound(
            "assets/sounds/spells/fireball.mp3"
        )
        
        # Stats
        self.stats.damage = 8
        self.stats.cooldown = 4.0
        self.stats.speed = 300
        self.stats.lifetime = 5.0
        self.stats.pierce = 0
        
        # Burn stats
        self.burn_damage = 2
        self.burn_duration = 5
        
        # Animation frames
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/fireball/fireball{i}.png"
                ).convert_alpha(),
                (PROJECTILE_SIZE, PROJECTILE_SIZE)
            )
            for i in range(1, 3)
        ]
        
    def cast(self, context):
        
        player = context.player
        
        result = self.targeting.select(context)
        
        if result is None:
            return None
        
        direction = (
            result.position
            - player.position
        )
        
        self.sound.play()        
        
        return FireballProjectile(
            player.position,
            direction,
            self.stats,
            self.burn_damage,
            self.burn_duration,
            self.frames
        )    
        
class FireballProjectile(ProjectileBehavior):
    def __init__(
        self,
        position,
        direction,
        stats,
        burn_damage,
        burn_duration,
        frames
    ):
        super().__init__(
            position,
            direction,
            stats.speed,
            stats.lifetime
        )
        
        self.damage = stats.damage
        self.pierce = stats.pierce
        
        self.hit_enemies = set()
        self.hitbox_radius = PROJECTILE_SIZE / 2
        
        # Burn stats
        self.burn_damage = burn_damage
        self.burn_duration = burn_duration
        
        # Animation frames
        self.frames = frames
                
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        # Rotate 
        angle = -pygame.Vector2(0, -1).angle_to(
            pygame.Vector2(direction)
        )
        
        self.frames = [
            pygame.transform.rotate(
                frame,
                angle
            )
            for frame in self.frames
        ]
                                        
    def update(self, dt):
        # Move
        super().update(dt)
        
        # Animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1
            
            if self.animation_frame >= len(self.frames):
                self.animation_frame = 0
                
    def on_hit(self, enemy):
        
        enemy.apply_effect(
            Burn(
                self.burn_damage,
                self.burn_duration,
                enemy.size
            )
        )
        
    def draw(self, screen, camera):
        screen_position = camera.apply(self.position)
        
        frame = self.frames[self.animation_frame]
        
        rect = frame.get_rect(
            center=(
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(frame, rect)