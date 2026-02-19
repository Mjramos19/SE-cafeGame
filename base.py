import pygame
import os
from player1 import Player


# 1. Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cafe Simulator")

# Colors
COLORS = {
    'RED': (255, 0, 0),
    'BLUE': (0, 0, 255),
    'BG': (30, 30, 30)
}

# Blue Rect (Static obstacle)
blue_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)

# Game Clock
clock = pygame.time.Clock()

# Player Initialization (Passing width and height)
player = Player(50, 80)

# organize into lists
collisions = [blue_rect]

# game state management (main_menu, running:(front, middle, back), taking_order, machine_minigame, pause_menu, shop_menu)
GAME_STATE = 'Running'

# 3. Game Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input Handling
    keys = pygame.key.get_pressed()

    # Move player and handle collisions
    player.handle_movement(keys, collisions)

    # 6. Drawing
    screen.fill(COLORS['BG'])

    # Draw Blue Rect
    pygame.draw.rect(screen, COLORS['BLUE'], blue_rect)

    # Draw Player Rect (Red)
    player.render()

    pygame.display.flip()
    clock.tick(60)
    