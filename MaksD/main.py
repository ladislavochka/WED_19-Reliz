import pygame
import math
import random

pygame.init()

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("Minecraft Upgrader")
running = True
clock = pygame.time.Clock()

font = pygame.font.Font('WED_19-Reliz/MaksD/minecraft.ttf', 30)
font_small = pygame.font.Font('WED_19-Reliz/MaksD/minecraft.ttf', 20)
text_title = font.render("UPGRADER", True, (255, 255, 255))

img1 = pygame.image.load('WED_19-Reliz/MaksD/mc_inventory1.png')
img2 = pygame.image.load('WED_19-Reliz/MaksD/mc_inventory2.png')

w_d_img = pygame.image.load('WED_19-Reliz/MaksD/w_s.webp')
s_s_img = pygame.image.load('WED_19-Reliz/MaksD/s_s.png')
i_s_img = pygame.image.load('WED_19-Reliz/MaksD/i_s.webp')
g_s_img = pygame.image.load('WED_19-Reliz/MaksD/g_s.png')
d_s_img = pygame.image.load('WED_19-Reliz/MaksD/d_s.webp')
n_w_img = pygame.image.load('WED_19-Reliz/MaksD/n_s.webp')

img1 = pygame.transform.scale(img1, (700, 300))
img2 = pygame.transform.scale(img2, (70, 70))

upgrader_c_raw = pygame.image.load('WED_19-Reliz/MaksD/upgrader circle.png')
upgrader_c = pygame.transform.scale(upgrader_c_raw, (280, 280))

w_d_img = pygame.transform.scale(w_d_img, (55, 55))
s_s_img = pygame.transform.scale(s_s_img, (55, 55))
i_s_img = pygame.transform.scale(i_s_img, (55, 55))
g_s_img = pygame.transform.scale(g_s_img, (55, 55))
d_s_img = pygame.transform.scale(d_s_img, (55, 55))
n_w_img = pygame.transform.scale(n_w_img, (55, 55))

ITEM_VALUES = {
    "wood": 10,
    "stone": 25,
    "iron": 60,
    "gold": 150,
    "diamond": 400,
    "netherite": 1000
}

UPGRADE_CHAIN = ["wood", "stone", "iron", "gold", "diamond", "netherite"]

swords = [
    {"name": "wood", "rect": pygame.Rect(100, 393, 55, 55), "home_pos": (100, 393), "img": w_d_img},
    {"name": "stone", "rect": pygame.Rect(170, 393, 55, 55), "home_pos": (170, 393), "img": s_s_img},
    {"name": "iron", "rect": pygame.Rect(240, 393, 55, 55), "home_pos": (240, 393), "img": i_s_img},
    {"name": "gold", "rect": pygame.Rect(310, 393, 55, 55), "home_pos": (310, 393), "img": g_s_img},
]

SWORD_IMAGES = {
    "wood": w_d_img,
    "stone": s_s_img,
    "iron": i_s_img,
    "gold": g_s_img,
    "diamond": d_s_img,
    "netherite": n_w_img
}

UPGRADE_BTN = pygame.Rect(325, 380, 150, 45)

sword_slot_pos = (122, 177)
target_slot_pos = (627, 177)

active_sword = None
target_sword_name = None
success_chance = 0.0

spinning = False
wheel_angle = 0.0
spin_speed = 0.0
target_angle = 0.0
spin_start_time = 0
status_text = ""


def calculate_upgrade():
    global target_sword_name, success_chance
    if not active_sword:
        target_sword_name = None
        success_chance = 0.0
        return

    current_name = active_sword["name"]
    if current_name in UPGRADE_CHAIN:
        idx = UPGRADE_CHAIN.index(current_name)
        if idx < len(UPGRADE_CHAIN) - 1:
            target_sword_name = UPGRADE_CHAIN[idx + 1]
            v_curr = ITEM_VALUES[current_name]
            v_next = ITEM_VALUES[target_sword_name]
            success_chance = min(1.0, v_curr / v_next)
        else:
            target_sword_name = None
            success_chance = 0.0


def start_spin():
    global spinning, spin_speed, wheel_angle, target_angle, spin_start_time, status_text
    if not active_sword or success_chance <= 0 or spinning:
        return

    spinning = True
    status_text = "Вращение..."

    is_win = random.random() < success_chance
    win_angle_max = success_chance * 360.0

    if is_win:
        chosen_angle_on_wheel = random.uniform(5, max(6, win_angle_max - 5))
    else:
        chosen_angle_on_wheel = random.uniform(win_angle_max + 5, 355)

    required_final_angle = (90 - chosen_angle_on_wheel) % 360
    extra_turns = 360 * 5
    target_angle = wheel_angle + extra_turns + ((required_final_angle - (wheel_angle % 360)) % 360)

    spin_speed = 25.0
    spin_start_time = pygame.time.get_ticks()


