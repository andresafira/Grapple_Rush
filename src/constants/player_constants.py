# GH == Grappling Hook
# Todos os valores a seguir foram carteados

GH_MAX_LENGTH: float = 500
GH_MIN_LENGTH: float = 30
GH_MAX_THRUST: float = 6.9

GRAPPLING_HOOK_SPEED: float = 500

PLAYER_WIDHT: float = 6.9
PLAYER_HEIGHT: float = 6.9

# Movement Constants
ACC_KP: float = 8 # Proportionality constant for horizontal movement: acc = ACC_KP*(target_speed - speed)
MAX_HORIZONTAL_SPEED: float = 200
MAX_JUMP_SPEED: float = 200
MAX_FALL_SPEED: float = 600

BASE_G_VALUE: float = -600  # Basic acceleration value (remember to be negative)
FALL_G_MULTIPLIER: float = 1.2  # Gravity multiplier while falling (intended to be greater than 1)
JUMP_G_CONTROL: float = 0.4  # Gravity multiplier (intended to be less than 1)
