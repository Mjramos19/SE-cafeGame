"""
Cafe Simulator Inventory and Environment Module.

This module defines the classes for managing the backroom storage system,
including shelving units, individual shelf spots, and ingredient containers.
"""

import pygame
from items import *

class StockingShelf(GameObject):
    """
    A large shelving unit that manages multiple individual storage spots.
    
    Attributes:
        interaction_zone (pygame.Rect): The area where a player must stand to interact.
        spots (list): A collection of shelf_spot objects contained within this shelf.
        icon (pygame.Surface): The visual sprite for the shelf unit.
    """
    def __init__(self, x, y, w, h):
        """
        Initializes the shelf and generates its internal grid of storage spots.
        """
        super().__init__(x, y, w, h, (255,0,0))
        self.interaction_zone = pygame.Rect(self.x, self.y + 300, self.w, self.h - 200)
        self.spots = [
            shelf_spot(self.rect.x + 60, self.rect.y + 55, 90, 100, "Shelf"),
            shelf_spot(self.rect.x + 340, self.rect. y + 55, 90, 100, "Shelf"),
            shelf_spot(self.rect.x + 60, self.rect.y + 170, 90, 100, "Shelf"),
            shelf_spot(self.rect.x + 340, self.rect.y + 170, 90, 100, "Shelf")
            ]
        self.icon = IMAGE_LIBRARY["fireAhhShelf"]
    
    #unfinished function
    def placeshelf_spot(self, num):
        """Updates given shelf spot"""
        for i in range(len(self.spots)):
            if i == num:
                pass
        
    def render(self, screen, font, DebugMode):
        """
        Draws the shelf icon and triggers the render method for all nested spots.
        """
        screen.blit(self.icon, self.rect)
        for spot in self.spots:
            spot.render(screen, font)

class shelf_spot(GameObject):
    """
    An individual slot on a shelf that can hold a single ingredient box.
    
    Attributes:
        open (bool): Whether the spot is currently empty.
        held_ingredient_box (ingredientBox): The box object currently stored in this spot.
    """
    def __init__(self, x, y, w, h, parent):
        """Initializes an empty shelf spot."""
        super().__init__(x, y, w, h, (0, 0, 0))
        self.open = True
        self.held_ingredient_box = None
        self.parent = parent
    
    def store_ingredient_box(self, player):
        """
        Transfers an ingredient box from the player's active inventory slot to this spot.
        
        Args:
            player (Player): The player object attempting to store an item.
        """
        slot = player.inventory[player.selected_slot]
        if len(slot) == 0 or (not (isinstance(slot[0], IngredientBox))):
                return
        
        item = slot[0]
        item.set_spot(self)

        if self.open:
                self.held_ingredient_box = item
                self.open = False
                #set boxes new position to shelf spot
                item.update_position(self.rect.center)
                #remove box interaction zone since its going on shelf
                item.interaction_zone = None
                #clear hotbar/inventory spot
                player.pop_inv_item(item, type(item))
                

    def remove_ingredient_box(self):
        """
        Resets box to open state
        """
        self.open = True
        self.held_ingredient_box = None

    def render(self, screen, font):
        """
        Renders its contained box if it is currently occupied.
        """
        if self.open == False:
            if self.parent == "Shelf":
                self.held_ingredient_box.render(screen, font)
            else:
                return


