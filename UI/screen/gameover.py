import pygame

import UI.font as fonts 

class GameOver:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Buttons
        self.retry_btn = pygame.Rect(
            0, 0, 250, 70
        )
        
        self.select_btn = pygame.Rect(
            0, 0, 250, 70
        )
        
        self.quit_btn = pygame.Rect(
            0, 0, 250, 70
        )
        
        self.update_btn_position()
        
    def update_btn_position(self):
        center_x = self.screen_width // 2
        
        self.retry_btn.center = (
            center_x,
            self.screen_height // 2 -100
        )
        
        self.select_btn.center = (
            center_x,
            self.screen_height // 2 
        )
        
        self.quit_btn.center = (
            center_x,
            self.screen_height // 2 + 100
        )
        
    def resize(self, screen_width, screen_heigth):
        self.screen_width = screen_width
        self.screen_height = screen_heigth
        
        self.update_btn_position()
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.retry_btn.collidepoint(event.pos):
                    return "retry"
                
                if self.select_btn.collidepoint(event.pos):
                    return "select"
                
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
            "YOU DIE!",
            True,
            (220, 50, 50)
        )
        
        title_rect = title.get_rect(
            center = (
                self.screen_width // 2,
                self.screen_height // 2 - 250
            )
        )
        
        screen.blit(title, title_rect)
        
        # Retry btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.retry_btn
        )
        
        retry_text = fonts.BUTTON_FONT.render(
            "RETRY",
            True,
            (255, 255, 255)
        )
        
        retry_rect = retry_text.get_rect(
            center = self.retry_btn.center
        )
        
        screen.blit(
            retry_text,
            retry_rect
        )
        
        # Menu btn
        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.select_btn
        )
        
        select_text = fonts.BUTTON_FONT.render(
            "SELECT MODE",
            True,
            (255, 255, 255)
        )
        
        select_rect = select_text.get_rect(
            center = self.select_btn.center
        )
        
        screen.blit(
            select_text,
            select_rect
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
        
        