import pygame

# SETTINGS
from settings import FPS, PROJECTILE_SIZE

# UI
from UI.screen.__init__ import *
from UI.font import *
import UI.font as fonts
from UI.screen.levelup import LevelUp

# WORLD
from World.world import World
from World.camera import Camera
from World.mapManager import (
    get_map, 
    get_map_names,
    get_map_ambient
)

# GAMEMODES
from Game.gamemode import Timed, Endless

# ENTITIES
from Entities.Player.player import Player
from Entities.Enemies.spawner import Spawner

# SYSTEMS
from Systems.collision import CollisionSystem
from Systems.Audio.audioManager import AudioManager

from Systems.Progression.levelupSystem import LevelUpSystem
from Systems.Progression.upgradeSystem import UpgradeSystem

class Game:
    def __init__(self):
        # Displayer settings
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.set_num_channels(AudioManager.Channel.TOTAL)
        init_fonts()
        
        self.screen_width = 1024       
        self.screen_height = 768
        
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), 
            pygame.RESIZABLE
        )
        
        pygame.display.set_caption("Bullet Hell Game")
        self.clock = pygame.time.Clock()
        
        # Menu settings
        self.menu = MainMenu(
            self.screen_width, 
            self.screen_height
        )
        
        self.select_mode = SelectMode(
            self.screen_width,
            self.screen_height
        )
        
        self.select_map = SelectMap(
            self.screen_width,
            self.screen_height
        )
                
        self.pause = Pause(
            self.screen_width,
            self.screen_height
        )
        
        self.gameover = GameOver(
            self.screen_width,
            self.screen_height
        )

        self.levelup = LevelUp(
            self.screen_width, 
            self.screen_height
        )
        
        # Game objects
        self.world = None
        self.player = Player()
    
        self.enemies = []
        self.spawner = Spawner()
        
        self.game_mode = None
        self.selected_map = None
        
        self.camera = Camera(
            self.screen_width, 
            self.screen_height
        )
        
        # Systems
        self.collision_system = CollisionSystem()
        self.sound = AudioManager()
        
        self.spellbook = self.player.spellbook

        self.upgrade_system = UpgradeSystem(
            self.spellbook
        )

        self.level_up_system = LevelUpSystem(
            self.player,
            self.spellbook,
            self.upgrade_system
        )
        
        # Game state
        self.running = True
        self.game_state = "menu"
        self.elapsed_time = 0.0
        
    # Start game    
    def start_game(self):
        self.game_state = "game"
        
        self.sound.play_ambient(
            get_map_ambient(self.game_mode.map_name)
        )
        
        self.world = World(
            get_map(self.game_mode.map_name)
        )
        
        self.player = Player()
                
        self.spellbook = self.player.spellbook
        self.upgrade_system = UpgradeSystem(self.spellbook)
        self.level_up_system = LevelUpSystem(
            self.player, 
            self.spellbook, 
            self.upgrade_system
        )
        
        
        self.enemies = []
        self.spawner = Spawner()
        self.elapsed_time = 0.0
                  
    # Game events
    def handle_events(self):
        for event in pygame.event.get():
            
            # Quit window
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Handle window resize event
            if event.type == pygame.VIDEORESIZE:
                    
                self.screen_width = event.w
                self.screen_height = event.h
                    
                self.screen = pygame.display.set_mode(
                    (self.screen_width, self.screen_height), 
                    pygame.RESIZABLE
                )
                    
                self.camera.resize(
                    self.screen_width, 
                    self.screen_height
                )
                    
                self.menu.resize(
                    self.screen_width,
                    self.screen_height
                )
                
                self.select_mode.resize(
                    self.screen_width,
                    self.screen_height
                )
                
                self.select_map.resize(
                    self.screen_width,
                    self.screen_height
                )
                
                self.pause.resize(
                    self.screen_width,
                    self.screen_height
                )
                
                
                self.gameover.resize(
                    self.screen_width,
                    self.screen_height
                )
                
                self.levelup.resize(
                    self.screen_width, 
                    self.screen_height
                )
                
                continue
                        
            # Menu
            if self.game_state == "menu":
                
                result = self.menu.handle_event(event)
                
                if result == "start":
                    self.game_state = "mode_select"
                        
                elif result == "exit":
                    self.running = False
                        
                continue  # Skip the rest of the event handling for this frame
            
            # Mode select
            elif self.game_state == "mode_select":
                
                result = self.select_mode.handle_event(event)
                                
                if result == "challenges":
                    self.game_state = "map_select"
                    
                if result == "endless":
                    self.game_mode = Endless(
                        get_map_names()
                    )   
                    
                    self.start_game()
                    
                elif result == "back":
                    self.game_state = "menu"
                    
                continue
                
            # Map select    
            elif self.game_state == "map_select":
                
                result = self.select_map.handle_event(event)
                
                if result == "back":
                    self.game_state = "mode_select"
                    
                elif result is not None:
                    self.selected_map = result
                    
                    self.game_mode = Timed(
                        self.selected_map
                    )
                    
                    self.start_game()
                    
                continue
            
            # Game
            elif self.game_state == "game":

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_state = "pause"

                continue
            
            # Pause            
            elif self.game_state == "pause":
                
                result = self.pause.handle_event(event)
                
                if result == "continue":
                    self.game_state = "game"
                    
                elif result == "quit":
                    self.game_state = "menu"
            
            
            # Level up
            elif self.game_state == "levelup":
                index = self.levelup.handle_event(
                    event,
                    self.level_up_system.pending_choices
                )

                if index is not None:
                    choice = self.level_up_system.pending_choices[index]
                    self.level_up_system.apply_choice(choice)

                    if not self.level_up_system.awaiting_choice:
                        self.game_state = "game"
                                
            # Gameover
            elif self.game_state == "gameover":
                result = self.gameover.handle_event(event)
                
                if result == "retry":
                    self.start_game()
                    
                elif result == "select":
                    self.game_state = "mode_select"
                    
                elif result == "quit":
                    self.game_state = "menu"
                                        
    # Update game state
    def update(self, dt):
        if self.game_state == "game":
            
            self.elapsed_time += dt
            
            # Game mode
            result = self.game_mode.update(
                self.elapsed_time
            )
            
            if result == "win":
                self.game_state = "gameover"
                return
            
            # Spawn enemies
            self.spawner.update(
                dt,
                self.player,
                self.enemies,
                self.elapsed_time
            )
                        
            # Spawn player
            self.player.update(
                dt,
                self.enemies
            )
    
            
            # Update enemies 
            for enemy in self.enemies:
                enemy.update(
                    dt, 
                    self.player
                )
                
            # Collision
            self.collision_system.update(
                self.player,
                self.enemies,
                dt
            )
                                        
            # Update world
            self.world.update(self.player)
            
            # Update camera to follow player
            self.camera.update(self.player)
            
            # Player die
            if not self.player.alive:
                self.game_state = "gameover"
                
            # Give exp and remove dead enemies
            alive_enemy = []
            
            for enemy in self.enemies:
                if enemy.alive:
                    alive_enemy.append(enemy)
                    
                else:
                    level_ups = self.player.stats.add_exp(enemy.exp_reward)
                    if level_ups > 0:
                        self.level_up_system.handle_level_up(level_ups)
                        
            self.enemies = alive_enemy
            
            if (
                self.level_up_system.awaiting_choice
                and self.game_state == "game"
            ):
                self.game_state = "levelup"
            
          
    # Draw game objects
    def draw(self):
        # Menu
        if self.game_state == "menu":
            self.menu.draw(self.screen)
            
        # Mode select
        elif self.game_state == "mode_select":
            self.select_mode.draw(
                self.screen
            )
            
        # Map select
        elif self.game_state == "map_select":
            self.select_map.draw(
                self.screen
            )
            
        # Game
        elif self.game_state in ("game", "pause", "gameover", "levelup"):
            self.screen.fill((0, 0, 0))  # Clear the screen with black
            
            # Draw the world
            self.world.draw(
                self.screen, 
                self.camera
            )
            
            # Draw ground spells
            self.player.spell_controller.draw_ground(
                self.screen,
                self.camera
            )
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(
                    self.screen,
                    self.camera
                )
                                                        
            # Draw player
            self.player.draw(
                self.screen, 
                self.camera
            )
            
            # Draw flying spells
            self.player.spell_controller.draw_flying(
                self.screen,
                self.camera
            )
            
            # Draw UI
            self.draw_timer()  
            
            # Pause overlay
            if self.game_state == "pause":
                self.pause.draw(self.screen)
            
            # Gameover overlay    
            if self.game_state == "gameover":
                self.gameover.draw(self.screen)
                
            # Level up overlay
            if self.game_state == "levelup":
                self.levelup.draw(
                    self.screen,
                    self.level_up_system.pending_choices
                )
            
        pygame.display.flip()  # Update the display
        
    # Timer
    def draw_timer(self):
        total_seconds = int(self.elapsed_time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        
        timer_text = f"{minutes:02}:{seconds:02}"
        
        # Render the text
        text = fonts.TITLE_FONT.render(
            timer_text, 
            True, 
            (255, 255, 255)
        )
        
        # center the text on top of the screen
        text_rect = text.get_rect(
            midtop = (
                self.screen_width 
                // 2, 
                100
            )
        )

        self.screen.blit(
            text, 
            text_rect
        )
        
    # Main game loop
    def run(self):
        while self.running:
            
            # Delta time calculation
            dt = self.clock.tick(FPS) / 1000.0  # Limit to FPS
            
            # Prevent extreme dt values
            # if the game is paused or the window is dragged, dt can become very large
            dt = min(dt, 0.1)  # Cap dt to 0.1 seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
        pygame.quit()