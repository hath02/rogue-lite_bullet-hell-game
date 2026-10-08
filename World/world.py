import pygame

from World.Map.maps import Map

class World:
    def __init__(self, map):
        self.map = map
    
    def update(self, player):
        self.map.update(player)
        
    def draw(self, screen, camera):
        self.map.draw(screen, camera)