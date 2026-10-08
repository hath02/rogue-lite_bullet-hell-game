import pygame

from settings import PLAYER_SIZE
from Entities.Player.stats import Stats
from Entities.Player.spellbook import Spellbook

from SpellSystem.Spells.__init__ import *

from SpellSystem.spellController import SpellController

# Tinted image for take damage
def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags = pygame.BLEND_RGB_MULT)
    return tinted
    
class Player:
    def __init__(self):
        self.position = pygame.Vector2(0, 0)
        self.stats = Stats()
        
        self.alive = True
        
        # Player hitbox
        self.hitbox_radius = PLAYER_SIZE / 4
        
        # Spell
        self.default_spell = Bullet()
        self.spellbook = Spellbook(self.default_spell)
    
        self.spell_objects = []
        self.spell_controller = SpellController(self)
        
        # Idle animation frames
        self.idle_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Player/idle_player1.png"
                ).convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Player/idle_player2.png"
                ).convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            )
        ]
        
        # Movement animation frames
        self.move_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Player/move_player1.png"
                ).convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Player/move_player2.png"
                ).convert_alpha(),
                (PLAYER_SIZE, PLAYER_SIZE)
            )
        ]
            
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        
        # Player facing direction
        self.facing_right = True
        self.facing_direction = pygame.Vector2(0, -1)
        
        # Current frame to display
        self.moving = False

        # Damage flash
        self.damage_flash = 0
        self.damage_flash_duration = 0.15
        
        self.invuln_timer = 0
        self.invuln_duration = 0.5
                
    def take_damage(self, damage):
        if self.invuln_timer > 0 or not self.alive:
            return

        self.stats.hp -= damage
        self.damage_flash = self.damage_flash_duration
        self.invuln_timer = self.invuln_duration

        if self.stats.hp <= 0:
            self.stats.hp = 0
            self.die()
            
    def die(self):
        self.alive = False
            
    def update(self, dt, enemies):
        self.move(dt)
        
        # Spell cooldown + casting
        self.spell_controller.update(
            dt, 
            enemies
        )
            
        # Update animation based on movement
        if self.moving:
            frame = self.move_frames
        else:
            frame = self.idle_frames
            
        # Update animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.animation_frame += 1
            
            if self.animation_frame >= len(frame):
                self.animation_frame = 0
                
        # Damage flash
        if self.damage_flash > 0:
            self.damage_flash -= dt
        
        if self.invuln_timer > 0:
            self.invuln_timer -= dt

    def move(self, dt):
        direction = pygame.Vector2(0, 0)
        
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_s]:
            direction.y += 1
        if keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_d]:
            direction.x += 1
        
        # Check if the player is moving
        self.moving = direction.length_squared() > 0
        
        if self.moving:
            direction = direction.normalize()
            
            # Move the player based on speed and delta time
            self.position += (
                direction 
                * self.stats.speed 
                * dt
            )
            
            self.facing_direction = direction
        
        # Update facing direction based on movement        
        if direction.x > 0:
            self.facing_right = True
            
        elif direction.x < 0:
            self.facing_right = False

    def draw(self, screen, camera):
        # Choose the correct frame based on movement
        if self.moving:
            frame = self.move_frames[self.animation_frame]
        else:
            frame = self.idle_frames[self.animation_frame]
            
        # Flip the frame if facing left
        if not self.facing_right:
            frame = pygame.transform.flip(frame, True, False)
        
        # Damage flash
        if self.damage_flash > 0:
            frame = tint_image(frame, (255,100,100))
                
        screen_position = (
            self.position 
            - camera.position
        )
        
        screen.blit(
            frame,
            (
                int(
                    screen_position.x 
                    - PLAYER_SIZE // 2
                ),
                int(
                    screen_position.y 
                    - PLAYER_SIZE // 2
                )
            )
        )