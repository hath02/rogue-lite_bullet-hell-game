class CastContext:
    def __init__(
        self, 
        player, 
        enemies,
        elapsed_time = 0
    ):
        self.player = player
        self.enemies = enemies
        self.elapsed_time = elapsed_time
        
class SpellController:
    def __init__(self, player):
        self.player = player
        
    def update(self, dt, enemies):
        
        context = CastContext(
            self.player,
            enemies
        )
        
        # Update spell cooldowns
        for spell in self.player.spellbook.spells:
            spell.update(dt)
            
        # Try to cast spells
        for spell in self.player.spellbook.spells:
            
            if not spell.can_cast():
                continue
            
            spell_object = spell.cast(context)
            
            if spell_object:
                self.player.spell_objects.append(
                    spell_object
                )
                
                spell.start_cooldown()
                
        # Update active spell objects
        for spell_object in self.player.spell_objects:
            spell_object.update(dt)
            
        # Remove dead objects
        self.player.spell_objects = [
            obj
            for obj in self.player.spell_objects
            if obj.alive
        ]
                
    def update_objects(self, dt):
        
        for spell_object in self.player.spell_objects:
            spell_object.update()
            
        self.spell_objects = [
            spell_object
            for spell_object in self.player.spell_objects
            if spell_object.alive
        ]
                
    def draw_ground(self, screen, camera):
        for obj in self.player.spell_objects:
            if getattr(obj, "on_ground", False):
                obj.draw(screen, camera)


    def draw_flying(self, screen, camera):
        for obj in self.player.spell_objects:
            if not getattr(obj, "on_ground", False):
                obj.draw(screen, camera)