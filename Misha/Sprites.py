import pygame
from math import cos, sin, radians
from settings import velocity, angle, gravity, SCREEN_WIDTH

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = 25
        self.height = 25

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))


class Bullet:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = 10
        self.width = self.radius
        self.height = self.radius
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
    def draw(self, window):
        pygame.draw.circle(window, self.color, (int(self.x), int(self.y)), self.radius)

    def reset(self):
        self.x = -20
        self.y = -20
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def move(self, turn, t):
        import main as game_state
        player1 = game_state.player1
        player2 = game_state.player2
        if turn == 1:
            self.x = player1.x + player1.width + velocity * cos(radians(angle)) * t
            self.y = player1.y + player1.height // 2 - (velocity * sin(radians(angle)) * t - 0.5 * gravity * t**2)
        else:
            self.x = player2.x - velocity * cos(radians(angle)) * t
            self.y = player2.y + player2.height // 2 - (velocity * sin(radians(angle)) * t - 0.5 * gravity * t**2)
            
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        
    def explosion(self):
        from main import ground
        if self.rect.colliderect(ground.rect):
            collision_x = int(self.x - ground.x)
            collision_y = int(self.y - ground.y)
            radius = 15
            ground.create_crater(collision_x, collision_y, radius)


class Ground:
    def __init__(self, x, y, width, height, color=(90, 60, 30, 255)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.surface.fill((149, 104, 25, 255))

    def draw(self, window):
        window.blit(self.surface, (self.x, self.y))

    def draw_polygon(self, points, color=None):
        pygame.draw.polygon(self.surface, color or self.color, points)

    def create_crater(self, local_x, local_y, radius):
        size = radius * 2
        temp = pygame.Surface((size, size), pygame.SRCALPHA)
        temp.fill((0, 0, 0, 0))
        pygame.draw.circle(temp, (0, 0, 0, 255), (radius, radius), radius)
        blit_x = local_x - radius
        blit_y = local_y - radius
        self.surface.blit(temp, (blit_x, blit_y), special_flags=pygame.BLEND_RGBA_SUB)

