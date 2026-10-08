import pygame

class ConeBehavior:
    def __init__(
        self,
        owner,
        direction,
        range,
        angle
    ):
        self.owner = owner
        
        self.collision_type = "cone"
        
        self.position = (
            owner.position.copy()
        )
        
        self.direction = pygame.Vector2(direction)
        
        if self.direction.length_squared() > 0:
            self.direction.normalize_ip()
        
        self.range = range
        self.angle = angle
        
        self.alive = True
        
    def update(self, dt):
        
        # Follow player
        self.position = (
            self.owner.position.copy()
            + self.direction * 20
        )