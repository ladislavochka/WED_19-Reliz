import pygame
from ghost import ghosts,move_ghosts, draw_ghosts
from dots import dots, draw_dots #add
pygame.init()

screen = pygame.display.set_mode((600, 600))
pacman = pygame.Rect(280, 280, 30, 30)
speed = 4
walls = [
        pygame.Rect(50,50, 500, 20),
        pygame.Rect(50, 530, 500,20),
        pygame.Rect(50, 50, 20, 500),
        pygame.Rect(530, 50, 20, 500),
        pygame.Rect(150, 100, 300, 20),
        pygame.Rect(150, 150, 300, 20),
        pygame.Rect(430, 100, 20,  150),
        pygame.Rect(150, 400, 150, 20),
        pygame.Rect(150, 250, 20, 170),
        pygame.Rect(430, 250, 20, 170),
    ]

pacman = pygame.Rect(280, 280, 30, 30)
speed = 4

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys = pygame.key.get_pressed()
    old_x = pacman.x
    old_y = pacman.y
    if keys[pygame.K_LEFT]:
        pacman.x -= speed
    if keys[pygame.K_RIGHT]:
        pacman.x += speed
    if keys[pygame.K_UP]:
        pacman.y -= speed
    if keys[pygame.K_DOWN]:
        pacman.y += speed
    #add
    for wall in walls:
        if pacman.colliderect(wall):
            pacman.x = old_x
            pacman.y = old_y
    for dot in dots[:]:
        if pacman.colliderect(dot):
            dots.remove(dot)

    move_ghosts(walls)
    for ghost in ghosts:
         if pacman.colliderect(ghost):
            pacman.x = 280
            pacman.y = 280
    if len(dots) == 0:
        print ("YOU WIN!")
        running = False
    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall)
    draw_dots(screen)
    draw_ghosts(screen)
    pygame.draw.circle(screen,(255, 255, 255), pacman.center,15)
    pygame.display.update()
    screen.fill((0, 0, 0))
#add
pygame.quit()