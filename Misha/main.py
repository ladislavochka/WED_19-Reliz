import pygame
from time import *
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEFAULT_COLOR,
    HOVER_COLOR,
    PRESS_COLOR,
    ERROR_COLOR,
)
from Sprites import Player, Bullet, Ground
from ui import Button

pygame.init()

value = 0
timer_start = None


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fire_button = Button(325, 10, 150, 40, (230, 0, 0), "огень")
player1 = Player(50, 900, (255, 0, 0))
player2 = Player(700, 900, (0, 0, 255))
bullet = Bullet(-20, -20, (0, 0, 0))
ground = Ground(0, 950, SCREEN_WIDTH, 50)
add_power_button = Button(740, 10, 50, 50, (125, 125, 125), "+")
remove_power_button = Button(480, 10, 50, 50, (125, 125, 125), "-")

clock = pygame.time.Clock()

turn = 1
t = 0
fired = False
running = True

power = 0
def display():
    player1.draw(screen)
    player2.draw(screen)
    fire_button.draw(screen)
    bullet.draw(screen)
    ground.draw(screen)
    add_power_button.draw(screen)
    remove_power_button.draw(screen)
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if fire_button.is_hovered(mouse_pos) and not fired:
                fired = True
                t = 0
                print("ВЫСТРЕЛ")


    # МЕХАНИКА ИГРЫ

    mouse_pos = pygame.mouse.get_pos()

    if fire_button.is_hovered(mouse_pos):
        fire_button.color = HOVER_COLOR
    else:
        fire_button.color = DEFAULT_COLOR

    if fire_button.is_pressed(mouse_pos):
        fire_button.color = PRESS_COLOR
        if fired:
            fire_button.color = ERROR_COLOR

    if fired:
        t += 0.1
        bullet.move(turn, t)
        if bullet.y > 1000 or bullet.x < 0 or bullet.x > 800:
            fired = False
            bullet.reset()
            turn = 2 if turn == 1 else 1

        if ground.rect.collidepoint(bullet.x, bullet.y):
            local_x = int(bullet.x - ground.x)
            local_y = int(bullet.y - ground.y)
            if 0 <= local_x < ground.width and 0 <= local_y < ground.height:
                # функция get_at возвращяет лист [r,g,b,а] на позиции пули при столкновении
                if ground.surface.get_at((local_x, local_y))[3] > 0:
                    bullet.explosion()
                    print(f"collision at {bullet.x}, {bullet.y}")
                    fired = False
                    bullet.reset()
                    turn = 2 if turn == 1 else 1

    if add_power_button.is_hovered(mouse_pos):
        add_power_button.color = (85, 85, 85)
        if add_power_button.is_pressed(mouse_pos):
            timer_start = time()
            add_power_button.color = (25, 25, 25)
            if power < 5:
                power += 1
                
    else:
        add_power_button.color = (125, 125, 125)

    if remove_power_button.is_hovered(mouse_pos):
        remove_power_button.color = (85, 85, 85)
        if remove_power_button.is_pressed(mouse_pos):
            remove_power_button.color = (25, 25, 25)
    else:
        remove_power_button.color = (125, 125, 125)

    if timer_start is not None:
        value = int(time() - timer_start)

    screen.fill((135, 206, 235))

    print(value)
    # РЕНДЕРИНГ

    display()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()