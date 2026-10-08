import pygame

from Entities.Enemies.enemy import ContactEnemy, tint_image
from settings import ENEMY_SIZE

class Tank(ContactEnemy):
    def __init__(self, position):
        super().__init__(position)
        
        # Changed stats
        self.max_hp = 100
        self.hp = self.max_hp
        self.damage = 40
        self.base_speed = 30
        self.speed = self.base_speed
        
        self.exp_reward = 6
        
        self.size = ENEMY_SIZE * 2
        
        self.hitbox_radius = ENEMY_SIZE / 2
        
        # Animation frame
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/tank_enemy/tank_enemy1.png"
                ).convert_alpha(),
                (self.size, self.size)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/tank_enemy/tank_enemy2.png"
                ).convert_alpha(),
                (self.size, self.size)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/tank_enemy/tank_enemy3.png"
                ).convert_alpha(),
                (self.size, self.size)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/tank_enemy/tank_enemy4.png"
                ).convert_alpha(),
                (self.size, self.size)
            )            
        ]
        
        # Animation stats
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.5
        
    def update(self, dt, player):
        # Update animation
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.animation_frame += 1
            
            if self.animation_frame >= len(self.frames):
                self.animation_frame = 0
                
        # Update common enemy stuffs
        super().update(dt, player)
        
    def draw(self, screen, camera):
        frame = self.frames[self.animation_frame]
        
        # Damage flash
        if self.damage_flash > 0:
            frame = tint_image(frame, (255,100,100))
                    
        screen_position = camera.apply(self.position)

        
        rect = frame.get_rect(
            center = (
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(frame, rect)
        
        # Draw effects
        for effect in self.effects:
            effect.draw(screen, camera)