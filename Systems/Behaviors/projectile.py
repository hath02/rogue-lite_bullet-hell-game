import pygame

from Systems.Behaviors.behavior import Behavior

class ProjectileBehavior(Behavior):
    def __init__(
        self,
        position,
        direction,
        speed,
        lifetime
    ):
        super().__init__()
        
        self.collision_type = "projectile"
        
        self.position = pygame.Vector2(position)
        self.direction = pygame.Vector2(direction)
        
        if self.direction.length_squared() > 0:
            self.direction = self.direction.normalize()

        self.speed = speed
        self.lifetime = lifetime
        
        # Collision
        self.hitbox_radius = 10.0
        
    def update(self, dt):
        # Movement
        self.position += (
            self.direction 
            * self.speed 
            * dt
        )
        
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.destroy()
            
    def destroy(self):
        self.alive = False