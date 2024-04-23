# GH == Grappling Hook
# Todos os valores a seguir foram carteados

HITPOINTS = {'x': (0, 0.5, 1),
             'y': (0, 0.25, 0.5, 0.75, 1)}

GH_MAX_LENGTH: float = 6.9
GH_MAX_THRUST: float = 6.9

PLAYER_WIDTH: int = 30
PLAYER_HEIGHT: int = 60

# Movement Constants
ACC_KP: float = 8 # Proportionality constant for horizontal movement: acc = ACC_KP*(target_speed - speed)
MAX_HORIZONTAL_SPEED: float = 200
MAX_JUMP_SPEED: float = 200
MAX_FALL_SPEED: float = 600

BASE_G_VALUE: float = -600  # Basic acceleration value (remember to be negative)
FALL_G_MULTIPLIER: float = 1.2  # Gravity multiplier while falling (intended to be greater than 1)
JUMP_G_CONTROL: float = 0.4  # Gravity multiplier (intended to be less than 1)
