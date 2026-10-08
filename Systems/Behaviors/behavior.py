class Behavior:
    def __init__(self):
        self.alive = True
        
    def update(self, dt):
        pass
    
    def destroy(self):
        self.alive = False