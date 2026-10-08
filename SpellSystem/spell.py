from SpellSystem.spellStats import SpellStats
from Systems.Audio.audioManager import AudioManager

class Spell:
    def __init__(self, stats = None):
        # Spell stats
        self.stats = stats if stats is not None else SpellStats()

        # Upgrades
        self.selected_upgrade = set()
        
        # Cooldown timer
        self.cooldown_timer = 0
        
        # Visual
        self.on_ground = False
        
        # Sound
        self.sound = None
    
    def update(self, dt):
        # Update spell cooldown
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt
            
            if self.cooldown_timer < 0:
                self.cooldown_timer = 0
                
    def can_cast(self):
        # Return True if spell is ready to cast  

        return self.cooldown_timer <= 0  

    def start_cooldown(self):
        # Start spell cooldown 
        self.cooldown_timer = self.stats.cooldown
        
    def cast(self, context):
        # Called by SpellController when the spell is ready
        # Child override this

        raise NotImplementedError(
            f"{self.__class__.__name__} must implement cast()"
        )