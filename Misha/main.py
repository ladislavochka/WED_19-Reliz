import pygame
import math
import random
from time import *
from settings import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEFAULT_COLOR,
    HOVER_COLOR,
    PRESS_COLOR,
    ERROR_COLOR,
    calculate_velocity,
)
from Sprites import Player, Bullet, Ground
from ui import Button
import sys
import os

pygame.init()

value = 0
timer_start = None
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

fire_button = Button(325, 10, 150, 40, (230, 0, 0), "огень")
fire_img = pygame.image.load("WED_19-Reliz/Misha/images/fire_button.png").convert_alpha()
fire_img_hover = pygame.image.load("WED_19-Reliz/Misha/images/fire_button_hover.png").convert_alpha()
fire_img_pressed = pygame.image.load("WED_19-Reliz/Misha/images/fire_button_pressed.png").convert_alpha()

options_world_width = SCREEN_WIDTH
options_ground_height = 200

if __name__ == "__main__" and len(sys.argv) >= 3:
    try:
        options_world_width = int(sys.argv[1])
        options_ground_height = int(sys.argv[2])
    except Exception:
        pass

ground = Ground(0, SCREEN_HEIGHT - options_ground_height, options_world_width, options_ground_height)

def get_spawn_y_for_x(ground, x, player_height=25, fallback_y=50):
    local_x = int(x - ground.x)

    if 0 <= local_x < ground.width:
        for dy in range(0, ground.height):
            if ground.surface.get_at((local_x, dy))[3] > 0:
                return ground.y + dy - player_height + 1

    return fallback_y

