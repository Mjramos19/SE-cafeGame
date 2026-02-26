import pygame

# Screen Dimensions
WIDTH, HEIGHT = 1366, 768

# Game Settings
FPS = 60
PLAYER_SPEED = 7
CUSTOMER_SPEED = 2
CUSTOMER_SPAWN_EVERY_MS = 2400
MAX_CUSTOMERS = 10
MAX_CUSTOMERS_WAITING = 4

# Colors
TABLE_COLOR = (140, 110, 70)
REGISTER_COLOR = (0, 0, 0)
COUNTER_COLOR = (140, 110, 70)
SEAT_COLOR = (0, 0, 0)
NPC_COLOR = (255, 220, 80)

# This dictionary starts empty and will be filled in game.py
# This prevents classes.py from trying to import game.py
IMAGE_LIBRARY = {}

# Line position coordinates for customers
LINE_POSITIONS = [(900, 385), (680, 350), (530, 350), (380, 350)]

# Recipe List
RECIPES_UNLOCKED = ["Breakfast Bagel", "Breakfast Sandwich", "Iced Coffee", "Hot Coffee"]