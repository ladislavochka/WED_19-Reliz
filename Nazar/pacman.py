import pygame

pygame.init()

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Pac-Man")

walls = [
    pygame.Rect(50, 50, 500, 20),
    pygame.Rect(50, 530, 500, 20),
    pygame.Rect(50, 50, 20, 500),
    pygame.Rect(530, 50, 20, 500),
    pygame.Rect(150, 100, 300, 20),
    pygame.Rect(150, 100, 20, 150),
    pygame.Rect(430, 100, 20, 150),
    pygame.Rect(150, 400, 300, 20),
    pygame.Rect(150, 250, 20, 170),
    pygame.Rect(430, 250, 20, 170)
]

pacman = pygame.Rect(280, 280, 30, 30)
speed = 4

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        pacman.x -= speed
    if keys[pygame.K_RIGHT]:
        pacman.x += speed
    if keys[pygame.K_UP]:
        pacman.y -= speed
    if keys[pygame.K_DOWN]:
        pacman.y += speed

    screen.fill((0, 0, 0))

    for wall in walls:
        pygame.draw.rect(screen, (0, 0, 255), wall)

    pygame.draw.circle(screen, (255, 255, 0), pacman.center, 15)

    pygame.display.flip()

pygame.quit()
for ghost in ghosts:
    if pacman.collides(ghost):
        pacman.x = 280
        pacman.y = 280