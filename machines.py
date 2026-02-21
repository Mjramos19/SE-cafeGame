import pygame

class Machines():
    pass

class espressoMachine(Machines):
    def __init__(self, x, y):
        self.image = pygame.image.load('assets/espresso_machine.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

