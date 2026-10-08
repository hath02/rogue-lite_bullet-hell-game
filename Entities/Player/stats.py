import pygame

class Stats:
    def __init__(self):
        # HP
        self.max_hp = 100
        self.hp = self.max_hp
        
        # Movement
        self.speed = 300
        
        # Progression
        self.level = 1
        
        self.exp = 0
        
    def add_exp(self, amount):
        self.exp += amount
        
        level_ups = 0
        
        while self.exp >= self.get_exp_required():
            self.exp -= self.get_exp_required()
            self.level += 1
            level_ups += 1
            
        return level_ups
    
    def get_exp_required(self):
        return int(10 * (self.level ** 1.5))