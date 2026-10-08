import random

class Timed:
    def __init__(self, map_name, duration = 300):
        self.map_name = map_name
        self.duration = duration
        
    def update(self, elapsed_time):
        if elapsed_time >= self.duration:
            return "win"
        
        return None
    
class Endless:
    def __init__(self, maps):
        self.maps = maps
        self.map_name = random.choice(self.maps)
        
    def update(self, elapsed_time):
        return None