class IngredientBox(GameObject):
    """
    A container for raw ingredients with a limited quantity.
    
    Attributes:
        ingredient (Ingredient): The type of ingredient stored inside.
        quantity (int): Remaining units before the box is depleted.
        interaction_zone (pygame.Rect): Clickable area when the box is on the floor.
    """
    def __init__(self, x, y, ingredient):
        """
        Initializes the box with a specific ingredient and a default quantity of 10.
        """
        super().__init__(x, y, 100, 100, (150, 75, 0))
        self.ingredient = ingredient
        self.quantity = 10
        self.interaction_zone = pygame.Rect(self.x, self.y - 50, self.w, self.h - 50)
        self.name = f"{self.ingredient.name} Box"
        self.spot = None
        self.icon = IMAGE_LIBRARY["best_box_ever"]
        self.ingredient_icon = IMAGE_LIBRARY[f"{ingredient.name}_icon"]
        self.stackable = False

    def update_position(self, center):
        """Updates the physical coordinates of the box to align with a shelf spot's center."""
        self.rect.center = center
        self.x = self.rect.x
        self.y = self.rect.y

    def pop_box(box, ingredient_boxes, backroomCollisions):
        """
        Static helper to remove a box from the global game tracking lists.
        
        Args:
            box (ingredientBox): The box instance to remove.
            ingredient_boxes (list): The list of all boxes in the room.
            backroomCollisions (list): The list of active collision rects.
        """
        backRoomIndex = -1
        for i in range(len(ingredient_boxes)):
            if box == ingredient_boxes[i]:
                ingredient_boxes[i] = None
                break
        
        for i in range(len(backroomCollisions)):
            if box == backroomCollisions[i]:
                backRoomIndex = i
                break
        backroomCollisions.pop(backRoomIndex)
    
    def pick_ingredient(ingredients_list, slot_index=None):
        """
        Returns a guaranteed ingredient per slot so essential items always spawn.
        Slot assignments:
            0 -> Coffee Beans (index 0)
            1 -> Water        (index 3)
            2 -> Ice          (index 5)
            3 -> Milk         (index 6)
            4 -> Cocoa Powder (index 9)
        """
        slot_map = {0: 0, 1: 9, 2: 0, 3: 9}
        if slot_index is not None and slot_index in slot_map:
            return ingredients_list[slot_map[slot_index]]
        return ingredients_list[random.randint(0, len(ingredients_list) - 1)]
    
    def set_spot(self, spot):
        """
        Links this box to a specific shelf spot.
        """
        self.spot = spot

    def grab_ingredient(self, player):
        """
        Removes one unit from the box and adds it to the player's inventory.
        
        Args:
            player (Player): The player retrieving the ingredient.
        """
        player.add_item_to_inv(self.ingredient, type(self.ingredient))
        self.quantity -= 1
        if self.quantity == 0:
            self.spot.remove_ingredient_box()
        
    def place_ingredient_in_box(self, player):
        """
        Removes one unit from the players inventory and adds it a box.

        Args:
            player (Player): The player storing the ingredient
        """
        slot = player.inventory[player.selected_slot]

        if len(slot) == 0 or (not (isinstance(slot[0], Ingredient))) or self.quantity == 10:
            return
        
        player.inventory[player.selected_slot].pop(0)
        self.quantity += 1

    def render(self, screen, font, DebugMode = False):
        """
        Draws the box icon, ingredient icon, and interaction zone if applicable.
        """
        ingred_icon_rect = self.ingredient_icon.get_rect()
        ingred_icon_rect.center = self.rect.center
        screen.blit(self.icon, self.rect)
        screen.blit(self.ingredient_icon, ingred_icon_rect)
        if self.interaction_zone != None and DebugMode:
            pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)        

class DoorEntry(GameObject):
    """
    A floor rug representing a transition point between different cafe rooms.
    """
    def __init__(self, x, y, w, h):
        """Initializes the entry point with a rug graphic."""
        super().__init__(x, y, w, h, color=WHITE)
        self.icon = IMAGE_LIBRARY["sick_rug"]
        self.icon_rect = self.icon.get_rect(topleft=(x, y))
    
    def render(self, screen):
        """
        Renders the entry rug at its designated coordinates.
        """
        screen.blit(self.icon, self.rect)


class Refrigerator(StockingShelf):
    """
    A Refrigerator unit that manages two storage spots for cold ingredients
    
    Attributes:
        ...
    """
    def __init__(self, x, y, w, h):
        """
        Initializes the refrigerator object for back room storage
        """
        super(StockingShelf, self).__init__(x, y, w, h, (255, 0, 0))
        self.interaction_zone = pygame.Rect(self.x, self.y + 300, self.w, self.h - 200)
        self.spots = [
            shelf_spot(self.rect.x + 7, self.rect.y + 75, 100, 200, "Fridge"),
            shelf_spot(self.rect.x + 121, self.rect.y + 75, 100, 200, "Fridge")
        ]
        self.icon = IMAGE_LIBRARY["fridge"]

