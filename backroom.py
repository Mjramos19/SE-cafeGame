from classes import *
import pygame


class stockingShelf(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, (255, 0, 0))
        self.interactionZone = pygame.Rect(self.x - 100, self.y, self.w, self.h)
        self.spots = [
            shelfSpot(1200, 200, 20, 20),
            shelfSpot(1200, 250, 20, 20),
            shelfSpot(1230, 200, 20, 20),
            shelfSpot(1230, 250, 20, 20)
        ]

    def render(self, screen):
        super().render(screen)
        for spot in self.spots:
            spot.render(screen)


class shelfSpot(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, (0, 0, 0))

    def render(self, screen):
        super().render(screen)


class ingredientBox(GameObject):
    def __init__(self, x, y, ingredient):
        super().__init__(x, y, 100, 100, (150, 75, 0))
        self.ingredient = ingredient
        self.isEmpty = False
        self.interactionZone = pygame.Rect(self.x, self.y + 100, self.w, self.h - 50)

    def render(self, screen):
        super().render(screen)
        font = pygame.font.SysFont(None, 22)
        ingredientType = font.render(f"{self.ingredient}", True, (250, 0, 0))
        screen.blit(ingredientType, (self.rect.x, self.rect.center[1]))
        pygame.draw.rect(screen, (255, 255, 0), self.interactionZone, 2)


class DoorEntry(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, color="white")
