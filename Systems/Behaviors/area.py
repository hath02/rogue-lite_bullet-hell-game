import pygame

from Systems.Behaviors.behavior import Behavior

class AreaBehavior(Behavior):
    def __init__(
        self,
        position,
        radius,
        duration,
        owner = None
    ):
        super().__init__()
        
        self.collision_type = "area"
        self.owner = owner
        
        if owner:
            self.position = owner.position.copy()
        else:
            self.position = pygame.Vector2(position)
        
        self.radius = radius
        self.duration = duration
        
        self.alive = True
        
    def update(self, dt):
        if self.owner:
            self.position = (
                self.owner.position.copy()
            )
            
        self.duration -= dt
        
        if self.duration <= 0:
            self.alive = False
            
    def destroy(self):
        self.alive = False