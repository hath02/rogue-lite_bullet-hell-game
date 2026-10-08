class UpgradeSystem:

    MAX_SPELL_LEVEL = 8
    PERK_LEVEL = {3, 5, 8}

    def __init__(self, spellbook):
        self.spellbook = spellbook

    def get_upgrade_type(self, spell_level):
        return "special" if spell_level in self.PERK_LEVEL else "stats"

    def can_upgrade(self, spell):
        return spell.level < self.MAX_SPELL_LEVEL

    def get_available_upgrades(self, spell):
        if not self.can_upgrade(spell):
            return []

        next_level = spell.level + 1

        if self.get_upgrade_type(next_level) == "special":
            return spell.get_perk_upgrades()

        return spell.get_stat_upgrades()

    def upgrade_spell(self, spell, upgrade):
        if upgrade not in self.get_available_upgrades(spell):
            return None

        next_level = spell.level + 1
        upgrade_type = self.get_upgrade_type(next_level)

        spell.level = next_level

        if upgrade_type == "special":
            spell.apply_perk_upgrade(upgrade)
        else:
            spell.apply_stats_upgrade(upgrade)

        return upgrade