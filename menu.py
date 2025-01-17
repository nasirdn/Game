import pygame
import sys
from settings import MENU_BG_IMAGE_PATH, WIDTH, HEIGHT

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.play_button_rect = pygame.Rect(400, 250, 200, 100)  # Позиция и размер кнопки "Play"
        self.exit_button_rect = pygame.Rect(400, 400, 200, 100)  # Позиция и размер кнопки "Exit"

        # Загрузка изображения фона
        self.menu_bg_image = pygame.image.load(MENU_BG_IMAGE_PATH)  # Укажите путь к вашему изображению
        self.menu_bg_image = pygame.transform.scale(self.menu_bg_image, (WIDTH, HEIGHT))

    def display(self):
        self.screen.blit(self.menu_bg_image, (0, 0))
        title_text = self.font.render("Главное меню", True, (220, 20, 60))
        title_rect = title_text.get_rect(center=(500, 150))
        self.screen.blit(title_text, title_rect)

        # Отображение кнопки "Play"
        pygame.draw.rect(self.screen, (230, 230, 250), self.play_button_rect)
        play_text = self.font.render("Play", True, (205, 92, 92))
        play_text_rect = play_text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(play_text, play_text_rect)

        # Отображение кнопки "Exit"
        pygame.draw.rect(self.screen, (230, 230, 250), self.exit_button_rect)
        exit_text = self.font.render("Exit", True, (205, 92, 92))
        exit_text_rect = exit_text.get_rect(center=self.exit_button_rect.center)
        self.screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

    def wait_for_selection(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Проверяем, что нажата левая кнопка мыши
                        if self.play_button_rect.collidepoint(event.pos):
                            waiting = False  # Начать игру, если нажата кнопка "Play"
                        elif self.exit_button_rect.collidepoint(event.pos):
                            pygame.quit()  # Закрыть игру, если нажата кнопка "Exit"
                            sys.exit()
