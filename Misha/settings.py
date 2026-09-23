from math import sqrt

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
DEFAULT_COLOR = (230, 0, 0)
HOVER_COLOR = (200, 0, 0)
PRESS_COLOR = (0, 255, 0)
ERROR_COLOR = (0, 0, 0)


def calculate_velocity(loads):
    POWER_VELOCITIES = [0.0, 30.0, 50.0, 75.0, 95.0, 120.0]
    l = int(max(0, min(5, loads)))
    return POWER_VELOCITIES[l]


angle = 90
gravity = 9.8