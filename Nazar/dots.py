import pygame

dots = []
for x in range(80, 520, 40):     
    for y in range(80, 520, 40):
        dots.append(pygame.Rect(x, y, 6, 6))

def draw_dots(screen):
    for dot in dots:
        pygame.draw.circle(screen, (255, 255, 255), dot.center, 3)