left_max = min(250, max(60, options_world_width // 3))
red_x = random.randint(20, left_max)
blue_left = max(options_world_width - 120, options_world_width // 2 + 20)
blue_right = max(options_world_width - 50, blue_left + 1)

if blue_left >= blue_right:
    blue_left = max(left_max + 50, options_world_width - 150)
    blue_right = max(blue_left + 1, options_world_width - 20)

blue_x = random.randint(blue_left, blue_right)

player1 = Player(red_x, get_spawn_y_for_x(ground, red_x), (255, 0, 0), is_left=True)
player2 = Player(blue_x, get_spawn_y_for_x(ground, blue_x), (0, 0, 255), is_left=False)

bullet = Bullet(-20, -20, (0, 0, 0))
add_power_button = Button(740, 10, 50, 50, (125, 125, 125), "+")
remove_power_button = Button(480, 10, 50, 50, (125, 125, 125), "-")
restart_button = Button((SCREEN_WIDTH - 200) // 2, SCREEN_HEIGHT - 70, 200, 50, (50, 50, 50), "Restart")

add_img = pygame.image.load("WED_19-Reliz/Misha/images/add_power_button.png").convert_alpha()
remove_img = pygame.image.load("WED_19-Reliz/Misha/images/remove_power_button.png").convert_alpha()
add_img = pygame.transform.smoothscale(add_img, (add_power_button.width, add_power_button.height))
remove_img = pygame.transform.smoothscale(remove_img, (remove_power_button.width, remove_power_button.height))

base_path = "WED_19-Reliz/Misha/images/restart_button.png"
hover_path = "WED_19-Reliz/Misha/images/restart_button_hover.png"
pressed_path = "WED_19-Reliz/Misha/images/restart_button_pressed.png"

if os.path.exists(base_path):
    restart_img = pygame.image.load(base_path).convert_alpha()
    restart_img = pygame.transform.smoothscale(restart_img, (restart_button.width, restart_button.height))
else:
    restart_img = None

if os.path.exists(hover_path):
    restart_img_hover = pygame.image.load(hover_path).convert_alpha()
    restart_img_hover = pygame.transform.smoothscale(restart_img_hover, (restart_button.width, restart_button.height))
else:
    restart_img_hover = restart_img

if os.path.exists(pressed_path):
    restart_img_pressed = pygame.image.load(pressed_path).convert_alpha()
    restart_img_pressed = pygame.transform.smoothscale(restart_img_pressed, (restart_button.width, restart_button.height))
else:
    restart_img_pressed = restart_img_hover if restart_img_hover is not None else restart_img

clock = pygame.time.Clock()

turn = 1
t = 0
fired = False
running = True
game_over = False
winner = None
power = 0
timer_start = None
last_second = 0

def display():
    world_w = max(1, options_world_width)
    scale = float(SCREEN_WIDTH) / float(world_w)
    screen.fill((135, 206, 235))
    y_offset = int(SCREEN_HEIGHT * (1.0 - scale))

    ground.draw_scaled(screen, scale, y_offset)
    player1.draw_scaled(screen, scale, y_offset)
    player2.draw_scaled(screen, scale, y_offset)
    bullet.draw_scaled(screen, scale, y_offset)

    mp = pygame.mouse.get_pos()

    if fire_button.is_pressed(mp):
        screen.blit(fire_img_pressed, (fire_button.x, fire_button.y))
    elif fire_button.is_hovered(mp):
        screen.blit(fire_img_hover, (fire_button.x, fire_button.y))
    else:
        screen.blit(fire_img, (fire_button.x, fire_button.y))

    add_power_button.draw(screen)
    remove_power_button.draw(screen)
    screen.blit(remove_img, (remove_power_button.x, remove_power_button.y))
    screen.blit(add_img, (add_power_button.x, add_power_button.y))

    slots = 5
    left = remove_power_button.x + remove_power_button.width + 12
    right = add_power_button.x - 12
    total_width = right - left
    slot_w = 48
    slot_h = 34
    spacing = (total_width - slots * slot_w) // (slots - 1) if slots > 1 else 0
    slot_y = remove_power_button.y + (remove_power_button.height - slot_h) // 2

    for i in range(slots):
        sx = left + i * (slot_w + spacing)
        rect = pygame.Rect(sx, slot_y, slot_w, slot_h)

        if i < power:
            intensity = 120 + int(135 * ((i + 1) / slots))
            color = (intensity, intensity, 50)
        else:
            color = (60, 60, 60)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (0, 0, 0), rect, 3)

    if game_over and winner is not None:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        w_color = player1.color if winner == 1 else player2.color
        font = pygame.font.SysFont("comicsans", 64)
        text_surf = font.render(f"Player {winner} won", True, w_color)
        tx = (SCREEN_WIDTH - text_surf.get_width()) // 2
        ty = _text_center_y
        screen.blit(text_surf, (tx, ty))

        mp = pygame.mouse.get_pos()

        if restart_img is not None:
            if restart_rect.collidepoint(mp) and pygame.mouse.get_pressed()[0]:
                screen.blit(restart_img_pressed, (restart_rect.x, restart_rect.y))
            elif restart_rect.collidepoint(mp):
                screen.blit(restart_img_hover, (restart_rect.x, restart_rect.y))
            else:
                screen.blit(restart_img, (restart_rect.x, restart_rect.y))
        else:
            restart_button.draw(screen)

while running:
    _text_center_y = SCREEN_HEIGHT // 2 - 40
    _restart_x = (SCREEN_WIDTH - restart_button.width) // 2
    _restart_y = _text_center_y + 80
    restart_rect = pygame.Rect(_restart_x, _restart_y, restart_button.width, restart_button.height)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            if fire_button.is_hovered(mouse_pos) and not fired and not game_over:
                from math import sqrt
                ratio = float(options_world_width) / max(1.0, float(SCREEN_WIDTH))
                velocity_scale = sqrt(ratio)
                velocity_scale = max(0.6, min(velocity_scale, 1.6))
                bullet.set_velocity(calculate_velocity(power) * velocity_scale)
                bullet.launch(turn, player1, player2)
                fired = True
                t = 0

            if add_power_button.is_hovered(mouse_pos):
                if power < 5:
                    power += 1
                timer_start = time()
                last_second = 0

            if remove_power_button.is_hovered(mouse_pos):
                if power > 0:
                    power -= 1
                timer_start = time()
                last_second = 0

            if restart_rect.collidepoint(mouse_pos) and game_over:
                ground = Ground(0, SCREEN_HEIGHT - options_ground_height, options_world_width, options_ground_height)
                left_max = min(250, max(60, options_world_width // 3))
                red_x = random.randint(20, left_max)
                blue_left = max(options_world_width - 120, options_world_width // 2 + 20)
                blue_right = max(options_world_width - 50, blue_left + 1)

                if blue_left >= blue_right:
                    blue_left = max(left_max + 50, options_world_width - 150)
                    blue_right = max(blue_left + 1, options_world_width - 20)

                blue_x = random.randint(blue_left, blue_right)
                player1 = Player(red_x, get_spawn_y_for_x(ground, red_x), (255, 0, 0), is_left=True)
                player2 = Player(blue_x, get_spawn_y_for_x(ground, blue_x), (0, 0, 255), is_left=False)
                bullet.reset()
                fired = False
                game_over = False
                winner = None
                power = 0
                turn = 1

    dt = clock.tick(60) / 1000.0
    mouse_pos = pygame.mouse.get_pos()

    if not game_over:
        player1.update(ground, dt, active_turn=turn, bullet_fired=fired)
        player2.update(ground, dt, active_turn=turn, bullet_fired=fired)

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
            bullet.move_with_players(turn, t, player1, player2)

            p1_rect = pygame.Rect(int(player1.x), int(player1.y), player1.width, player1.height)
            p2_rect = pygame.Rect(int(player2.x), int(player2.y), player2.width, player2.height)
            target_rect = p2_rect if turn == 1 else p1_rect

            if bullet.rect.colliderect(target_rect):
                winner = turn
                game_over = True
                fired = False
                bullet.reset()
            else:
                if bullet.y > 1000 or bullet.x < 0 or bullet.x > options_world_width:
                    fired = False
                    bullet.reset()

                    if not game_over:
                        turn = 2 if turn == 1 else 1

                elif ground.rect.collidepoint(bullet.x, bullet.y):
                    local_x = int(bullet.x - ground.x)
                    local_y = int(bullet.y - ground.y)

                    if 0 <= local_x < ground.width and 0 <= local_y < ground.height:
                        if ground.surface.get_at((local_x, local_y))[3] > 0:
                            exp = bullet.explosion_on_ground(ground)

                            if exp is not None:
                                ex_x, ex_y, radius = exp

                                for pid, p in ((1, player1), (2, player2)):
                                    pcx = p.x + p.width / 2.0
                                    pcy = p.y + p.height / 2.0
                                    dist = math.hypot(pcx - ex_x, pcy - ex_y)

                                    if dist <= radius + max(p.width, p.height) / 2.0:
                                        loser = pid
                                        winner = 2 if loser == 1 else 1
                                        game_over = True
                                        break

                            fired = False
                            bullet.reset()

                            if not game_over:
                                turn = 2 if turn == 1 else 1

    if game_over:
        if restart_rect.collidepoint(mouse_pos):
            restart_button.color = HOVER_COLOR

            if pygame.mouse.get_pressed()[0]:
                restart_button.color = PRESS_COLOR
        else:
            restart_button.color = DEFAULT_COLOR

    if not game_over and add_power_button.is_hovered(mouse_pos):
        add_power_button.color = (85, 85, 85)

        if pygame.mouse.get_pressed()[0]:
            add_power_button.color = (25, 25, 25)

            if timer_start is not None:
                value = int(time() - timer_start)

                if value > last_second:
                    if power < 5:
                        power += 1
                    last_second = value
    else:
        add_power_button.color = (125, 125, 125)

    if not game_over and remove_power_button.is_hovered(mouse_pos):
        remove_power_button.color = (85, 85, 85)

        if pygame.mouse.get_pressed()[0]:
            remove_power_button.color = (25, 25, 25)

            if timer_start is not None:
                value = int(time() - timer_start)

                if value > last_second:
                    if power > 0:
                        power -= 1
                    last_second = value
    else:
        remove_power_button.color = (125, 125, 125)

    screen.fill((135, 206, 235))
    display()
    pygame.display.update()

pygame.quit()
