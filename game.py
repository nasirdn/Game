import pygame
import sys
import random
from settings import WIDTH, HEIGHT, SQUARE_SIZE, SQUARE_SPEED, BACKGROUND_IMAGE_PATH, HERO_IMAGE_PATH, BOSS_CS_IMAGE_PATH, BOSS_IMAGE_PATH, pl_bullet_allowed
from cutscene import Cutscene, Dial_cutscene, Final_cutscene, Boss_cs
from menu import Menu
from student import Student
from paper import Paper, Liepaper, Record_book
from bullet import Bullet, PlayerBullet


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Exam")

        self.background_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))

        self.boss_bg_image = pygame.image.load(BOSS_CS_IMAGE_PATH)
        self.boss_bg_image = pygame.transform.scale(self.boss_bg_image, (WIDTH, HEIGHT))

        # Загрузка изображения героя
        self.hero_image = pygame.image.load(HERO_IMAGE_PATH)
        self.hero_image = pygame.transform.scale(self.hero_image, (SQUARE_SIZE, SQUARE_SIZE * 1.75))

        self.boss_image = pygame.image.load(BOSS_IMAGE_PATH)
        self.boss_image = pygame.transform.scale(self.boss_image, (2 * SQUARE_SIZE, 2 * SQUARE_SIZE))

        self.square_x = WIDTH // 2 - SQUARE_SIZE // 2
        self.square_y = HEIGHT - 5 * SQUARE_SIZE

        # Состояние игры
        self.state = 'menu'  # Начальное состояние - меню
        self.menu = Menu(self.screen)
        self.cutscene = Cutscene(self.screen)
        self.student = Student()
        self.dial_cutscene = Dial_cutscene(self.screen)
        self.boss_cs = Boss_cs(self.screen)
        self.final_cs = Final_cutscene(self.screen)

        self.boss_x = WIDTH // 2
        self.boss_y = 40
        self.boss_health = 100
        self.player_health = 100

        self.bullets = []  # Список для хранения снарядов
        self.bullet_timer = 0  # Таймер для стрельбы

        self.player_bullets = []
        self.space_pressed = False

        self.papers = []
        self.liepapers = []
        self.record_books = []
        self.score = 0
        self.books = 0


    def display_menu(self):
        self.menu.display()
        self.menu.wait_for_selection()
        self.state = 'cutscene'

    def display_cutscene(self):
        self.cutscene.display()
        self.cutscene.wait_for_space()
        self.state = 'show_characters'

    def display_final_cutscene(self):
        self.final_cs.display()
        self.final_cs.wait_for_space()
        self.state = 'collect_books'
        self.create_record_books(5)

    def display_show_characters(self):
        # Отрисовка фона
        self.screen.blit(self.background_image, (0, 0))
        # Отрисовка героя
        self.screen.blit(self.hero_image, (self.square_x, self.square_y))
        # Отрисовка студента
        self.student.draw(self.screen)
        # Проверка на взаимодействие между героем и студентом
        if self.check_collision_with_student():
            # Здесь можно, например, перейти к диалоговой кат-сцене
            self.state = 'dial_cutscene'  # Переход к диалоговой кат-сцене

        pygame.display.flip()

    def check_collision_with_student(self):
        # Проверка, находится ли герой в пределах досягаемости студента
        hero_rect = pygame.Rect(self.square_x, self.square_y, SQUARE_SIZE, SQUARE_SIZE * 1.75)
        student_rect = pygame.Rect(self.student.x, self.student.y, self.student.size, self.student.size)

        check = hero_rect.colliderect(student_rect)
        # Проверка на взаимодействие с студентом
        if check:
            self.state = 'dial_cutscene'

    def display_dial_cutscene(self):
        self.dial_cutscene.display()
        self.dial_cutscene.wait_for_space()
        self.state = 'collect'
        self.create_papers(5)  # Создаем 5 обычных шпор
        self.create_liepapers(3)

    def create_papers(self, count):
        for _ in range(count):
            while True:
                x = random.randint(60, WIDTH - 60)
                y = random.randint(60, HEIGHT - 60)

                # Проверка, чтобы шпоры не появлялись в ограниченных местах
                if not (x + y < WIDTH - 9 * SQUARE_SIZE or x - y > 9 * SQUARE_SIZE):
                    break

            self.papers.append(Paper(x, y))

    def create_liepapers(self, count):
        for _ in range(count):
            while True:
                x = random.randint(60, WIDTH - 60)
                y = random.randint(60, HEIGHT - 60)

                # Проверка, чтобы лжешпоры не появлялись в ограниченных местах
                if not (x + y < WIDTH - 9 * SQUARE_SIZE or x - y > 9 * SQUARE_SIZE):
                    break

            self.liepapers.append(Liepaper(x, y))

    def create_record_books(self, count):
        for _ in range(count):
            while True:
                x = random.randint(200, WIDTH - 200)
                y = random.randint(100, HEIGHT - 200)
                break
            self.record_books.append(Record_book(x, y))

    def collect_paper(self):
        # Проверка на сбор шпор
        for paper in self.papers[:]:  # Создаем копию списка для безопасного изменения
            if self.square_x < paper.x + paper.size and self.square_x + SQUARE_SIZE > paper.x and \
                    self.square_y < paper.y + paper.size and self.square_y + SQUARE_SIZE > paper.y:
                self.papers.remove(paper)  # Удаление бумаги из списка
                self.score += 1

        for liepaper in self.liepapers[:]:  # Создаем копию списка для безопасного изменения
            if self.square_x < liepaper.x + liepaper.size and self.square_x + SQUARE_SIZE > liepaper.x and \
                    self.square_y < liepaper.y + liepaper.size and self.square_y + SQUARE_SIZE > liepaper.y:
                self.liepapers.remove(liepaper)  # Удаление бумаги из списка
                self.score -= 1
                if self.score < 0:
                    self.score = 0

        for record_book in self.record_books[:]:  # Создаем копию списка для безопасного изменения
            if self.square_x < record_book.x + record_book.size and self.square_x + SQUARE_SIZE > record_book.x and \
                    self.square_y < record_book.y + record_book.size and self.square_y + SQUARE_SIZE > record_book.y:
                self.record_books.remove(record_book)  # Удаление бумаги из списка
                self.books += 1

    def final_draw(self):
        self.screen.blit(self.boss_bg_image, (0, 0))  # Отрисовываем изображение фона
        self.screen.blit(self.hero_image, (self.square_x, self.square_y))

        for record_book in self.record_books:
            record_book.draw(self.screen)

        # Отображение счётчика
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Зачетки: {self.books}', True, (220, 20, 60))

        # Вычисляем позицию для центрирования текста
        text_rect = score_text.get_rect(center=(WIDTH // 2, 20))  # 20 - это отступ от верхней границы
        self.screen.blit(score_text, text_rect)

        if self.books == 5:
            font = pygame.font.Font(None, 36)
            if self.score == 2:
                self.screen.fill((205, 92, 92))
                text = font.render(f"О нет, у меня «{self.score}».", True, (255, 255, 255))
                text2 = font.render(f"Придется идти на дополнительную сессию. Грустно.", True, (255, 255, 255))
            elif self.score == 3:
                self.screen.fill((205, 92, 92))
                text = font.render(f"Слава всему у меня «{self.score}».", True, (255, 255, 255))
                text2 = font.render(f"Мне не придется идти на дополнительную сессию, но стипендию тоже хотелось...", True, (255, 255, 255))
            elif self.score == 4:
                self.screen.fill((60, 179, 113))
                text = font.render(f"Хорошо, я в шоке, у меня «{self.score}».", True, (255, 255, 255))
                text2 = font.render(f"Дополнительной сессии нет, а стипендия есть. Я рад.", True, (255, 255, 255))
            else:
                self.screen.fill((60, 179, 113))
                text = font.render(f"Я не знаю как у меня получилось заработать «{self.score}».", True, (255, 255, 255))
                text2 = font.render(f"Я чувствую себя самым удачливым человеком!", True, (255, 255, 255))

            t_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, t_rect)

            text_height = text.get_height()

            t_rect2 = text2.get_rect(center=(WIDTH // 2, t_rect.bottom + text_height + 10))
            self.screen.blit(text2, t_rect2)

        pygame.display.flip()

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + ' '
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + ' '

        if current_line:
            lines.append(current_line)

        return lines

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))  # Отрисовываем изображение фона
        self.screen.blit(self.hero_image, (self.square_x, self.square_y))  # Отрисовываем изображение героя

        # Отрисовка шпор
        for paper in self.papers:
            paper.draw(self.screen)

        for liepaper in self.liepapers:
            liepaper.draw(self.screen)

        # Отображение счётчика
        font = pygame.font.Font(None, 36)
        score_text = font.render(f'Отметка: {self.score}', True, (220, 20, 60))

        # Вычисляем позицию для центрирования текста
        text_rect = score_text.get_rect(center=(WIDTH // 2, 20))  # 20 - это отступ от верхней границы
        self.screen.blit(score_text, text_rect)

        pygame.display.flip()

        if len(self.papers) == 0:
            self.state = 'boss_cutscene'

    def display_boss_cutscene(self):
        self.boss_cs.display()
        self.boss_cs.wait_for_space()
        self.state = 'boss'

    def display_show_boss(self):
        self.screen.blit(self.boss_bg_image, (0, 0))
        self.screen.blit(self.hero_image, (self.square_x, self.square_y))
        self.screen.blit(self.boss_image, (self.boss_x - SQUARE_SIZE, self.boss_y))

        for bullet in self.bullets:
            bullet.draw(self.screen)

        self.draw_player_bullets()  # Отрисовываем снаряды игрока

        # Отображение здоровья босса
        font = pygame.font.Font(None, 36)
        health_text = font.render(f'Здоровье монстра: {self.boss_health}', True, (255, 0, 0))
        self.screen.blit(health_text, (WIDTH // 2 - 350, 20))  # Отображаем здоровье в верхней части экрана

        # Отображение здоровья игрока
        font = pygame.font.Font(None, 36)
        health_text = font.render(f'Здоровье игрока: {self.player_health}', True, (255, 0, 0))
        self.screen.blit(health_text, (WIDTH // 2 - 350, 40))

        pygame.display.flip()

    def shoot_bullet(self):
        bullet = Bullet(self.boss_x, self.boss_y, self.square_x + SQUARE_SIZE // 2, self.square_y)
        self.bullets.append(bullet)

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y > HEIGHT-2*SQUARE_SIZE or bullet.x < 2*SQUARE_SIZE or bullet.x > WIDTH-2*SQUARE_SIZE:
                self.bullets.remove(bullet)

    def check_bullet_collision(self):
        hero_rect = pygame.Rect(self.square_x, self.square_y, SQUARE_SIZE, SQUARE_SIZE * 1.75)
        boss_rect = pygame.Rect(self.boss_x - SQUARE_SIZE // 2, self.boss_y, 2 * SQUARE_SIZE, 2 * SQUARE_SIZE)

        for bullet in self.player_bullets[:]:  # Создаем копию списка для безопасного изменения
            bullet_rect = pygame.Rect(bullet.x - bullet.size, bullet.y - bullet.size, bullet.size * 2, bullet.size * 2)
            if bullet_rect.colliderect(boss_rect):
                self.boss_health -= 20  # Уменьшаем здоровье босса на 10
                self.player_bullets.remove(bullet)
                if self.boss_health <= 0:
                    self.state = 'final_cs'

        for bullet in self.bullets[:]:  # Создаем копию списка для безопасного изменения
            bullet_rect = pygame.Rect(bullet.x - bullet.size, bullet.y - bullet.size, bullet.size * 2, bullet.size * 2)
            if bullet_rect.colliderect(hero_rect):
                self.player_health -= 10  # Уменьшаем здоровье босса на 10
                self.bullets.remove(bullet)
                # Проверка, если здоровье игрока достигло 0
                if self.player_health <= 0:
                    self.state = 'menu'
                    self.player_health = 100

    def shoot_player_bullet(self):
        # Создаем шарик из текущей позиции игрока
        if len(self.player_bullets) < pl_bullet_allowed:
            bullet = PlayerBullet(self.square_x + SQUARE_SIZE // 2, self.square_y)
            self.player_bullets.append(bullet)  # Добавляем шарик в список снарядов

    def update_player_bullets(self):
        for bullet in self.player_bullets[:]:
            bullet.update()
            if bullet.y < 2*SQUARE_SIZE or bullet.x < 2*SQUARE_SIZE or bullet.x > WIDTH-2*SQUARE_SIZE:
                self.player_bullets.remove(bullet)

    def draw_player_bullets(self):
        for bullet in self.player_bullets:
            bullet.draw(self.screen)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.square_x -= SQUARE_SPEED
        if keys[pygame.K_RIGHT]:
            self.square_x += SQUARE_SPEED
        if keys[pygame.K_UP]:
            self.square_y -= SQUARE_SPEED
        if keys[pygame.K_DOWN]:
            self.square_y += SQUARE_SPEED
        if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

        # Ограничение перемещения героя по краям экрана
        self.square_x = max(0, min(self.square_x, WIDTH - SQUARE_SIZE))
        self.square_y = max(0, min(self.square_y, HEIGHT - 1.75 * SQUARE_SIZE))

        if self.state == 'collect' or self.state == 'show_characters':
            # Ограничение перемещения героя по диагонали слева
            if self.square_x + self.square_y < WIDTH - 8 * SQUARE_SIZE:
                excess = (self.square_x + self.square_y) - (WIDTH - 8 * SQUARE_SIZE)
                if self.square_x > self.square_y:
                    self.square_x -= excess
                else:
                    self.square_y -= excess

            # Ограничение перемещения героя по диагонали справа
            if self.square_x - self.square_y > 8 * SQUARE_SIZE:
                excess = (self.square_x - self.square_y) - (8 * SQUARE_SIZE)
                if self.square_x < self.square_y:
                    self.square_x -= excess
                else:
                    self.square_y += excess

        elif self.state == 'boss' or self.state == 'collect_books':
            self.square_x = max(145, min(self.square_x, WIDTH - 3*SQUARE_SIZE))
            self.square_y = max(50, min(self.square_y, HEIGHT - 3*SQUARE_SIZE))

    def update_shoot(self):
        # Логика стрельбы
        self.bullet_timer += 1
        if self.bullet_timer >= 20:
            self.shoot_bullet()
            self.bullet_timer = 0

        # Логика стрельбы игрока
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not self.space_pressed:  # Если пробел не зажат
            self.shoot_player_bullet()
            self.space_pressed = True  # Установить флаг, что пробел зажат
        elif not keys[pygame.K_SPACE]:
            self.space_pressed = False  # Сбросить флаг, если пробел отпущен

        self.update_player_bullets()  # Обновляем снаряды игрока

        self.update_bullets()
        self.check_bullet_collision()

    def run(self):
        while True:

            if self.state == 'menu':
                self.display_menu()
            elif self.state == 'cutscene':
                self.display_cutscene()
            elif self.state == 'show_characters':
                self.display_show_characters()
                self.update()
            elif self.state == 'dial_cutscene':
                self.display_dial_cutscene()
            elif self.state == 'collect':
                self.update()
                self.collect_paper()
                self.draw()
            elif self.state == 'boss_cutscene':
                self.display_boss_cutscene()
            elif self.state == 'boss':
                self.display_show_boss()
                self.update()
                self.update_shoot()
            elif self.state == 'final_cs':
                self.display_final_cutscene()
            elif self.state == 'collect_books':
                self.update()
                self.collect_paper()
                self.final_draw()

            self.handle_events()
            pygame.time.Clock().tick(60)



