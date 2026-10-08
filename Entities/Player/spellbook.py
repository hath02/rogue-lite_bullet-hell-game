class Spellbook:
    def __init__(self, default_spell):
        self.spells = [default_spell]
        self.selected_index = 0

    def add_spells(self, spell):
        self.spells.append(spell)

    def get_selected_spells(self):
        if not self.spells:
            return None
        return self.spells[self.selected_index]

    def remove_spells(self, spell):
        if spell in self.spells:
            self.spells.remove(spell)
            self.selected_index = min(
                self.selected_index,
                max(0, len(self.spells) - 1)
            )

    def select_spells(self, index):
        if 0 <= index < len(self.spells):
            self.selected_index = index