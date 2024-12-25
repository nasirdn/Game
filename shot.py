import pygame
from pygame.sprite import Sprite

# Класс для Шариков
class Shot(Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Размер шарика
        self.image.fill((255, 0, 0))  # Цвет шарика (красный)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Позиция шарика
        self.speed = 10  # Скорость движения шарика

        # Определение направления движения шарика
        self.direction = direction

    def update(self):
        # Движение шарика в зависимости от направления
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

        # Уничтожение шарика, если он выходит за пределы экрана
        if self.rect.bottom < 0 or self.rect.top > 600 or self.rect.right < 0 or self.rect.left > 800:
            self.kill()




