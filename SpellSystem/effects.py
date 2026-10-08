import pygame

def tint_image(image, color):
    tinted = image.copy()
    tinted.fill(color, special_flags = pygame.BLEND_RGB_MULT)
    return tinted

class Effect:
    def __init__(self, duration, stackable = False):
        self.duration = duration
        self.finished = False
        self.stackable = stackable
        self.target = None
    
    def apply(self, target):
        self.target = target
            
    def update(self, dt):
        pass
    
class Burn(Effect):
    def __init__(self, damage, duration, size):
        super().__init__(
            duration,
            stackable = True
        )
        

        self.damage = damage
        self.timer = 0.0
        
        # Animation
        self.frames = [
            pygame.image.load(
                "assets/Effects/burn/burn1.png"
            ).convert_alpha(),
            
            pygame.image.load(
                "assets/Effects/burn/burn2.png"
            ).convert_alpha()            
        ]
        
        # Scale burn to enemy size
        self.frames = [
            pygame.transform.scale(
                frame,
                (int(size), int(size))
            )
            for frame in self.frames
        ]
                
        self.animation_frame = 0
        self.animation_timer = 0.0
        self.animation_speed = 0.1
        
    def update(self, dt):
        if self.target is None:
            return
        
        self.duration -= dt
        self.timer += dt
        
        if self.timer >= 1.0:
            self.target.take_damage(self.damage)
            self.timer -= 1.0
            
        if self.duration <= 0:
            self.finished = True
            

        # Burn animation
        self.animation_timer += dt

        if self.animation_timer >= self.animation_speed:
            self.animation_timer -= self.animation_speed
            self.animation_frame += 1

            if self.animation_frame >= len(self.frames):
                self.animation_frame = 0
                
    def draw(self, screen, camera):
        if self.target is None:
            return
        
        frame = self.frames[self.animation_frame]
        
        screen_position = camera.apply(
            self.target.position
        )
        
        rect = frame.get_rect(
            center = (
                int(screen_position.x),
                int(screen_position.y)
            )
        )
        
        screen.blit(frame, rect)
        
class Slow(Effect):
    def __init__(self, duration, multiplier):
        super().__init__(
            duration,
            stackable = False  
        )
                
        self.multiplier = multiplier
        self.original_speed = None
        
    def apply(self, target):
        super().apply(target)
        
        # Save og speed
        self.original_speed = target.speed
        
        # Apply slow
        target.speed = (
            target.base_speed
            * self.multiplier
        )
        
    def update(self, dt):
        if self.target is None:
            return 
        
        self.duration -= dt
        
        if self.duration <= 0:
            # Restore speed
            self.target.speed = (
                self.target.base_speed
            )
            
            self.finished = True
            
    def draw(self, screen, camera):
        pass