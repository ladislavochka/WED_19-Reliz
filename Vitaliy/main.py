from random import randint

import pygame

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("WED_19-Reliz/Vitaliy/verity-edit.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
jumb_sound=pygame.mixer.Sound("WED_19-Reliz/Vitaliy/jumboo.mp3")
lose_sound=pygame.mixer.Sound("WED_19-Reliz/Vitaliy/sela-dala (1).mp3")
window_size = 1200, 800
window = pygame.display.set_mode(window_size)
pygame.display.set_caption("Mega RUN")
background = pygame.image.load("WED_19-Reliz/Vitaliy/fon.jpg").convert()
background = pygame.transform.scale(background, window_size)
clock = pygame.time.Clock()
money_bag=pygame.image.load("WED_19-Reliz/Vitaliy/images (1).jfif").convert_alpha()
money_bag=pygame.transform.scale(money_bag,(140,180))
player_rect = pygame.Rect(150, 300, 100, 100)
runner=pygame.image.load("WED_19-Reliz/Vitaliy/fag.jpg").convert()
runner=pygame.transform.scale(runner,(100,120))
def generate_pipes(
    count,
    pipe_width=140,
    gap=280,
    min_height=50,
    max_height=440,
    distance=650
):
    pipes = []
    start_x = 1200

    for i in range(count):
        height = randint(min_height, max_height)
        bottom_pipe = pygame.Rect(
            start_x,
            height + gap,
            pipe_width,
            800 - (height + gap)
        )
        pipes.append(bottom_pipe)
        start_x += distance

    return pipes

pipes = generate_pipes(150)

main_font = pygame.font.Font(None, 100)
score = 0
lose = False
y_vel = 2

running = True

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_SPACE and not lose:
                y_vel = -15
                jumb_sound.play()

            if e.key == pygame.K_r:
                lose = False
                score = 0
                pipes = generate_pipes(150)
                player_rect.y = 700
                y_vel = 0

    if not lose:
        y_vel += 0.6
        player_rect.y += int(y_vel)

        if player_rect.bottom >= 800:
            player_rect.bottom = 800
            y_vel = 0
    window.blit(background,(0,0))


    window.blit(runner, player_rect)

    for pipe in pipes[:]:
        if not lose:
            pipe.x -= 10


        window.blit(money_bag, (pipe.x, pipe.y))

        money_rect = pygame.Rect(
            pipe.x,
            pipe.y,
            140,
            180
        )

        if player_rect.colliderect(money_rect):
            lose = True
            lose_sound.play()

        if pipe.x <= -140:
            pipes.remove(pipe)
            score += 0.5

    if len(pipes) <4:
        pipes += generate_pipes(150)

    score_text = main_font.render(
        f"{int(score)}",
        True,
        "black"
    )

    center_text = (1200 - score_text.get_rect().width) // 2

    window.blit(
        score_text,
        (center_text, 40)
    )

    pygame.display.update()
    clock.tick(60)

    if pygame.key.get_pressed()[pygame.K_r]:
        lose = False
        score = 0
        pipes = generate_pipes(150)
        player_rect.y = 300
        y_vel = 2





pygame.quit()