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

    def render(self):
        return pygame.draw.rect(screen, COLORS['RED'], player.get_rect())


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
    