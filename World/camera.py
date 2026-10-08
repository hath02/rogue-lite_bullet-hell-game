import pygame

class Camera:
    
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.position = pygame.Vector2(0, 0)
        
    def update(self, target):
        # Center the camera on the target position
        self.position = (
            target.position 
            - pygame.Vector2(
                self.screen_width / 2, 
                self.screen_height / 2
            )
        )
    
    def apply(self, world_position):
        # Convert world position to screen position based on the camera's position
        return world_position - self.position
    
    # Resize the camera when the window is resized    
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height