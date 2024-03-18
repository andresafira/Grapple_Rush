from box import Box
from vector import Vector


def get_points(x: float, y: float, width: float, height: float) -> tuple:
    P1 = Vector(x, y)
    P2 = Vector(x + width, y)
    P3 = Vector(x + width, y + height)
    P4 = Vector(x, y+ height)
    return (P1, P2, P3, P4)


def create_box(x: float, y: float, width: float, height: float) -> Box:
    points = get_points(x, y, width, height)
    return Box(*points)
