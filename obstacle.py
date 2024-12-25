import pygame
from pygame.sprite import Sprite

# Класс Препятствия
class Obstacle(Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 255, 0))  # Цвет препятствия (желтый)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Позиция препятствия
