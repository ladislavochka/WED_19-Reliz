import pygame

dots = []
for x in range(250, 351, 100):     
    for y in range(250, 351, 100):
        dots.append(pygame.Rect(x, y, 60, 60))

def draw_dots(screen):
    for dot in dots:
        pygame.draw.circle(screen, (255, 255, 255), dot.center, 3)