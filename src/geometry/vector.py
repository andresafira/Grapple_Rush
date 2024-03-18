from math import sqrt, cos, sin


class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def polar(self, r: float, theta: float):
        self.x = r*cos(theta)
        self.y = r*sin(theta)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def dot(self, other):
        return self.x * other.x + self.y * other.y
    
    def abs(self):
        return sqrt(self.x * self.x + self.y * self.y)
    
    def normalize(self, new_mod: float = 1):
        if self.abs() < 0.001:
            return self
        return self / self.abs() * new_mod
