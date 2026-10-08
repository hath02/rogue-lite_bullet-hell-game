import pygame

class FallingBehavior:
    def __init__(
        self,
        position,
        target_position,
        speed
    ):
        self.position = pygame.Vector2(position)
        self.target_position = pygame.Vector2(target_position)
        
        direction = self.target_position - self.position
        
        if direction.length_squared() > 0:
            self.direction = direction.normalize()
        else:
            self.direction = pygame.Vector2()
            
        self.speed = speed
        self.alive = True
        self.reached_target = False
        
    def update(self, dt):
        if not self.alive:
            return
        
        distance  = self.position.distance_to(self.target_position)
        movement = self.speed * dt
        
        # Reached target
        if distance <= movement:
            self.position = (
                self.target_position.copy()
            )
            
            self.reached_target = True
            self.alive = False
            return
        
        self.position += (
            self.direction
            * movement
        )