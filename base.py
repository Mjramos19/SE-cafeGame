import pygame
import sys

# 1. Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Red Square Scaling Game")

# Colors
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BG_COLOR = (30, 30, 30)

# 2. Rect Properties
# Red Rect: Start 1/3 up from the bottom (which is 2/3 down from the top)
red_width, red_height = 50, 50
red_x = WIDTH // 2
red_y = (HEIGHT * 2) // 3  
red_speed = 5

# Blue Rect (Static obstacle)
blue_rect = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 50, 100, 100)

# Game Clock
clock = pygame.time.Clock()

# 3. Game Loop
while True:
    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Input Handling
    keys = pygame.key.get_pressed()
    new_x, new_y = red_x, red_y

    if keys[pygame.K_LEFT]:  new_x -= red_speed
    if keys[pygame.K_RIGHT]: new_x += red_speed
    if keys[pygame.K_UP]:    new_y -= red_speed
    if keys[pygame.K_DOWN]:  new_y += red_speed

    # 4. Scaling Logic
    # Calculate scale factor based on Y position (higher screen = smaller size)
    # 0.2 is the minimum scale so it doesn't disappear completely
    scale_factor = max(0.2, (new_y / HEIGHT))
    current_w = int(red_width * scale_factor)
    current_h = int(red_height * scale_factor)

    # Create the player rect for collision math
    player_rect = pygame.Rect(new_x, new_y, current_w, current_h)

    # 5. Collision Logic
    # Only update position if it doesn't collide with the blue rect
    if not player_rect.colliderect(blue_rect):
        red_x, red_y = new_x, new_y

    # 6. Drawing
    screen.fill(BG_COLOR)
    
    # Draw Blue Rect
    pygame.draw.rect(screen, BLUE, blue_rect)
    
    # Draw Red Rect (using the calculated scale)
    pygame.draw.rect(screen, RED, (red_x, red_y, current_w, current_h))

    pygame.display.flip()
    clock.tick(60) # Limit to 60 Frames Per Second



    #new line

    