import random
import sys
import pygame

WIDTH, HEIGHT = 900, 550

PLAYER_COLOR = (80, 180, 255)
TABLE_COLOR = (140, 110, 70)
COUNTER_COLOR = (140, 110, 70)
NPC_COLOR = (255, 220, 80)

PLAYER_SPEED = 260  #pixels per sec

class Entity:
    def __init__(self, x, y, w, h, color):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = color

    def update(self, dt):
        """dt = seconds since last frame"""
        pass

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)


class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 28, 28, PLAYER_COLOR)

    def update(self, dt, keys):
        vx = vy = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vx -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vx += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            vy -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            vy += 1

        #diagonal movement
        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

        self.rect.x += int(vx * PLAYER_SPEED * dt)
        self.rect.y += int(vy * PLAYER_SPEED * dt)

        #keep in bounds
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))


class Table(Entity):
    """No implementation yet—just a rectangle in the world."""
    def __init__(self, x, y, w=70, h=40):
        super().__init__(x, y, w, h, TABLE_COLOR)

class Counter(Entity):
    """No implementation yet - just a rectangle in the world."""
    def __init__(self, x, y, w = 40, h = 240):
        super().__init__(x, y, w, h, COUNTER_COLOR)


class NPC(Entity):
    """just exists for now."""
    def __init__(self, x, y):
        super().__init__(x, y, 22, 22, NPC_COLOR)

    def update(self, dt):
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))