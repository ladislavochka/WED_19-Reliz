import pygame
import os
import sys
import time

pygame.init()
pygame.mixer.init()

sq = 80
pal_h = 90
clock_h = 25

board_w = sq * 8
board_h = sq * 8

WIDTH = board_w
HEIGHT = clock_h + pal_h + board_h + pal_h + clock_h

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("chess frr")
clock = pygame.time.Clock()

color1 = (240, 217, 181)
color2 = (181, 136, 99)
color_select = (246, 246, 105)
color_bg = (40, 40, 40)
color_pal_bg = (60, 60, 60)
color_text = (20, 20, 20)
color_text2 = (230, 230, 230)
color_clock = (230, 230, 230)
color_clock_active = (246, 246, 105)
color_clock_dead = (180, 60, 60)

this_folder = os.path.dirname(os.path.abspath(__file__))
pieces_folder = this_folder + os.sep + "pieces"

music_path = this_folder + os.sep + "music.mp3"
move_sound_path = this_folder + os.sep + "move.wav"
capture_sound_path = this_folder + os.sep + "capture.wav"

if os.path.exists(music_path):
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.set_volume(0.35)
    pygame.mixer.music.play(-1)

move_sound = None
capture_sound = None

if os.path.exists(move_sound_path):
    move_sound = pygame.mixer.Sound(move_sound_path)
    move_sound.set_volume(0.7)

if os.path.exists(capture_sound_path):
    capture_sound = pygame.mixer.Sound(capture_sound_path)
    capture_sound.set_volume(0.8)

all_codes = ["wp", "wr", "wn", "wb", "wq", "wk", "bp", "br", "bn", "bb", "bq", "bk"]

images = {}

for c in all_codes:
    p = pieces_folder + os.sep + c + ".png"

    if os.path.exists(p):
        im = pygame.image.load(p).convert_alpha()
        im = pygame.transform.smoothscale(im, (sq - 6, sq - 6))
        images[c] = im
    else:
        images[c] = None

font_big = pygame.font.SysFont("Arial", 36, bold=True)
font_small = pygame.font.SysFont("Arial", 16, bold=True)
font_clock = pygame.font.SysFont("Arial", 30, bold=True)


