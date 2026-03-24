import pygame
import sys
import time
import random

# Screen Dimensions
WIDTH, HEIGHT = 1366, 768

# Game Settings
FPS = 60
PLAYER_SPEED = 7
CUSTOMER_SPEED = 2
CUSTOMER_SPAWN_EVERY_MS = 2400
MAX_CUSTOMERS = 10
MAX_CUSTOMERS_WAITING = 4
ORDER_DELAY = 4000 # milliseconds

# Colors
TABLE_COLOR = (140, 110, 70)
REGISTER_COLOR = (0, 0, 0)
COUNTER_COLOR = (140, 110, 70)
SEAT_COLOR = (0, 0, 0)
NPC_COLOR = (255, 220, 80)
UI_BG_COLOR = (30, 30, 30)
YELLOW = (255, 215, 0)
BLUE = (80, 160, 255)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORDER_COLORS = [YELLOW, BLUE]

# This dictionary starts empty and will be filled in game.py
# This prevents classes.py from trying to import game.py
IMAGE_LIBRARY = {}

# Line position coordinates for customers
LINE_POSITIONS = [(900, 385), (680, 350), (530, 350), (380, 350)]

# Time Management for Day Cycle
REAL_DAY_SEC = 86400
TIME_SPEED = 72

# Back room ingredients box positions
MAX_INGREDIENT_BOXES = 4
BOX_POSITIONS = [(50, 125), (200, 125), (350, 125), (500, 125)]

# Inventory constants
NUM_SLOTS = 4
SLOT_SIZE = 50
INVENTORY_POSITIONS = [(10, 500), (10, 560), (10, 620), (10, 680)]

# Recipe view states
RECIPE_VIEW_NONE = None
RECIPE_VIEW_MENU = "MENU"
RECIPE_VIEW_DETAIL = "DETAIL"

# Recipe UI layout constants
RECIPE_ICON_SIZE = (100, 100)
RECIPE_ICON_PADDING = 20
RECIPE_START_X = 200
RECIPE_START_Y = 200

# Input bindings
OPEN_RECIPE_MENU_KEY = pygame.K_m
CLOSE_MENU_KEY = pygame.K_ESCAPE



class GameObject:
    '''A GameObject determines an objects' position and dimensions.'''
    def __init__(self, x, y, w, h, color):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = color

    def render(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect)  # make render apply to all after making individual renders


# Ingredients Class for building all ingredients
class Ingredient(GameObject):
    """An Ingredient is---"""
    def __init__(self, name, image_keys: list, an_input=False,price_to_buy=0.0, quantity=0):
        self.image = IMAGE_LIBRARY[image_keys[0]]
        image_rect = self.image.get_rect()

        super().__init__(x=0, y=0, w=image_rect.width, h=image_rect.height, color=(0, 0, 0))

        self.name = name
        self.price = price_to_buy
        self.an_input = an_input
        self.image_keys = image_keys
        self.quantity = quantity

    def render(self, screen):
        screen.blit(self.image, (self.x, self.y))


