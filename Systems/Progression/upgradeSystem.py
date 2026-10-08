class UpgradeSystem:
    
    MAX_SPELL_LEVEL = 10
    PERK_LEVEL = {3, 5, 10}
    
    def __init__(self, spellbook):
        self.spellbook = spellbook
        
    def get_upgrade_type(self, spell_level):
        if spell_level in self.PERK_LEVEL:
            return "special"
        
        return "stats"
    
    def can_upgrade(self, spell):
        return spell.level < self.MAX_SPELL_LEVEL
    
    
    def get_available_upgrades(self, spell):
        if not self.can_upgrade(spell):
            return []
        
        next_level = spell.level + 1
        upgrade_type = self.get_upgrade_type(next_level)
        
        if upgrade_type == "special":
            return [spell.perk_upgrade(spell)]
        
        return [spell.get_stat_upgrades(spell)]

    
    def upgrade_spell(self, spell, upgrade):
        if not self.can_upgrade(spell):
            return None
        
        if upgrade not in self.get_available_upgrades(spell):
            return None
        
        next_level = spell.level + 1
        upgrade_type = self.get_upgrade_type(next_level)
        
        spell.level = next_level
        
        if upgrade_type == "special":
            return spell.apply_perk_upgrade(spell)
        
        return spell.apply_stats_upgrade(spell)