import pygame
import math
from pygame.sprite import Sprite

# Класс Врага
class Enemy(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 255, 0))  # Цвет врага (зеленый)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Начальная позиция врага
        self.speed = 2  # Скорость движения врага

    def update(self, player, obstacles):
        # Вычисляем направление к игроку
        direction_x = player.rect.centerx - self.rect.centerx
        direction_y = player.rect.centery - self.rect.centery
        distance = math.hypot(direction_x, direction_y)

        if distance > 0:  # Если враг не на месте
            direction_x /= distance  # Нормализация
            direction_y /= distance  # Нормализация

            # Обновляем позицию врага
            new_rect = self.rect.move(direction_x * self.speed, direction_y * self.speed)

            # Проверка на столкновение с препятствиями
            for obstacle in obstacles:
                if new_rect.colliderect(obstacle.rect):
                    break  # Если столкновение, не перемещаем врага
            else:
                self.rect = new_rect  # Если нет столкновения, перемещаем врага
