from utils import Vector
from typing import Union


class Player:
    def __init__(self, initial_pos: Vector):
        self.position = initial_pos
        self.velocity = Vector(0, 0)
        self.alive = True

        self.gh_position: Union[None, Vector] = None
        self.gh_attached: bool = False

    def move(self):
        self.position += self.velocity
