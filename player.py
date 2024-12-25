import pygame
from pygame.sprite import Sprite

# Класс Игрока
class Player(Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 255))  # Цвет игрока (белый)
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)  # Начальная позиция игрока
        self.speed = 5
        self.direction = (0, -1)  # По умолчанию направление вверх

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.direction = (-1, 0)  # Влево
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.direction = (1, 0)  # Вправо
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.direction = (0, -1)  # Вверх
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.direction = (0, 1)  # Вниз

        # Ограничение движения по экрану
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))
