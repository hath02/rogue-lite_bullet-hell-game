import pygame

import UI.font as fonts

CARD_W, CARD_H, GAP = 280, 340, 30


def wrap_text(text, font, max_width):
    lines, line = [], ""

    for word in text.split():
        test = (line + " " + word).strip()

        if font.size(test)[0] <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = word

    if line:
        lines.append(line)

    return lines


class LevelUp:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def resize(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

    def get_rects(self, count):
        total = count * CARD_W + (count - 1) * GAP
        start_x = (self.screen_width - total) // 2
        y = self.screen_height // 2 - CARD_H // 2

        return [
            pygame.Rect(start_x + i * (CARD_W + GAP), y, CARD_W, CARD_H)
            for i in range(count)
        ]

    def handle_event(self, event, choices):
        """Returns the index of the chosen card, or None."""
        if event.type == pygame.KEYDOWN:
            for i, key in enumerate((pygame.K_1, pygame.K_2, pygame.K_3)):
                if event.key == key and i < len(choices):
                    return i

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.get_rects(len(choices))):
                if rect.collidepoint(event.pos):
                    return i

        return None

    @staticmethod
    def card_text(choice):
        upgrade = choice["upgrade"]

        if choice["type"] == "new_spell":
            return choice["spell_class"].__name__, upgrade["name"], upgrade["description"]

        spell = choice["spell"]
        title = f"{type(spell).__name__} Lv{spell.level + 1}"
        return title, upgrade["name"], upgrade["description"]

    def draw(self, screen, choices):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        title = fonts.TITLE_FONT.render("LEVEL UP!", True, (255, 255, 255))
        screen.blit(
            title,
            title.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - CARD_H // 2 - 60))
        )

        mouse = pygame.mouse.get_pos()

        for i, (choice, rect) in enumerate(zip(choices, self.get_rects(len(choices)))):
            hovered = rect.collidepoint(mouse)

            pygame.draw.rect(screen, (95, 95, 95) if hovered else (70, 70, 70), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)

            head, name, desc = self.card_text(choice)
            y = rect.y + 20
            max_w = CARD_W - 40

            for text, font, color in (
                (head, fonts.HUD_FONT, (255, 220, 120)),
                (name, fonts.HUD_FONT, (255, 255, 255)),
                (desc, fonts.DESCRIPTION_FONT, (200, 200, 200)),
            ):
                for line in wrap_text(text, font, max_w):
                    surf = font.render(line, True, color)
                    screen.blit(surf, (rect.x + 20, y))
                    y += surf.get_height() + 4
                y += 14

            key = fonts.DESCRIPTION_FONT.render(f"[{i + 1}]", True, (150, 150, 150))
            screen.blit(key, key.get_rect(midbottom=(rect.centerx, rect.bottom - 10)))