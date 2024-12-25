import pygame
from player import Player
from shot import Shot
from enemy import Enemy
from obstacle import Obstacle

# Константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Это программа 'Сдохни или умри'")
        self.clock = pygame.time.Clock()

        self.player, self.all_sprites, self.shots, self.enemies, self.obstacles = self.reset_game()

    def reset_game(self):
        """Сброс игры и создание новых объектов."""
        player = Player()
        all_sprites = pygame.sprite.Group()
        shots = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()

        all_sprites.add(player)

        # Создание препятствий
        obstacle1 = Obstacle(300, 200, 200, 20)
        obstacle2 = Obstacle(500, 400, 20, 200)
        obstacles.add(obstacle1, obstacle2)
        all_sprites.add(obstacle1, obstacle2)

        # Создание врагов
        for i in range(5):  # Создаем 5 врагов
            enemy = Enemy(100 + i * 100, 100)
            enemies.add(enemy)
            all_sprites.add(enemy)

        return player, all_sprites, shots, enemies, obstacles

    def run_game(self):
        """Основной игровой цикл."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Обработка нажатия клавиш
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                    if event.key == pygame.K_SPACE:
                        shot = Shot(self.player.rect.centerx, self.player.rect.centery, self.player.direction)
                        self.all_sprites.add(shot)
                        self.shots.add(shot)

            # Обновление всех спрайтов, кроме врагов
            for sprite in self.all_sprites:
                if not isinstance(sprite, Enemy):  # Проверяем, что это не враг
                    sprite.update()

            # Обновление врагов с передачей необходимых аргументов
            for enemy in self.enemies:
                enemy.update(self.player, self.obstacles)

            # Проверка на коллизии между снарядами и врагами
            for shot in self.shots:
                hit_enemies = pygame.sprite.spritecollide(shot, self.enemies, False)  # Проверяем коллизии
                for enemy in hit_enemies:
                    enemy.kill()  # Удаляем врага
                    shot.kill()   # Удаляем снаряд
                    break  # Выходим из цикла, так как снаряд может столкнуться только с одним врагом

            # Проверка на столкновения между игроком и врагами
            if pygame.sprite.spritecollideany(self.player, self.enemies):  # Если есть столкновение
                print("Игрок убит! Начинаем новую игру...")
                self.player, self.all_sprites, self.shots, self.enemies, self.obstacles = self.reset_game()  # Сброс игры

            # Отрисовка
            self.screen.fill((0, 0, 0))  # Цвет фона (черный)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            # Установка FPS
            self.clock.tick(FPS)

        pygame.quit()


