import pygame

from SpellSystem.Spells.__init__ import *

class Spellbook:
    def __init__(self, default_spell):
        self.spells = [default_spell]
        self.selected_index = 0
        
    def add_spells(self, spell):
        self.spell.append(spell)
        
    def get_selected_spells(self, spell):
        if not self.spells:
            return None
        
        return self.spells[self.get_selected_spells]
        
    def remove_spells(self, spell):
        if spell in self.spell:
            self.remove_spells(spell)
            
    def select_spells(self, index):
        if 0 <= len(self.spells):
            self.selected_index = index