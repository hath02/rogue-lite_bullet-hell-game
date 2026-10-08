import pygame

from settings import ENEMY_SIZE, PROJECTILE_SIZE
from Systems.Behaviors import ProjectileBehavior
from assets import load_image
from SpellSystem.effects import *

# Tinted image for take damage
def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags = pygame.BLEND_RGB_MULT)
    return tinted
    
class Enemy:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        
        self.max_hp = 30
        self.hp = self.max_hp
        
        self.damage = 15
        self.base_speed = 50
        self.speed = self.base_speed
        
        self.exp_reward = 3
        self.point = 1
        
        self.size = ENEMY_SIZE
        self.alive = True
        
        # Enemy hitbox
        self.hitbox_radius = ENEMY_SIZE / 4
        
        # Damage flash
        self.damage_flash = 0
        self.damage_flash_duration = 0.15

        # Effected effects
        self.effects = []
        
    def take_damage(self, damage):
        self.hp -= damage
        self.damage_flash = self.damage_flash_duration
        
        if self.hp <= 0:
            self.hp = 0
            self.die()
            
    def apply_effect(self, effect):
        if not effect.stackable:
            
            for existing in self.effects:
                
                if type(existing) == type(effect):
                    existing.duration = effect.duration
                    return
    
        effect.apply(self) 
        self.effects.append(effect)   
        
    def update_effects(self, dt):
        self.speed = self.base_speed

        for effect in self.effects:
            effect.update(dt)
            
            if isinstance(effect, Slow):
                self.speed *= effect.multiplier

        self.effects = [
            e for e in self.effects
            if not e.finished
        ]        
        
    def die(self):
        self.alive = False
                
    def update(self, dt, player):
        # Damage flash
        if self.damage_flash > 0:
            self.damage_flash -= dt
            
        self.update_effects(dt)
        
    def draw(self, screen, camera):   
        screen_position = camera.apply(self.position)

        rect = pygame.Rect(
            0,
            0,
            ENEMY_SIZE,
            ENEMY_SIZE
        )

        rect.center = (
            int(screen_position.x),
            int(screen_position.y)
        )

            
        pygame.draw.rect(
            screen,
            (0, 255, 0),
            rect
        )
        
        # Draw effects
        for effect in self.effects:
            effect.draw(screen, camera)
        
class ContactEnemy(Enemy):
    deals_contact_damage = True
    
    def update(self, dt, player):
        direction = player.position - self.position
        distance = direction.length()
        
        if distance > self.hitbox_radius:
            direction = direction.normalize()
            self.position += direction * self.speed * dt
            
        super().update(dt, player)
        
class RangeEnemy(Enemy):
    def __init__(self, position):
        super().__init__(position)
        
        self.attack_range = 300
        self.range_tolerance = 30
        
        self.is_attacking = False
        self.attack_cd = 3
        self.attack_cd_timer = 0
        self.attack_fired = False
        
        # Animation stats
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.5
                
    def attack(self, player):
        self.is_attacking = True
        self.current_animation = self.attack_frames
        self.animation_frame = 0
        self.animation_timer = 0
        self.attack_fired = False
        
    def perform_attack(self, player):
        # Child classes override this
        pass
        
    def update(self, dt, player):
        self.attack_cd_timer -= dt
        
        direction = player.position - self.position
        distance = direction.length()
        
        # Update movement
        if distance > self.attack_range + self.range_tolerance: # Too far -> move toward player
            direction = direction.normalize()
            self.position += direction * self.speed * dt
            
        elif distance < self.attack_range - self.range_tolerance: # Too close -> move away 
            direction = -direction.normalize()
            self.position += direction * self.speed * dt
            
        # Update attack
        elif(
            not self.is_attacking
            and self.attack_cd_timer <= 0
        ):
            self.attack(player)
            self.attack_cd_timer = self.attack_cd
            
        # Update animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.animation_frame += 1
            
            # Projectile fire in frame 3
            if(
                self.is_attacking
                and self.animation_frame == 2
                and not self.attack_fired
            ):
                self.perform_attack(player)
                self.attack_fired = True
                
            if self.animation_frame >= len(self.current_animation):
                
                if self.is_attacking:
                    # Attack animation finished
                    self.is_attacking =False
                    self.attack_fired = False
                    self.current_animation = self.idle_frames
                    self.animation_frame = 0
                    
                else:
                    # Idle animation loop
                    self.animation_frame = 0
            
        super().update(dt, player)
        
class EnemyProjectile(ProjectileBehavior):
    def __init__(self, position, target):

        direction = target.position - position
        
        super().__init__(
            position,
            direction,
            speed = 300,
            lifetime = 5
        )

        self.damage = 10
        
        self.hitbox_radius = PROJECTILE_SIZE / 2
        
        self.image = load_image(
            "assets/Enemy/enemy_projectile.png",
            (PROJECTILE_SIZE, PROJECTILE_SIZE)
        )  
        
        
    def draw(self, screen, camera):
        if not self.alive:
            return
        
        screen_position = camera.apply(self.position)
        
        rect = self.image.get_rect(
            center = (
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(self.image, rect)