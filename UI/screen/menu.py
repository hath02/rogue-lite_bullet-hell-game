import pygame

import UI.font as fonts

class MainMenu:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.start_button = pygame.Rect(
            screen_width // 2 - 150,
            screen_height // 2 - 40,
            300,
            70
        )

        self.exit_button = pygame.Rect(
            screen_width // 2 - 150,
            screen_height // 2 + 60,
            300,
            70
        )

        self.title_bg = pygame.transform.scale(
            pygame.image.load(
                "assets/UI/title_bg.png"
            ).convert_alpha(),
            (640, 192)
        )
        
    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.start_button.center = (
            screen_width // 2,
            screen_height // 2 - 5
        )

        self.exit_button.center = (
            screen_width // 2,
            screen_height // 2 + 95
        )

    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 1:

                if self.start_button.collidepoint(event.pos):
                    return "start"
                
                if self.exit_button.collidepoint(event.pos):
                    return "exit"

        return None

    def draw(self, screen):

        screen.fill((40, 40, 40))

        # Title
        title = fonts.TITLE_FONT.render(
            "BULLET HELL",
            True,
            (255, 255, 255)
        )

        title_rect = title.get_rect(
            center=(
                self.screen_width // 2,
                150
            )
        )

        screen.blit(
            title, 
            title_rect
        )

        # Start button
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            self.start_button
        )

        start_text = fonts.BUTTON_FONT.render(
            "START",
            True,
            (255, 255, 255)
        )

        start_rect = start_text.get_rect(
            center=self.start_button.center
        )

        screen.blit(start_text, start_rect)

        # Exit button
        pygame.draw.rect(
            screen,
            (50, 50, 50),
            self.exit_button
        )

        exit_text = fonts.BUTTON_FONT.render(
            "EXIT",
            True,
            (255, 255, 255)
        )

        exit_rect = exit_text.get_rect(
            center=self.exit_button.center
        )

        screen.blit(exit_text, exit_rect)