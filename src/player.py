from utils import Vector



class Player:
    def __init__(self, initial_pos: Vector):
        self.position = initial_pos
        self.velocity = Vector(0, 0)
    
    def move(self):
        self.position += self.velocity
