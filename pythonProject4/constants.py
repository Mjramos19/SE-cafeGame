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
ORDER_DELAY = 4000 # milliseconds

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

# Ingredients Class for building all ingredients
class Ingredient:
    def __init__(self, name, images:list, price_to_buy=None, quantity=None):
        if isinstance(name, str):
            self.name = name
        if isinstance(price_to_buy, int):
            self.price = price_to_buy
        if isinstance(images, list):
            self.images = images
        if isinstance(quantity, int):
            self.quantity = int

bag_coffee_beans = Ingredient("Coffee Beans", ["img"], 18.35, 56)
ground_coffee = Ingredient("Ground Coffee",["img"])
espresso_shot = Ingredient("Espresso Shot",["img"])
espresso_doubleShot = Ingredient("Espresso Double Shot",["img"])
water = Ingredient("Water",["img"])
hot_water = Ingredient("Hot Water",["img"])
ice = Ingredient("Ice",["img"])
milk = Ingredient("Milk",["img"], 3.28, 16)
steamed_milk = Ingredient("Steamed Milk",["img"])
foamed_milk = Ingredient("Foamed Milk",["img"])
cocoa_powder = Ingredient("Cocoa Powder",["img"], 9.40, 64)
hot_chocolate = Ingredient("Hot Chocolate",["img"])

# Ingredients List
INGREDIENTS = [bag_coffee_beans, ground_coffee, espresso_shot, water, hot_water, ice, milk, steamed_milk, foamed_milk, cocoa_powder, hot_chocolate]