def update_wheel():
    global wheel_angle, spin_speed, spinning, status_text, active_sword
    if not spinning:
        return

    remaining = target_angle - wheel_angle
    if remaining > 0.5:
        spin_speed = max(1.5, remaining * 0.08)
        wheel_angle += spin_speed
    else:
        wheel_angle = target_angle
        spinning = False

        pointer_angle_on_wheel = (90 - wheel_angle) % 360
        win_angle_max = success_chance * 360.0

        if pointer_angle_on_wheel <= win_angle_max:
            status_text = "УСПЕХ!"
            active_sword["name"] = target_sword_name
            active_sword["img"] = SWORD_IMAGES[target_sword_name]
            calculate_upgrade()
        else:
            status_text = "ПРОВАЛ!"
            active_sword["rect"].topleft = active_sword["home_pos"]
            active_sword = None
            calculate_upgrade()


def draw_wheel(surface, center, radius, chance):
    cx, cy = center

    pygame.draw.circle(surface, (200, 50, 50), center, radius)

    if chance > 0:
        angle_deg = chance * 360.0
        points = [(cx, cy)]
        for a in range(0, int(angle_deg) + 1):
            rad = math.radians(a - wheel_angle)
            px = cx + radius * math.cos(rad)
            py = cy - radius * math.sin(rad)
            points.append((px, py))

        if len(points) > 2:
            pygame.draw.polygon(surface, (50, 200, 80), points)

    pygame.draw.circle(surface, (40, 40, 50), center, radius, 4)

    pointer_pts = [
        (cx, cy - radius - 12),
        (cx - 10, cy - radius + 8),
        (cx + 10, cy - radius + 8)
    ]
    pygame.draw.polygon(surface, (255, 215, 0), pointer_pts)
    pygame.draw.polygon(surface, (0, 0, 0), pointer_pts, 2)


def blitz():
    screen.fill((22, 25, 35))
    screen.blit(text_title, (280, 20))

    screen.blit(img1, (50, 375))
    screen.blit(img2, (115, 170))
    screen.blit(img2, (620, 170))

    wheel_center = (405, 230)
    wheel_radius = 110
    draw_wheel(screen, wheel_center, wheel_radius, success_chance)

    screen.blit(upgrader_c, (265, 90))

    if target_sword_name and target_sword_name in SWORD_IMAGES:
        target_img = SWORD_IMAGES[target_sword_name]
        screen.blit(target_img, target_slot_pos)

    for sword in swords:
        screen.blit(sword["img"], (sword["rect"].x, sword["rect"].y))

    if active_sword and target_sword_name:
        chance_percent = int(success_chance * 100)
        chance_text = font.render(f"{chance_percent}%", True, (255, 255, 255))
        screen.blit(chance_text, (380, 215))

    btn_color = (70, 160, 70) if (active_sword and not spinning and success_chance > 0) else (80, 80, 80)
    pygame.draw.rect(screen, btn_color, UPGRADE_BTN, border_radius=8)
    pygame.draw.rect(screen, (255, 255, 255), UPGRADE_BTN, 2, border_radius=8)
    btn_text = font_small.render("UPGRADE", True, (255, 255, 255))
    screen.blit(btn_text, (UPGRADE_BTN.x + 22, UPGRADE_BTN.y + 12))

    if status_text:
        col = (100, 255, 100) if status_text == "УСПЕХ!" else (255, 80, 80)
        st_txt = font_small.render(status_text, True, col)
        screen.blit(st_txt, (360, 345))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos

            if UPGRADE_BTN.collidepoint(mouse_pos):
                start_spin()

            if not spinning:
                for sword in swords:
                    if sword["rect"].collidepoint(mouse_pos):
                        if sword["rect"].topleft == sword_slot_pos:
                            sword["rect"].topleft = sword["home_pos"]
                            active_sword = None
                        else:
                            for s in swords:
                                s["rect"].topleft = s["home_pos"]
                            sword["rect"].topleft = sword_slot_pos
                            active_sword = sword

                        status_text = ""
                        calculate_upgrade()

    update_wheel()
    blitz()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()