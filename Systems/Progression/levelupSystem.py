import random

from SpellSystem.Spells import Fireball, Flame, Meteor, Frost

LEARNABLE_SPELLS = [Fireball, Flame, Meteor, Frost]


class LevelUpSystem:
    def __init__(self, player, spellbook, upgrade_system):
        self.player = player
        self.spellbook = spellbook
        self.upgrade_system = upgrade_system

        self.pending_choices = []
        self.pending_levels = 0
        self.awaiting_choice = False

    def handle_level_up(self, level_ups):
        self.pending_levels += level_ups

        if not self.awaiting_choice:
            self.start_next_choice()

    def start_next_choice(self):
        while self.pending_levels > 0:
            self.pending_levels -= 1

            choices = self.generate_upgrade_choices()

            if choices:
                self.pending_choices = choices
                self.awaiting_choice = True
                return

        self.pending_choices = []
        self.awaiting_choice = False

    def generate_upgrade_choices(self):
        available = []

        # Upgrades for spells the player owns
        for spell in self.spellbook.spells:
            for upgrade in self.upgrade_system.get_available_upgrades(spell):
                available.append({
                    "type": "upgrade",
                    "spell": spell,
                    "upgrade": upgrade
                })

        # New spells the player doesn't own yet
        owned = {type(s) for s in self.spellbook.spells}

        for spell_class in LEARNABLE_SPELLS:
            if spell_class not in owned:
                available.append({
                    "type": "new_spell",
                    "spell_class": spell_class,
                    "upgrade": {
                        "name": "New spell",
                        "description": f"Learn {spell_class.__name__}"
                    }
                })

        random.shuffle(available)
        return available[:3]

    def apply_choice(self, choice):
        if not self.awaiting_choice or choice not in self.pending_choices:
            return None

        if choice["type"] == "new_spell":
            self.spellbook.add_spells(choice["spell_class"]())
            result = choice["upgrade"]
        else:
            result = self.upgrade_system.upgrade_spell(
                choice["spell"],
                choice["upgrade"]
            )

        self.pending_choices = []
        self.awaiting_choice = False

        # If several levels were gained at once, show the next set
        self.start_next_choice()

        print("spells now:", [type(s).__name__ for s in self.spellbook.spells])
        
        return result