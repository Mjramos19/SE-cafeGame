import pygame
import sys


class Player:
    def __init__(self, width, height):
        self.x, self.y = 40, 600
        self.speed = 5
        self.width = width
        self.height = height

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_movement(self, keys, collisions):
        # Store old position in case we hit something
        old_x, old_y = self.x, self.y

        # Move
        if keys[pygame.K_LEFT]:  self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed
        if keys[pygame.K_UP]:    self.y -= self.speed
        if keys[pygame.K_DOWN]:  self.y += self.speed

        # Collision Check: If new position overlaps obstacle, move back
        for c in collisions:
            if self.get_rect().colliderect(c):
                self.x, self.y = old_x, old_y

    def take_order(self):
        pass

    def attempt_restock(self):
        pass

    def attempt_brew(self):
        pass

    def deliver(self):
        pass

    def render(self, screen):
        return pygame.draw.rect(screen, COLORS['RED'], player.get_rect())

