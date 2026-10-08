import pygame

from World.mapManager import get_map_names
import UI.font as fonts

class SelectMap:
    def __init__(
        self,
        screen_width,
        screen_height
    ):
        
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.maps = get_map_names()
        
        self.selected_map = 0
        
        self.map_buttons = []
        
        self.back_btn = pygame.Rect(
            0, 0, 200, 60
        )
        
        self.button_width = 300
        self.button_height = 180
        self.button_gap = 30
        
        # Horizontal scrolling
        self.scroll_offset = 0
        
        self.update_position()
        
    def update_position(self):
        center_x  = self.screen_width // 2
        center_y = self.screen_height // 2
        
        self.map_buttons = []
        
        start_x = 100 + self.scroll_offset
        
        for i in range(len(self.maps)):
            button = pygame.Rect(
                0,
                0,
                self.button_width,
                self.button_height
            )
            
            button.center = (
                start_x
                + i * (self.button_width + self.button_gap)
                + self.button_width // 2
                + self.scroll_offset,
                center_y
            )
            
            self.map_buttons.append(button)
            
        self.back_btn.center = (
            center_x,
            self.screen_height - 100
        )
        
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.update_position()
    
    def scroll(self, amount):
        self.scroll_offset += amount
        
        #Calculate total width
        total_width = (
            len(self.maps) * self.button_width
            + (len(self.maps) - 1) * self.button_gap
        )    
        
        center_x = self.screen_width // 2
        
        # Maxium scroll
        max_srcoll = max(
            0,
            total_width - self.screen_width + 200
        )
        
        # Keep scroll inside limits
        self.scroll_offset = max(
            - max_srcoll,
            min(0, self.scroll_offset)
        )
        
        self.update_position()
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "back"
        
        # Mouse wheel
        if event.type == pygame.MOUSEWHEEL:
            self.scroll(event.y * 100)    
            
        # Mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                
                for i, button in enumerate(
                    self.map_buttons
                ):
                    if button.collidepoint(event.pos):
                        return self.maps[i]
                    
                if self.back_btn.collidepoint(event.pos):
                    return "back"
                
        return None
    
    def draw(self, screen):
        screen.fill((0, 0, 0))

        title = fonts.TITLE_FONT.render(
            "SELECT MAP",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                self.screen_height // 2 - 250
            )
        )

        screen.blit(title, title_rect)

        for i, button in enumerate(
            self.map_buttons
        ):
            pygame.draw.rect(
                screen,
                (70, 70, 70),
                button
            )

            text = fonts.BUTTON_FONT.render(
                self.maps[i].upper(),
                True,
                (255, 255, 255)
            )

            text_rect = text.get_rect(
                center=button.center
            )

            screen.blit(text, text_rect)

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