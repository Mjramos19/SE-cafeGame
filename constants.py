import pygame
import sys
import time
import random
import copy

# Screen Dimensions
WIDTH, HEIGHT = 1366, 768

# Game Settings
FPS = 60
PLAYER_SPEED = 7
CUSTOMER_SPEED = 2
#CUSTOMER_SPAWN_EVERY_MS = 2400
CUSTOMER_SPAWN_EVERY_MS = 4000
MAX_CUSTOMERS = 10
MAX_CUSTOMERS_WAITING = 4
ORDER_DELAY = 4000 # milliseconds

""" Colors """
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
LINE_POSITIONS = [(840, 350), (660, 335), (490, 320), (320, 305)]

CUSTOMER_ENTRY_X = -130
CUSTOMER_ENTRY_Y = 315

# Time Management for Day Cycle
REAL_DAY_SEC = 86400
TIME_SPEED = 72

DAY_START = 21600
SEVEN_AM = 25200
EIGHT_AM = 28800
DAY_END = 64800

# Back room ingredients box positions
MAX_INGREDIENT_BOXES = 4
BOX_POSITIONS = [(750, 200), (875, 200), (1000, 200), (1125, 200)]

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

"""
Cafe Game Base Classes Module.
Defines core game objects and ingredient logic for the cafe simulation.
"""

class GameObject:
    """
    A base class for all interactable and rendered entities in the game.

    Attributes:
        x (int): Horizontal coordinate.
        y (int): Vertical coordinate.
        w (int): Width of the object.
        h (int): Height of the object.
        rect (pygame.Rect): The collision and boundary rectangle.
        color (tuple): RGB color value for default rendering.
    """
    def __init__(self, x, y, w, h, color):
        """Initializes position, dimensions, and the pygame Rect object."""
        self.x, self.y, self.w, self.h = x, y, w, h
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)

    def render(self, screen):
        """Draws a simple rectangle to the screen if no sprite is provided."""
        pygame.draw.rect(screen, self.color, self.rect)


class Ingredient(GameObject):
    """
    Represents individual items used in recipes or stored in inventory.

    Attributes:
        name (str): The display name of the ingredient.
        image (pygame.Surface): The current sprite for rendering.
        price (float): Cost to purchase the ingredient.
        an_input (bool): True if the item is a raw material for a machine.
        stackable (bool): Determines if multiple units occupy one inventory slot.
    """
    def __init__(self, name, image_keys, an_input=False, price_to_buy=0.0, quantity=0):
        """Sets up ingredient properties and pulls the initial sprite from the library."""
        self.image_keys = image_keys
        self.image = IMAGE_LIBRARY[self.image_keys[0]]
        image_rect = self.image.get_rect()

        # Initialize base GameObject with image dimensions
        super().__init__(x=0, y=0, w=image_rect.width, h=image_rect.height, color=(0, 0, 0))

        self.name = name
        self.price = price_to_buy
        self.an_input = an_input
        self.quantity = quantity
        self.stackable = True

    def render(self, screen):
        """Blits the ingredient's sprite at its current coordinates."""
        screen.blit(self.image, (self.x, self.y))