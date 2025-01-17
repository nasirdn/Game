import math
import pygame
from settings import BULLET_IMAGE_PATH, PLAYER_BULLET_IMAGE_PATH


class Bullet:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        self.size = 30  # Размер снаряда
        self.speed = 5  # Скорость снаряда

        self.image = pygame.image.load(BULLET_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

        # Вычисляем направление к игроку
        direction_x = target_x - self.x
        direction_y = target_y - self.y
        length = math.sqrt(direction_x ** 2 + direction_y ** 2)

        # Нормализуем вектор направления
        self.dx = direction_x / length
        self.dy = direction_y / length

    def update(self):
        self.x += self.dx * self.speed  # Двигаем снаряд в направлении игрока
        self.y += self.dy * self.speed

    def draw(self, surface):
        surface.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))



class PlayerBullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.speed = 7    # Скорость движения шарика
        self.image = pygame.image.load(PLAYER_BULLET_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def update(self):
        self.y -= self.speed  # Двигаем шарик вверх

    def draw(self, surface):
        surface.blit(self.image, (self.x - self.image.get_width() // 2, self.y - self.image.get_height() // 2))