import pygame, math, os

from SpellSystem.spell import Spell
from Systems.Behaviors.falling import FallingBehavior
from Systems.targeting import EnemyCluster

from settings import METEOR_SIZE

class Meteor(Spell):
    def __init__(self):
        super().__init__()
        
        self.targeting = EnemyCluster(
            radius = 150,
            max_range = 500
        )

        # Stats
        self.stats.damage = 35
        self.stats.cooldown = 12.0
        self.stats.speed = 2500
        
        # Explosion stats
        self.explosion_duration = 0.75
        self.explosion_radius = METEOR_SIZE * 0.75
        
        # Meteor animation
        self.meteor_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/meteor/meteor{i}.png"
                ).convert_alpha(),
                (METEOR_SIZE, METEOR_SIZE)
            )
            for i in range(1, 3)
        ]
        
        self.meteor_frame = 0
        self.meteor_animation_timer = 0
        self.meteor_animation_speed = 0.08
        
        # Explostion animation
        self.explosion_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/explosion/explosion{i}.png"
                ).convert_alpha(),
                (METEOR_SIZE, METEOR_SIZE)
            )
            for i in range(1, 6)
        ]
        
        self.explosion_frame = 0
        self.explosion_animation_timer = 0
        self.explosion_animation_speed = (
            self.explosion_duration
            / len(self.explosion_frames)
        )
        
        # Aftershock
        self.aftershock_image = pygame.transform.scale(
            pygame.image.load(
                "assets/Spells/explosion/aftershock.png"
            ).convert_alpha(),
            (METEOR_SIZE, METEOR_SIZE)
        )
        
        # Aftershock
        self.aftershock_duration = 1.0
        self.aftershock_timer = 0

        self.aftershock_alpha = 255
        self.aftershock_fade_speed = (
            255 / self.aftershock_duration
        )
        
    def cast(self, context):
        
        result = self.targeting.select(
            context
        )
        
        if result is None:
            return None
        
        target = result.position
        
        # Spawn
        direction = pygame.Vector2(-1, 1).normalize()
        
        spawn_position = (
            target - direction * 1500
        )
        
        return MeteorObject(
            spawn_position,
            target,
            self.stats,
            self.explosion_radius,
            self.explosion_duration,
            self.meteor_frames,
            self.explosion_frames,
            self.aftershock_image
        )
        
class MeteorObject:
    def __init__(
        self,
        position,
        target,
        stats,
        explosion_radius,
        explosion_duration,
        meteor_frames,
        explosion_frames,
        aftershock_image,
    ):
        # Position
        self.position = pygame.Vector2(position)
        self.target = pygame.Vector2(target)
        
        # Movement
        self.falling = FallingBehavior(
            position,
            target,
            stats.speed
        )
        
        # Visual
        self.on_ground = False
            
        # Stats
        self.damage = stats.damage
        self.explosion_radius = explosion_radius
        
        self.explosion_duration = (
            explosion_duration
        )
        
        # State
        self.state = "falling"
        self.alive = True
        
        # Collision
        self.collision_type = "none"
        self.radius = 0
        self.hit_timers = {}
        self.damage_interval = 0.2
        
        # Meteor animation
        self.meteor_frames = meteor_frames
        
        self.meteor_frame = 0
        self.meteor_timer = 0
        self.meteor_speed = 0.08
        
        # Explosion animation
        self.explosion_frames = explosion_frames
        
        self.explosion_frame = 0
        self.explosion_timer = 0
        
        self.explosion_speed = (
            explosion_duration / 
            len(self.explosion_frames)
        )
        
        # Aftershock animation
        self.aftershock_image = (
            aftershock_image
        )
        
        self.aftershock_duration = 1.0
        self.aftershock_timer = 0

        self.aftershock_alpha = 255
        
        self.aftershock_fade_speed = (
            255 / self.aftershock_duration
        )
        
    def update(self, dt):
        if self.state == "falling":
            self.update_falling(dt)
                
        elif self.state == "exploding":
            self.update_explosion(dt)
            
        elif self.state == "aftershock":
            self.update_aftershock(dt)
    
    def update_falling(self, dt):
        self.falling.update(dt)
        
        self.position = (
            self.falling.position.copy()
        )           
        
        # Animation
        self.meteor_timer += dt
        
        if self.meteor_timer >= self.meteor_speed:
            self.meteor_timer -= self.meteor_speed
            self.meteor_frame += 1
            
            if self.meteor_frame >= len(
                self.meteor_frames
            ):
                self.meteor_frame = 0
                
        # Hit ground
        if self.falling.reached_target:
            self.start_explosion()
                
    def start_explosion(self):
        self.state = "exploding"
        
        self.explosion_frame = 0
        self.explosion_timer = 0
        
        # Enable AOE collision
        self.collision_type = "area"
        
        self.radius = (
            self.explosion_radius
        )
        
        self.hit_timers = {}
            
    def update_explosion(self, dt):
        self.explosion_timer += dt
        
        if self.explosion_timer >= self.explosion_speed:
            self.explosion_timer = 0
            self.explosion_frame += 1
            
        if self.explosion_frame >= len(
            self.explosion_frames
        ):
            self.explosion_frame = (
                len(self.explosion_frames) - 1
            )
            
            self.start_aftershock()
    
    def start_aftershock(self):
        self.state = "aftershock"
        
        self.on_ground = True
        
        self.collision_type = "none"
        
        self.aftershock_timer = 0
        
        self.aftershock_alpha = 255
            
    def update_aftershock(self, dt):
        self.aftershock_timer += dt
        
        self.aftershock_alpha -= (
            self.aftershock_fade_speed
            * dt
        )       
        
        if self.aftershock_alpha <= 0:
            self.aftershock_alpha = 0
            
        if self.aftershock_timer >= (
            self.aftershock_duration
        ):
            self.alive = False
            self.collision_type = "none"
    
    def on_hit(self, enemy):
        pass
    
    def draw(self, screen, camera):
        pos = camera.apply(
            self.position
        )
        
        # Falling
        if self.state == "falling":
            image = self.meteor_frames[
                self.meteor_frame
            ]
        
        # Exploding    
        elif self.state == "exploding":
            image = self.explosion_frames[
                self.explosion_frame
            ]
        
        # Aftershock    
        elif self.state == "aftershock":
            image = self.aftershock_image.copy()
            
            image.set_alpha(
                int(self.aftershock_alpha)
            )
            
        rect = image.get_rect(
            center = (
                int(pos.x),
                int(pos.y)
            )
        )
    
        screen.blit(
                image,
                rect
        )