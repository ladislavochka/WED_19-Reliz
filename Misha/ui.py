import pygame


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        text = pygame.font.SysFont("comicsans", 30)
        text_surface = text.render(self.text, True, (255, 255, 255))
        window.blit(text_surface, (self.x + self.width//4, self.y+self.height//4))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]