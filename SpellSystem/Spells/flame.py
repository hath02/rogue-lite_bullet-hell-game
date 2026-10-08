import pygame

from SpellSystem.spell import Spell
from Systems.Behaviors.cone import ConeBehavior
from Systems.targeting import NearestEnemy
from SpellSystem.effects import Burn
from settings import PLAYER_SIZE

class Flame(Spell):
    def __init__(self):
        super().__init__()
        
        self.targeting = NearestEnemy(
            max_range = 400
        )
        
        # Visual
        self.on_ground = False     
        
        # Sound
        self.sound = pygame.mixer.Sound(
            "assets/sounds/spells/flame.mp3"
        )
        
        self.sound.set_volume(0.5)
            
        # Stats
        self.stats.damage = 6
        self.stats.cooldown = 5.0
        self.stats.duration = 3.0
        
        # Flame stats
        self.range = 120
        self.angle = 45
        self.damage_interval = 0.3
        
        # Burn stats
        self.burn_damage = 2
        self.burn_duration = 8
        
        # Visual stats
        self.flame_length = 120
        self.flame_width = 80
        
        # Animation
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/flame/flamethrower{i}.png"
                ).convert_alpha(),
                (self.flame_width, self.flame_length)
            )
            for i in range(1, 3)
        ]
        
    def cast(self, context):
        
        result = self.targeting.select(context)
        
        if result is None:
            return None
        
        direction = (
            result.position
            - context.player.position
        )
        
        sound_channel = self.sound.play(-1)
        
        return FlameAttack(
            context.player,
            direction,
            self.stats,
            self.range,
            self.angle,
            self.damage_interval,
            self.burn_damage,
            self.burn_duration,
            self.flame_length,
            self.frames,
            sound_channel
        )
        
class FlameAttack(ConeBehavior):
    def __init__(
        self,
        player,
        direction,
        stats,
        range,
        angle,
        damage_interval,
        burn_damage,
        burn_duration,
        flame_length,
        frames,
        sound_channel
    ):
        super().__init__(
            player,
            direction,
            range,
            angle
        )
        
        self.collision_type = "cone"
        
        self.damage = stats.damage
        self.duration = stats.duration
        self.damage_interval = damage_interval
        
        # Sound
        self.sound_channel = sound_channel
        
        # Collision data
        self.hit_timers = {}
        
        # Burn stats
        self.burn_damage = burn_damage
        self.burn_duration = burn_duration
        
        self.flame_length = flame_length
        
        # Animation
        self.frames = frames
        
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        self.alive = True
    
    def update(self, dt):
        if not self.alive:
            return
        
        self.duration -= dt
            
        if self.duration <= 0:
            self.alive = False
            
            if self.sound_channel:
                self.sound_channel.stop()
                self.sound_channel = None
                
            return
        
         # Follow player
        self.position = (
            self.owner.position.copy()
            + self.direction 
            * 20
        )

        # Animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
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
        if not self.alive:
            return
        
        frame = self.frames[self.animation_frame]
        
        # Rotate flame toward enemy
        angle = -pygame.Vector2(0, -1).angle_to(
            self.direction
        )
        
        frame = pygame.transform.rotate(
            frame,
            angle
        )
        
        # Move visual center half the flame length forward
        visual_center = (
            self.position
            + self.direction * (self.flame_length / 2)
        )
            
        screen_position = camera.apply(visual_center)
        
        rect = frame.get_rect(
            center = (
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(frame, rect)