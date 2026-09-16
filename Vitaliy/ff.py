import pygame
import random
import sys

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("WED_19-Reliz/Vitaliy/verity-edit.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
# Вікно
WIDTH = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MEGA RUNNER")

clock = pygame.time.Clock()

# Кольори
SKY = (135, 206, 235)
GROUND = (80, 180, 80)
WHITE = (255, 255, 255)
BLACK = (30, 30, 30)
RED = (220, 60, 60)
BLUE = (50, 100, 220)

# Шрифти
font = pygame.font.Font(None, 45)
big_font = pygame.font.Font(None, 80)

# Земля
GROUND_Y = 500

# Гравець
player = pygame.Rect(150, GROUND_Y - 80, 55, 80)
velocity_y = 0
gravity = 1
jump_power = -18
on_ground = True

# Перешкоди
obstacles = []

# Швидкість гри
speed = 7

# Рахунок
score = 0

# Час до появи наступної перешкоди
spawn_timer = 0
spawn_delay = 1000

game_over = False


def create_obstacle():
    """Створює нову перешкоду справа."""
    height = random.randint(50, 100)
    width = random.randint(35, 60)

    obstacle = pygame.Rect(
        WIDTH + 20,
        GROUND_Y - height,
        width,
        height
    )

    obstacles.append(obstacle)


def draw_player():
    # Голова
    pygame.draw.circle(
        screen,
        BLUE,
        (player.centerx, player.y + 18),
        18
    )

    # Тіло
    pygame.draw.rect(
        screen,
        BLUE,
        (player.x + 10, player.y + 35, 35, 35)
    )

    # Ноги
    pygame.draw.line(
        screen,
        BLACK,
        (player.x + 18, player.bottom - 10),
        (player.x + 5, player.bottom),
        6
    )

    pygame.draw.line(
        screen,
        BLACK,
        (player.x + 37, player.bottom - 10),
        (player.x + 50, player.bottom),
        6
    )


def reset_game():
    global obstacles
    global score
    global speed
    global game_over
    global velocity_y
    global on_ground

    player.x = 150
    player.y = GROUND_Y - 80

    velocity_y = 0
    on_ground = True

    obstacles = []

    score = 0
    speed = 7
    game_over = False


# Головний цикл
running = True

while running:

    dt = clock.tick(60)

    # Події
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            # Стрибок
            if event.key in (pygame.K_SPACE, pygame.K_UP):

                if on_ground and not game_over:
                    velocity_y = jump_power
                    on_ground = False

            # Перезапуск
            if event.key == pygame.K_r:

                if game_over:
                    reset_game()

    # Якщо гра не закінчена
    if not game_over:

        # -----------------
        # Рух гравця
        # -----------------

        velocity_y += gravity
        player.y += velocity_y

        # Земля
        if player.bottom >= GROUND_Y:

            player.bottom = GROUND_Y
            velocity_y = 0
            on_ground = True

        # -----------------
        # Створення перешкод
        # -----------------

        spawn_timer += dt

        if spawn_timer >= spawn_delay:

            create_obstacle()

            spawn_timer = 0

            # Випадкова затримка
            spawn_delay = random.randint(800, 1600)

        # -----------------
        # Рух перешкод
        # -----------------

        for obstacle in obstacles:

            obstacle.x -= speed

        # Видаляємо перешкоди, які вийшли за екран
        obstacles = [
            obstacle
            for obstacle in obstacles
            if obstacle.right > 0
        ]

        # -----------------
        # Перевірка зіткнення
        # -----------------

        for obstacle in obstacles:

            if player.colliderect(obstacle):

                game_over = True

        # -----------------
        # Рахунок
        # -----------------

        score += 1

        # Поступово збільшуємо швидкість
        if score % 600 == 0:

            speed += 0.5

    # -----------------
    # Малювання
    # -----------------

    screen.fill(SKY)

    # Сонце
    pygame.draw.circle(
        screen,
        (255, 230, 80),
        (850, 100),
        50
    )
    # Хмари
    pygame.draw.circle(screen, WHITE, (180, 120), 30)
    pygame.draw.circle(screen, WHITE, (220, 120), 40)
    pygame.draw.circle(screen, WHITE, (260, 120), 30)

    # Земля
    pygame.draw.rect(
        screen,
        GROUND,
        (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y)
    )

    # Лінія землі
    pygame.draw.line(
        screen,
        BLACK,
        (0, GROUND_Y),
        (WIDTH, GROUND_Y),
        5
    )

    # Перешкоди
    for obstacle in obstacles:
        pygame.draw.rect(
            screen,
            RED,
            obstacle,
            border_radius=8
        )

        # Шип
        pygame.draw.polygon(
            screen,
            BLACK,
            [
                (obstacle.centerx, obstacle.y),
                (obstacle.left + 5, obstacle.bottom),
                (obstacle.right - 5, obstacle.bottom)
            ]
        )

    # Гравець
    draw_player()

    # Рахунок
    score_text = font.render(
        f"Рахунок: {score // 10}",
        True,
        BLACK
    )

    screen.blit(
        score_text,
        (20, 20)
    )

    # Швидкість
    speed_text = font.render(
        f"Швидкість: {speed:.1f}",
        True,
        BLACK
    )

    screen.blit(
        speed_text,
        (20, 60)
    )

    # -----------------
    # Game Over
    # -----------------

    if game_over:
        text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        screen.blit(
            text,
            (
                WIDTH // 2 - text.get_width() // 2,
                200
            )
        )

        restart_text = font.render(
            "Натисни R, щоб почати знову",
            True,
            BLACK
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                300
            )
        )

    pygame.display.flip()

pygame.quit()
sys.exit()