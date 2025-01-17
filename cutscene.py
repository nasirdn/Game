import pygame
import sys
from settings import CUTSCENE_IMAGE_PATH, HERO_CUTSCENE_IMAGE_PATH, WIDTH, HEIGHT, BACKGROUND_IMAGE_PATH, STUDENT_CS_IMAGE_PATH, BOSS_CS_IMAGE_PATH

class Cutscene:
    def __init__(self, screen):
        self.screen = screen
        self.cutscene_image = pygame.image.load(CUTSCENE_IMAGE_PATH)
        self.cutscene_image = pygame.transform.scale(self.cutscene_image, (WIDTH, HEIGHT))
        self.hero_image = pygame.image.load(HERO_CUTSCENE_IMAGE_PATH)

    def display(self):
        # Отображение кат-сцены
        self.screen.blit(self.cutscene_image, (0, 0))

        # Создание прямоугольника для текста
        rect_height = 150
        rect_y = pygame.display.get_surface().get_height() - rect_height
        rect_color = (0, 0, 0, 128)

        hero_rect = self.hero_image.get_rect(midleft=(50, rect_y + rect_height // 2))
        hero_rect.bottom = rect_y + 150

        self.screen.blit(self.hero_image, hero_rect)
        pygame.draw.rect(self.screen, rect_color, (0, rect_y, pygame.display.get_surface().get_width(), rect_height))

        font = pygame.font.Font(None, 36)
        dialog_text = "Сегодня самый сложный экзамен, а я ничего не учил. Точно неуд поставит... Думаю, что я не один такой, может мы с одногруппниками что-то сможем придумать."

        wrapped_text = self.wrap_text(dialog_text, font, pygame.display.get_surface().get_width())
        for i, line in enumerate(wrapped_text):
            text_surface = font.render(line.strip(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(pygame.display.get_surface().get_width() // 2, rect_y + rect_height // 2 - (len(wrapped_text) * 18) // 2 + i * 36))
            self.screen.blit(text_surface, text_rect)

        font_inst = pygame.font.Font(None, 24)
        instr_text = "Нажми SPACE, чтобы продолжить..."
        surface_text = font_inst.render(instr_text, True, (255, 255, 244))
        rect_text = surface_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(surface_text, rect_text)

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

    def wait_for_space(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()

class Dial_cutscene:
    def __init__(self, screen):
        self.screen = screen
        self.dial_cutscene_image = pygame.image.load(BACKGROUND_IMAGE_PATH)
        self.dial_cutscene_image = pygame.transform.scale(self.dial_cutscene_image, (WIDTH, HEIGHT))
        self.student_image = pygame.image.load(STUDENT_CS_IMAGE_PATH)
        self.hero_image = pygame.image.load(HERO_CUTSCENE_IMAGE_PATH)

        self.texts = [" ",
                      "Утро. Ты готовилась к экзамену?",
                      "И тебе. О ну нет, я смотрела мультики всю ночь. Максимум моих действий вчера было написать шпаргалки.",
                      "О! Можешь поделиться?",
                      "Извини, но я сделала только для себя. Могу тебе сказать, что кто-то из наших раскидал шпоры за ненадобностью. Только будь аккуратен среди шпаргалок есть те, которые подкинул препод, там могут быть не правильные ответы.",
                      "Спасибо! С меня шоколадка!"
                      ]
        self.colors = [(255, 255, 255), (74, 55, 255)]

    def display(self):
        # Отображение кат-сцены
        self.screen.blit(self.dial_cutscene_image, (0, 0))

        # Создание прямоугольника для текста
        rect_height = 150
        rect_y = pygame.display.get_surface().get_height() - rect_height
        rect_color = (0, 0, 0, 128)

        # герой
        hero_rect = self.hero_image.get_rect(midleft=(50, rect_y + rect_height // 2))
        hero_rect.bottom = rect_y + 200

        self.screen.blit(self.hero_image, hero_rect)

        # студент
        student_rect = self.student_image.get_rect(midleft=(hero_rect.right + 250, hero_rect.centery))
        student_rect.bottom = rect_y + 150

        self.screen.blit(self.student_image, student_rect)
        pygame.draw.rect(self.screen, rect_color, (0, rect_y, pygame.display.get_surface().get_width(), rect_height))

        font = pygame.font.Font(None, 36)

        line_text = 1  # Начинаем с первой реплики
        while line_text < len(self.texts):
            # Очищаем экран перед отрисовкой новой реплики
            self.screen.blit(self.dial_cutscene_image, (0, 0))  # Перерисовываем фон
            self.screen.blit(self.hero_image, hero_rect)  # Перерисовываем героя
            self.screen.blit(self.student_image, student_rect)  # Перерисовываем студента
            pygame.draw.rect(self.screen, rect_color, (0, rect_y, pygame.display.get_surface().get_width(), rect_height))  # Перерисовываем прямоугольник

            COLOR = self.colors[line_text % len(self.colors)]

            dialog_text = self.texts[line_text]

            wrapped_text = self.wrap_text(dialog_text, font, pygame.display.get_surface().get_width())
            for i, line in enumerate(wrapped_text):
                text_surface = font.render(line.strip(), True, COLOR)
                text_rect = text_surface.get_rect(center=(pygame.display.get_surface().get_width() // 2,
                                                          rect_y + rect_height // 2 - (
                                                                  len(wrapped_text) * 18) // 2 + i * 36))
                self.screen.blit(text_surface, text_rect)

            pygame.display.flip()  # Обновляем экран

            # Ожидаем нажатия мыши для смены реплики
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        line_text += 1  # Переход к следующей реплике
                        waiting = False  # Выходим из цикла ожидания

        # После завершения всех реплик
        font_inst = pygame.font.Font(None, 24)
        instr_text = "Нажми SPACE, чтобы продолжить..."
        surface_text = font_inst.render(instr_text, True, (255, 255, 244))
        rect_text = surface_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(surface_text, rect_text)

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

    def wait_for_space(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()



class Final_cutscene:
    def __init__(self, screen):
        self.screen = screen
        self.cutscene_image = pygame.image.load(BOSS_CS_IMAGE_PATH)
        self.cutscene_image = pygame.transform.scale(self.cutscene_image, (WIDTH, HEIGHT))
        self.hero_image = pygame.image.load(HERO_CUTSCENE_IMAGE_PATH)

    def display(self):
        # Отображение кат-сцены
        self.screen.blit(self.cutscene_image, (0, 0))

        # Создание прямоугольника для текста
        rect_height = 150
        rect_y = pygame.display.get_surface().get_height() - rect_height
        rect_color = (0, 0, 0, 128)

        hero_rect = self.hero_image.get_rect(midleft=(50, rect_y + rect_height // 2))
        hero_rect.bottom = rect_y + 150

        self.screen.blit(self.hero_image, hero_rect)
        pygame.draw.rect(self.screen, rect_color, (0, rect_y, pygame.display.get_surface().get_width(), rect_height))

        font = pygame.font.Font(None, 36)
        dialog_text = "Фух. Наконец-то с монстром покончено. Осталось собрать зачетки, которые разлетелись по всей аудитории."

        wrapped_text = self.wrap_text(dialog_text, font, pygame.display.get_surface().get_width())
        for i, line in enumerate(wrapped_text):
            text_surface = font.render(line.strip(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(pygame.display.get_surface().get_width() // 2, rect_y + rect_height // 2 - (len(wrapped_text) * 18) // 2 + i * 36))
            self.screen.blit(text_surface, text_rect)

        font_inst = pygame.font.Font(None, 24)
        instr_text = "Нажми SPACE, чтобы продолжить..."
        surface_text = font_inst.render(instr_text, True, (255, 255, 244))
        rect_text = surface_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(surface_text, rect_text)

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

    def wait_for_space(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()



class Boss_cs:
    def __init__(self, screen):
        self.screen = screen
        self.boss_cutscene_image = pygame.image.load(BOSS_CS_IMAGE_PATH)
        self.boss_cutscene_image = pygame.transform.scale(self.boss_cutscene_image, (WIDTH, HEIGHT))
        self.hero_image = pygame.image.load(HERO_CUTSCENE_IMAGE_PATH)

    def display(self):
        # Отображение кат-сцены
        self.screen.blit(self.boss_cutscene_image, (0, 0))

        # Создание прямоугольника для текста
        rect_height = 150
        rect_y = pygame.display.get_surface().get_height() - rect_height
        rect_color = (0, 0, 0, 128)

        hero_rect = self.hero_image.get_rect(midleft=(50, rect_y + rect_height // 2))
        hero_rect.bottom = rect_y + 150

        self.screen.blit(self.hero_image, hero_rect)
        pygame.draw.rect(self.screen, rect_color, (0, rect_y, pygame.display.get_surface().get_width(), rect_height))

        font = pygame.font.Font(None, 36)
        dialog_text = "Ну я только дописал! Монстр украл наши зачетки! Кажется, если попасться ему экзамен будет завален! Нужно как-то отобрать зачётки, но у меня под рукой только методички! У меня нет другого выбора."

        wrapped_text = self.wrap_text(dialog_text, font, pygame.display.get_surface().get_width())
        for i, line in enumerate(wrapped_text):
            text_surface = font.render(line.strip(), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(pygame.display.get_surface().get_width() // 2, rect_y + rect_height // 2 - (len(wrapped_text) * 18) // 2 + i * 36))
            self.screen.blit(text_surface, text_rect)

        font_inst = pygame.font.Font(None, 24)
        instr_text = "Нажми SPACE, чтобы продолжить..."
        surface_text = font_inst.render(instr_text, True, (255, 255, 244))
        rect_text = surface_text.get_rect(topright=(self.screen.get_width() - 10, 10))
        self.screen.blit(surface_text, rect_text)

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

    def wait_for_space(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()


