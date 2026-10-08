import pygame

import UI.font as fonts

class SelectMode:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Buttons
        self.challenges_btn = pygame.Rect(
            0, 0, 300, 80
        )
        
        self.endless_btn = pygame.Rect(
            0, 0, 300, 80
        )
        
        self.back_btn = pygame.Rect(
            0, 0, 200, 60
        )
        
        self.update_position()
        
    def update_position(self):
        center_x  = self.screen_width // 2

        self.challenges_btn.center = (
            center_x,
            self.screen_height // 2 - 70
        )
        
        self.endless_btn.center = (
            center_x,
            self.screen_height // 2 + 30
        )        
            
        self.back_btn.center = (
            center_x,
            self.screen_height - 100
        )
        
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.update_position()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                if self.challenges_btn.collidepoint(event.pos):
                    return "challenges"
                
                if self.endless_btn. collidepoint(event.pos):
                    return "endless"
                    
                if self.back_btn.collidepoint(event.pos):
                    return "back"
                
        return None    
    
    def draw(self, screen):
        screen.fill((0, 0, 0))

        title = fonts.TITLE_FONT.render(
            "SELECT MODE",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                150
            )
        )

        screen.blit(title, title_rect)

        # Challenges btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.challenges_btn
        )

        text = fonts.BUTTON_FONT.render(
            "CHALLENGES",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.challenges_btn.center
        )

        screen.blit(text, text_rect)
                
        # Endless btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.endless_btn
        )

        text = fonts.BUTTON_FONT.render(
            "ENDLESS",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.endless_btn.center
        )

        screen.blit(text, text_rect)
        
        # Back btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.back_btn
        )

        text = fonts.BUTTON_FONT.render(
            "BACK",
            True,
            (255, 255, 255)
        )

        text_rect = text.get_rect(
            center=self.back_btn.center
        )

        screen.blit(text, text_rect)