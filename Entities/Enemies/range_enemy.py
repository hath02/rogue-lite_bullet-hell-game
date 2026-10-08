import pygame

from Entities.Enemies.enemy import RangeEnemy, EnemyProjectile, tint_image
from settings import ENEMY_SIZE, PROJECTILE_SIZE

class Range(RangeEnemy):
    def __init__(self, position):
        super().__init__(position)
        
        # Change stats
        self.max_hp = 20
        self.hp = self.max_hp
        self.damage = 20
        
        self.exp_reward = 4
        
        # Activate projectile
        self.projectiles = []
                
        # Idle animation frames
        self.idle_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/range_enemy/idle_range1.png"
                ).convert_alpha(),
                (ENEMY_SIZE, ENEMY_SIZE)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/range_enemy/idle_range2.png"
                ).convert_alpha(),
                (ENEMY_SIZE, ENEMY_SIZE)
            )
        ]        
        
        # Attack animation frames
        self.attack_frames = [
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/range_enemy/attack_range1.png"
                ).convert_alpha(),
                (ENEMY_SIZE, ENEMY_SIZE)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/range_enemy/attack_range2.png"
                ).convert_alpha(),
                (ENEMY_SIZE, ENEMY_SIZE)
            ),
            
            pygame.transform.scale(
                pygame.image.load(
                    "assets/Enemy/range_enemy/attack_range3.png"
                ).convert_alpha(),
                (ENEMY_SIZE, ENEMY_SIZE)
            )
        ]   
        
        # Current animation
        self.current_animation = self.idle_frames
        
        # Animation stats
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.5
        
    def perform_attack(self, player):
        projectile = EnemyProjectile(
            self.position,
            player
        )

        self.projectiles.append(projectile)
        
    def update(self, dt, player):
        # Update common enemy stuffs
        super().update(dt, player)
        
        # Update projectiles
        for projectile in self.projectiles:
            projectile.update(dt)
        # Remove dead projectile
        self.projectiles = [
            projectile
            for projectile in self.projectiles
            if projectile.alive
        ]      
                  
    def draw(self, screen, camera):
        frame = self.current_animation[self.animation_frame]
        
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
                    
        # Draw projectile
        for projectile in self.projectiles:
            projectile.draw(screen, camera)
            