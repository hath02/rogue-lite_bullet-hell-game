import pygame, math

class Orbitbehavior:
    def __init__(
        self,
        center,
        radius,
        angular_speed,
        angle = 0
    ):
        self.center = pygame.Vector2(center)
        self.position = (
            center.position
            + pygame.Vector2(radius, 0)
        )
        
        self.radius = radius
        self.angular_speed = angular_speed
        self.angle = angle
        
        self.alive = True
        
    def update(self, dt):
        if not self.alive:
            return
        
        self.angle += (
            self.angular_speed 
            * dt
        )
        
        center_position = self.center.position
        
        self.position.x = (
            center_position.x
            + math.cos(self.angle) 
            * self.radius
        )
        
        self.position.y = (
            center_position.y
            + math.sin(self.angle) 
            * self.radius
        )