import pygame

class CollisionSystem:

    def __init__(self):
        self.projectile_collision = ProjectileCollision()
        self.aoe_collision = AOECollision()
        self.cone_collision = ConeCollision()
        

    def update(self, player, enemies, dt):

        # Player spells
        for spell in player.spell_objects:

            if not spell.alive:
                continue

            self.check_spell(
                spell,
                enemies,
                dt
            )
            
            self.update_hit_timers(
                spell,
                dt
            )

        # Enemy projectiles
        self.check_enemy_projectiles(
            player,
            enemies
        )
        
    def update_hit_timers(self, spell, dt):

        if not hasattr(spell, "hit_timers"):
            return

        for enemy in list(spell.hit_timers):

            spell.hit_timers[enemy] -= dt

            if spell.hit_timers[enemy] <= 0:
                del spell.hit_timers[enemy]
                
    def check_spell(self, spell, enemies, dt):

        for enemy in enemies:

            if not enemy.alive:
                continue


            if spell.collision_type == "projectile":

                self.projectile_collision.check(
                    spell,
                    enemy
                )

            elif spell.collision_type == "area":

                self.aoe_collision.check(
                    spell,
                    enemy
                )

            elif spell.collision_type == "cone":

                self.cone_collision.check(
                    spell,
                    enemy
                )

            if not spell.alive:
                break

    def check_enemy_projectiles(
        self,
        player,
        enemies
    ):

        for enemy in enemies:

            if not hasattr(enemy, "projectiles"):
                continue


            for projectile in enemy.projectiles:

                if not projectile.alive:
                    continue


                distance = (
                    projectile.position
                    .distance_to(
                        player.position
                    )
                )


                if distance <= (
                    projectile.hitbox_radius
                    + player.hitbox_radius
                ):

                    player.take_damage(
                        projectile.damage
                    )

                    projectile.destroy()
                    
class CollisionHandler:
    def check(self, source, target):
        pass
    
    def hit(self, source, target):
        if hasattr(source, "hit_enemies"):
            
            if target in source.hit_enemies:
                return False
            
            source.hit_enemies.add(target)
        
        target.take_damage(
            source.damage
        )
        
        if hasattr(source, "on_hit"):
            source.on_hit(target)
            
        return True
    
class ProjectileCollision(CollisionHandler):
    def check(self, spell, enemy):
        distance = (
            spell.position
            .distance_to(enemy.position)
        )
        
        if distance > (
            spell.hitbox_radius
            + enemy.hitbox_radius
        ):
            return
        
        if not self.hit(spell, enemy):
            return
        
        spell.pierce -= 1
        
        if spell.pierce < 0:
            spell.destroy()
            
class AOECollision(CollisionHandler):
    def check(self, spell, enemy):
        
        distance = (
            spell.position
            .distance_to(enemy.position)
        )
        
        if distance > spell.radius:
            return
        
        # Timer    
        timer = spell.hit_timers.get(
            enemy,
            0
        )
        
        if timer > 0:
            return
        
        self.hit(
            spell,
            enemy
        )
        
        spell.hit_timers[enemy] = spell.damage_interval
                
class ConeCollision(CollisionHandler):
    def check(self, spell, enemy):    
        # Direction
        direction = (
            enemy.position
            - spell.position
        )
        
        if direction.length_squared() == 0:
            return
        
        distance = direction.length()
        
        if distance > spell.range:
            return
        
        direction.normalize_ip()
        
        angle = spell.direction.angle_to(
            direction
        )
        
        if abs(angle) > spell.angle / 2:
            return
        
        # Timer
        timer = spell.hit_timers.get(
            enemy,
            0
        )
        
        if timer > 0:
            return     
           
        self.hit(spell, enemy)
        
        spell.hit_timers[enemy] = spell.damage_interval