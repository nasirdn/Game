import pygame
from settings import STUDENT_IMAGE_PATH

class Student:
    def __init__(self):
        self.x = 500
        self.y = 50
        self.size = 70
        self.image = pygame.image.load(STUDENT_IMAGE_PATH)
        self.image = pygame.transform.scale(self.image, (self.size, self.size*1.75))
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size*1.75)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def update(self):
        self.rect.topleft = (self.x, self.y)




