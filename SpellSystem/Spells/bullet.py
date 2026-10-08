import pygame

from SpellSystem.spell import Spell
from Systems.Behaviors.projectile import ProjectileBehavior
from Systems.targeting import NearestEnemy
from settings import PROJECTILE_SIZE

class Bullet(Spell):
    def __init__(self):
        super().__init__()
        
        self.targeting = NearestEnemy(
            max_range = 600
        )
        
        # Visual
        self.on_ground = False
        
        # Sound
        self.sound = pygame.mixer.Sound(
            "assets/sounds/spells/bullet.mp3"
        )
        
        # Stats
        self.stats.damage = 10
        self.stats.cooldown = 1.5
        self.stats.speed = 500
        self.stats.lifetime = 4.0
        self.stats.pierce = 0
        
        self.level = 1
        
        # Assets
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    f"assets/Spells/bullet/bullet{i}.png"
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
        
        return BulletProjectile(
            player.position,
            direction,
            self.stats,
            self.frames
        )
    
    def get_stat_upgrades(self):
        upgrades = [
            {
                "id": "bullet-damage",
                "name": "Bullet #1",
                "description": "Damage +15"
            },
            {
                "id": "bullet-speed",
                "name": "Sniper Bullet",
                "description": "Speed +200, Cooldown -0.2"
            },
            {
                "id": "bullet-pierce",
                "name": "Piercing Bullet",
                "description": "Pierce +1"
            },
            {
                "id": "bullet-heavy",
                "name": "Heavy Bullet",
                "description": "Damage +30, Cooldown +0.5, Speed -100"
            }
        ]
        
        return [
            upgrade
            for upgrade in upgrades
            if upgrade["id"] not in self.selected_upgrade
        ]
        
    
    def apply_stats_upgrade(self, upgrade):
        if upgrade["id"] == "bullet-damage":
            self.stats.damage += 15
            
        elif upgrade["id"] == "bullet-speed":
            self.stats.speed += 200
            self.stats.cooldown -= 0.2
            
        elif upgrade["id"] == "bullet-pierce":
            self.stats.pierce += 1
            
        elif upgrade["id"] == "bullet-heavy":
            self.stats.damage += 30
            self.stats.cooldown += 0.5
            self.stats.speed -= 100
            
        self.selected_upgrade.add(upgrade["id"])
        
        
class BulletProjectile(ProjectileBehavior):
    def __init__(
        self,
        position,
        direction,
        stats,
        frames
    ):
        super().__init__(
            position,
            direction,
            stats.speed,
            stats.lifetime,
        )

        self.damage = stats.damage
        self.pierce = stats.pierce
        
        self.hit_enemies = set()
        self.hitbox_radius = PROJECTILE_SIZE / 2
          
        # Animation frames
        self.frames = frames
        
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1
        
        # Rotate bullet to face its direction
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
        # Movement
        super().update(dt)
        
        # Animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame += 1
            
            if self.animation_frame >= len(self.frames):
                self.animation_frame = 0
            
    def draw(self, screen, camera):
        screen_position = camera.apply(self.position)
        
        frame = self.frames[self.animation_frame]
        
        rect = frame.get_rect(center=(
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(frame, rect)
            
        