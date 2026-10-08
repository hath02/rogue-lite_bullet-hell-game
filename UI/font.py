import pygame

FONT_PATH = "assets/Font/bullet_hell_font.ttf"

TITLE_FONT = None
BUTTON_FONT = None
DESCRIPTION_FONT = None
HUD_FONT = None

def init_fonts():
    global TITLE_FONT
    global BUTTON_FONT
    global DESCRIPTION_FONT
    global HUD_FONT
    
    TITLE_FONT = pygame.font.Font(FONT_PATH, 72)
    BUTTON_FONT = pygame.font.Font(FONT_PATH, 45)
    DESCRIPTION_FONT = pygame.font.Font(FONT_PATH, 28)
    HUD_FONT = pygame.font.Font(FONT_PATH, 32)
    
def get_font(size):
    return pygame.font.Font(FONT_PATH, size)