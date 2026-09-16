import pygame
from pygame import *
pygame.init()
screen_width = 1957
screen_height = 1030
screen = display.set_mode((screen_width, screen_height))
run = True
tile_size = 103

class Player:
    def __init__(self,x,y):
        img = pygame.image.load("WED_19-Reliz/Dariy/png's/player.png")
        self.image = pygame.transform.scale(img,(65,100))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def flip(self):
        dx = 0
        dy = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            dx -= 5
        if key[pygame.K_RIGHT]:
            dx += 5
        screen.blit(self.image, self.rect)
class Cave():
    def __init__(self,data):
        self.tile_list = []
        rock_img = pygame.image.load("WED_19-Reliz/Dariy/png's/images-removebg-preview.png")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(rock_img,(tile_size,tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])


world_data = [

[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


player = Player(103,screen_height - 200)
cave = Cave(world_data)

while run:

    print(cave.tile_list)
    screen.fill(("#363835"))
    cave.draw()
    player.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    pygame.display.flip()

pygame.quit()