def draw_piece_img(code, x, y):
    img = images[code]

    if img != None:
        screen.blit(img, (x + 3, y + 3))
    else:
        col = code[0]
        typ = code[1]

        if col == "w":
            bgc = (255, 255, 255)
            fgc = (0, 0, 0)
        else:
            bgc = (25, 25, 25)
            fgc = (255, 255, 255)

        pygame.draw.circle(
            screen,
            bgc,
            (x + sq // 2, y + sq // 2),
            sq // 2 - 8
        )

        pygame.draw.circle(
            screen,
            fgc,
            (x + sq // 2, y + sq // 2),
            sq // 2 - 8,
            3
        )

        txt = font_big.render(typ.upper(), True, fgc)
        r = txt.get_rect(center=(x + sq // 2, y + sq // 2))

        screen.blit(txt, r)


def make_start_board():
    b = []

    for i in range(8):
        row = [None, None, None, None, None, None, None, None]
        b.append(row)

    order = ["r", "n", "b", "q", "k", "b", "n", "r"]

    for col in range(8):
        b[0][col] = "b" + order[col]
        b[1][col] = "bp"
        b[6][col] = "wp"
        b[7][col] = "w" + order[col]

    return b


board = make_start_board()

selected_cell = None
spawn_code = None

palette_order = ["p", "r", "n", "b", "q", "k"]

pal_slot_w = 80
pal_start_x = (WIDTH - pal_slot_w * 6) // 2

top_palette_y = clock_h
board_y = clock_h + pal_h
bottom_palette_y = board_y + board_h

top_palette_rects = []
bottom_palette_rects = []

i = 0

while i < 6:
    rx = pal_start_x + i * pal_slot_w

    top_palette_rects.append(
        pygame.Rect(rx, top_palette_y + 5, pal_slot_w - 4, pal_h - 10)
    )

    bottom_palette_rects.append(
        pygame.Rect(rx, bottom_palette_y + 5, pal_slot_w - 4, pal_h - 10)
    )

    i = i + 1


white_time = 5.0
black_time = 180.0

last_moved_color = None
last_clock_update = time.time()


def reset_clocks():
    global white_time
    global black_time
    global last_moved_color
    global last_clock_update

    white_time = 180.0
    black_time = 180.0

    last_moved_color = None
    last_clock_update = time.time()


def update_clocks():
    global white_time
    global black_time
    global last_clock_update

    now = time.time()
    dt = now - last_clock_update

    last_clock_update = now

    if last_moved_color == "w":
        if black_time > 0:
            black_time = black_time - dt

            if black_time < 0:
                black_time = 0

    if last_moved_color == "b":
        if white_time > 0:
            white_time = white_time - dt

            if white_time < 0:
                white_time = 0


def format_time(t):
    total = int(t)

    minutes = total // 60
    seconds = total % 60

    return str(minutes) + ":" + str(seconds).zfill(2)


def draw_clocks():
    black_color = color_clock
    white_color = color_clock

    if last_moved_color == "w" and black_time > 0:
        black_color = color_clock_active

    if last_moved_color == "b" and white_time > 0:
        white_color = color_clock_active

    if black_time <= 0:
        black_color = color_clock_dead

    if white_time <= 0:
        white_color = color_clock_dead

    black_txt = font_clock.render(
        "BLACK  " + format_time(black_time),
        True,
        black_color
    )

    white_txt = font_clock.render(
        "WHITE  " + format_time(white_time),
        True,
        white_color
    )

    black_rect = black_txt.get_rect(
        center=(WIDTH // 2, clock_h // 2)
    )

    white_rect = white_txt.get_rect(
        center=(WIDTH // 2, board_y + board_h + pal_h + clock_h // 2)
    )

    screen.blit(black_txt, black_rect)
    screen.blit(white_txt, white_rect)


def draw_palette():
    pygame.draw.rect(
        screen,
        color_pal_bg,
        (0, top_palette_y, WIDTH, pal_h)
    )

    pygame.draw.rect(
        screen,
        color_pal_bg,
        (0, bottom_palette_y, WIDTH, pal_h)
    )

    n = 0

    while n < 6:
        rct = top_palette_rects[n]
        code = "b" + palette_order[n]

        if spawn_code == code:
            pygame.draw.rect(screen, color_select, rct)

        draw_piece_img(code, rct.x, rct.y - 5)

        n = n + 1

    n = 0

    while n < 6:
        rct = bottom_palette_rects[n]
        code = "w" + palette_order[n]

        if spawn_code == code:
            pygame.draw.rect(screen, color_select, rct)

        draw_piece_img(code, rct.x, rct.y - 5)

        n = n + 1


files_letters = ["a", "b", "c", "d", "e", "f", "g", "h"]


def draw_board():
    for row in range(8):
        for col in range(8):

            if (row + col) % 2 == 0:
                c = color1
            else:
                c = color2

            x = col * sq
            y = board_y + row * sq

            pygame.draw.rect(
                screen,
                c,
                (x, y, sq, sq)
            )

            if selected_cell != None:
                if selected_cell[0] == row and selected_cell[1] == col:
                    pygame.draw.rect(
                        screen,
                        color_select,
                        (x, y, sq, sq),
                        5
                    )

            if col == 0:
                num_txt = font_small.render(
                    str(8 - row),
                    True,
                    color_text if c == color1 else color_text2
                )

                screen.blit(
                    num_txt,
                    (x + 4, y + 2)
                )

            if row == 7:
                letter_txt = font_small.render(
                    files_letters[col],
                    True,
                    color_text if c == color1 else color_text2
                )

                screen.blit(
                    letter_txt,
                    (x + sq - 14, y + sq - 18)
                )

    pygame.draw.rect(
        screen,
        (15, 15, 15),
        (0, board_y, board_w, board_h),
        3
    )


def draw_pieces_on_board():
    for row in range(8):
        for col in range(8):

            code = board[row][col]

            if code != None:
                x = col * sq
                y = board_y + row * sq

                draw_piece_img(
                    code,
                    x,
                    y
                )


def get_board_cell(pos):
    x, y = pos

    if y < board_y or y > board_y + board_h:
        return None

    row = (y - board_y) // sq
    col = x // sq

    return (row, col)


def get_palette_click(pos):
    n = 0

    while n < 6:
        if top_palette_rects[n].collidepoint(pos):
            return "b" + palette_order[n]

        n = n + 1

    n = 0

    while n < 6:
        if bottom_palette_rects[n].collidepoint(pos):
            return "w" + palette_order[n]

        n = n + 1

    return None


running = True

while running:

    update_clocks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            pal_click = get_palette_click(event.pos)

            if pal_click != None:

                spawn_code = pal_click
                selected_cell = None

            else:

                cell = get_board_cell(event.pos)

                if cell != None:

                    row = cell[0]
                    col = cell[1]

                    if spawn_code != None:

                        board[row][col] = spawn_code
                        spawn_code = None

                    else:

                        if selected_cell == None:

                            if board[row][col] != None:
                                selected_cell = (row, col)

                        else:

                            sr = selected_cell[0]
                            sc = selected_cell[1]

                            moving_piece = board[sr][sc]
                            target_piece = board[row][col]

                            if moving_piece != None:

                                if target_piece != None:

                                    if target_piece[0] != moving_piece[0]:

                                        board[row][col] = moving_piece
                                        board[sr][sc] = None

                                        last_moved_color = moving_piece[0]
                                        last_clock_update = time.time()

                                        if capture_sound != None:
                                            capture_sound.play()

                                    else:

                                        selected_cell = None
                                        continue

                                else:

                                    board[row][col] = moving_piece
                                    board[sr][sc] = None

                                    last_moved_color = moving_piece[0]
                                    last_clock_update = time.time()

                                    if move_sound != None:
                                        move_sound.play()

                            selected_cell = None

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:

                board = make_start_board()
                selected_cell = None
                spawn_code = None

                reset_clocks()

            if event.key == pygame.K_ESCAPE:

                selected_cell = None
                spawn_code = None

            if event.key == pygame.K_c:

                board = make_start_board()

                for row in range(8):
                    for col in range(8):
                        board[row][col] = None

                selected_cell = None
                spawn_code = None

                reset_clocks()

    screen.fill(color_bg)

    draw_clocks()
    draw_board()
    draw_pieces_on_board()
    draw_palette()

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
sys.exit()