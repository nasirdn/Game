import pygame
from settings import PAPER_IMAGE_PATH, LIE_PAPER_IMAGE_PATH, RECORD_BOOK_IMAGE_PATH

class Paper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 70
        self.image = pygame.image.load(PAPER_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.topleft = (self.x, self.y)

class Liepaper:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 70
        self.image = pygame.image.load(LIE_PAPER_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.topleft = (self.x, self.y)

class Record_book:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 30
        self.image = pygame.image.load(RECORD_BOOK_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size*1.5, self.size))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.topleft = (self.x, self.y)
