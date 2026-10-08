from SpellSystem.spellStats import SpellStats
from Systems.Audio.audioManager import AudioManager

class Spell:
    def __init__(self, stats = None):
        # Spell stats
        self.stats = stats if stats is not None else SpellStats()

        # Upgrades
        self.selected_upgrade = set()
        
        self.level = 1
        
        # Cooldown timer
        self.cooldown_timer = 0
        
        # Visual
        self.on_ground = False
        
        # Sound
        self.sound = None
    
    
        # ----- upgrades (spells can override these) -----
    def get_stat_upgrades(self):
        return [
            {"id": "damage",   "name": "Power", "description": "Damage +20%"},
            {"id": "cooldown", "name": "Haste", "description": "Cooldown -10%"},
        ]

    def apply_stats_upgrade(self, upgrade):
        if upgrade["id"] == "damage":
            self.stats.damage *= 1.2
        elif upgrade["id"] == "cooldown":
            self.stats.cooldown = max(0.2, self.stats.cooldown * 0.9)

    def get_perk_upgrades(self):
        # Placeholder perks for levels 3, 5, 10. Replace per spell later.
        return [
            {"id": "perk-power", "name": "Overcharge", "description": "Damage +50%"},
            {"id": "perk-speed", "name": "Rapid Cast", "description": "Cooldown -25%"},
        ]

    def apply_perk_upgrade(self, upgrade):
        if upgrade["id"] == "perk-power":
            self.stats.damage *= 1.5
        elif upgrade["id"] == "perk-speed":
            self.stats.cooldown = max(0.2, self.stats.cooldown * 0.75)
    
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