import pygame

import UI.font as fonts

class Pause:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Buttons
        self.continue_btn = pygame.Rect(
            0, 0, 250, 70
        )
        
        self.quit_btn = pygame.Rect(
            0, 0, 250, 70
        )

        self.update_btn_position()
        
    def update_btn_position(self):
        center_x = self.screen_width // 2
        
        self.continue_btn.center = (
            center_x,
            self.screen_height // 2 
        )    
        
        self.quit_btn.center = (
            center_x,
            self.screen_height // 2 + 100
        )
        
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.update_btn_position()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                return "continue"
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                if self.continue_btn.collidepoint(event.pos):
                    return "continue"
                
                if self.quit_btn.collidepoint(event.pos):
                    return "quit"
                
        return None
    
    def draw(self, screen):
        overlay = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA
        )
        
        overlay.fill((0, 0, 0, 160))
        
        screen.blit(
            overlay,
            (0, 0)
        )
        
        # Title
        title = fonts.TITLE_FONT.render(
            "PAUSED",
            True,
            (255, 255, 255)
        )
        
        title_rect = title.get_rect(
            center = (
                self.screen_width // 2,
                self.screen_height // 2 - 250
            )
        )
        
        screen.blit(title, title_rect)
        
        # Continue btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.continue_btn
        )
        
        continue_text = fonts.BUTTON_FONT.render(
            "CONTINUE",
            True,
            (255, 255, 255)
        )
        
        continue_rect = continue_text.get_rect(
            center = self.continue_btn.center
        )
        
        screen.blit(
            continue_text,
            continue_rect
        )
        
        # Quit btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.quit_btn
        )
        
        quit_text = fonts.BUTTON_FONT.render(
            "QUIT",
            True,
            (255, 255, 255)
        )
        
        quit_rect = quit_text.get_rect(
            center = self.quit_btn.center
        )
        
        screen.blit(
            quit_text,
            quit_rect
        )
        
        