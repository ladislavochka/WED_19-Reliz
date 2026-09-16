from math import sqrt

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1000
DEFAULT_COLOR = (230, 0, 0)
HOVER_COLOR = (200, 0, 0)
PRESS_COLOR = (0, 255, 0)
ERROR_COLOR = (0, 0, 0)


def calculate_velocity(loads):
    return 60 * sqrt(loads)


x = 10
loads = x / 7
velocity = calculate_velocity(loads)
angle = 90
gravity = 9.8