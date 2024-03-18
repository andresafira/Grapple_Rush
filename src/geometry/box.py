from vector import Vector


class Box:
    def __init__(self, x, y, width, height):
        self.vertices = (Vector(x, y),
                         Vector(x + width, y),
                         Vector(x + width, y + height),
                         Vector(x, y + height))

    def is_inside(self, point: Vector) -> bool:
        if point.x < self.vertices[0].x or point.x > self.vertices[2].x:
            return False
        if point.y < self.vertices[0].y or point.y > self.vertices[2].y:
            return False
        return True

    def check_collision(self, other):
        for p in other.vertices:
            if self.is_inside(p):
                return True
        return False
