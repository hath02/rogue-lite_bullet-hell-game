import pygame
import random

class LevelUpSystem:
    def __init__(self, player, spellbook, upgrade_system):
        self.player = player
        self.spellbook = spellbook
        self.upgrade_system = upgrade_system
        
        self.pending_choices = []
        self.awaiting_choice = False
        
    def add_exp(self, amount):
        level_ups = self.player.stats.add_exp(amount)
        
        if level_ups > 0:
            self.handle_level_up(level_ups)
            
    def handle_level_up(self, level_ups):
        for _ in range(level_ups):
            self.level_up()
            
    def level_up(self):
        self.pending_choices = self.generate_upgrade_choices()
        self.awaiting_choice = True
        
        return self.pending_choices
    
    def generate_upgrade_choices(self):
        available = []
        
        for spell in self.spellbook.spells:
            
            if not self.upgrade_system.can_upgrade(spell):
                continue
            
            upgrades = self.upgrade_system.get_available_upgrades(spell)
            
            for upgrade in upgrades:
                available.append({
                    "spell": spell, 
                    "upgrades": upgrade
                })
                
        random.shuffle(available)
        
        return available[:3]  # Return up to 3 random choices
    
    def apply_choice(self, choice):
        if not self.awaiting_choice:
            return None
        
        if choice not in self.pending_choices:
            return None
        
        spell = choice["spell"]
        upgrade = choice["upgrades"]
        
        result = self.upgrade_system.upgrade_spell(
            spell, 
            upgrade
        )
        
        self.pending_choices = []
        self.awaiting_choice = False
        
        return result