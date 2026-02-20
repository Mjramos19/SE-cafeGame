import pygame
import sys

import pygame
import sys


class Player:
    def __init__(self, width, height, image_path):
        # Visual dimensions
        self.width = width
        self.height = height

        # Position refers to the top-left of the whole sprite
        self.x, self.y = 40, 600
        self.speed = 5

        # 1. Define the Footprint dimensions (30*4 by 8*4)
        self.foot_w = 18 * 4
        self.foot_h = 8 * 4 

        # Load Sprite
        try:
            self.sprite = pygame.image.load(image_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))
        except:
            self.sprite = pygame.Surface((self.width, self.height))
            self.sprite.fill((255, 0, 0))

    def get_foot_rect(self):
        """ Returns a rect located at the bottom-center of the player sprite. """
        # We calculate the offset so the feet are centered horizontally
        # and sit at the very bottom of the sprite vertically.
        foot_x = self.x + (self.width // 2) - (self.foot_w // 2)
        foot_y = self.y + self.height - self.foot_h
        return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)

    def handle_movement(self, keys, collisions):
        # Store old position
        old_x, old_y = self.x, self.y

        # Move X
        if keys[pygame.K_LEFT]:  self.x -= self.speed
        if keys[pygame.K_RIGHT]: self.x += self.speed

        # Check X collision
        for c in collisions:
            if self.get_foot_rect().colliderect(c):
                self.x = old_x  # Undo X movement only

        # Move Y
        if keys[pygame.K_UP]:    self.y -= self.speed
        if keys[pygame.K_DOWN]:  self.y += self.speed

        # Check Y collision
        for c in collisions:
            if self.get_foot_rect().colliderect(c):
                self.y = old_y  # Undo Y movement only

    def render(self, screen):
        # Draw the actual character sprite
        screen.blit(self.sprite, (self.x, self.y))

        # OPTIONAL: Debugging - draw the foot rect so you can see it
        # pygame.draw.rect(screen, (0, 255, 0), self.get_foot_rect(), 2)


# --- Setup ---
pygame.init()
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Simulator")

COLORS = {'BLUE': (0, 0, 255), 'BG': (30, 30, 30)}
blue_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)
clock = pygame.time.Clock()

# 3. Pass the path to your image file here (e.g., 'player.png')
# Ensure the image file is in the same folder as your script!
player = Player((30*4), (67*4), "player.png")

collisions = [blue_rect]

# --- Main Loop ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    player.handle_movement(keys, collisions)

    screen.fill(COLORS['BG'])
    pygame.draw.rect(screen, COLORS['BLUE'], blue_rect)

    player.render(screen)

    pygame.display.flip()
    clock.tick(60)
