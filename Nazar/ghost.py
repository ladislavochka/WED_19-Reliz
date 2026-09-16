import pygame
import random

ghosts = [
    pygame.Rect(285, 230, 30, 30),
    pygame.Rect(325, 230, 30, 30),
    pygame.Rect(365, 230, 30, 30),
    pygame.Rect(405, 230, 30, 30)
]

ghost_colors = [
    (255, 0, 0),
    (255, 105, 180),
    (0, 255, 255),
    (255, 165, 0)
]

directions = [
    [2, 0],
    [-2, 0],
    [0, 2],
    [0, -2]
]

def move_ghosts(walls):
    for i, ghost in enumerate(ghosts):
        dx, dy = directions[i]

        old_x = ghost.x
        old_y = ghost.y

        ghost.x += dx
        ghost.y += dy

        for wall in walls:
            if ghost.colliderect(wall):
                ghost.x = old_x
                ghost.y = old_y

                directions[i] = random.choice([
                    [2, 0],
                    [-2, 0],
                    [0, 2],
                    [0, -2]
                ])
                break


def draw_ghosts(screen):
    for i, ghost in enumerate(ghosts):
        color = ghost_colors[i]

        pygame.draw.circle(
            screen,
            color,
            (ghost.centerx, ghost.top + 12),
            12
        )

        pygame.draw.rect(
            screen,
            color,
            (ghost.left + 3, ghost.top + 12, 24, 15)
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (ghost.left + 10, ghost.top + 10),
            5
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (ghost.left + 20, ghost.top + 10),
            5
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (ghost.left + 10, ghost.top + 10),
            2
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0))