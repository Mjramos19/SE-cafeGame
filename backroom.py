"""
Cafe Simulator Inventory and Environment Module.

This module defines the classes for managing the backroom storage system,
including shelving units, individual shelf spots, and ingredient containers.
"""

from classes import *
import pygame

class stockingShelf(GameObject):
    """
    A large shelving unit that manages multiple individual storage spots.
    
    Attributes:
        interactionZone (pygame.Rect): The area where a player must stand to interact.
        spots (list): A collection of shelfSpot objects contained within this shelf.
        icon (pygame.Surface): The visual sprite for the shelf unit.
    """
    def __init__(self, x, y, w, h):
        """Initializes the shelf and generates its internal grid of storage spots."""
        super().__init__(x, y, w, h, (255,0,0))
        self.interactionZone = pygame.Rect(self.x, self.y + 300, self.w, self.h - 200)
        self.spots = [
            shelfSpot(self.rect.x + 60, self.rect.y + 75, 100, 50),
            shelfSpot(self.rect.x + 340, self.rect. y + 75, 100, 50),
            shelfSpot(self.rect.x + 60, self.rect.y + 185, 100, 50),
            shelfSpot(self.rect.x + 340, self.rect.y + 185, 100, 50)
            ]
        self.icon = IMAGE_LIBRARY["fireAhhShelf"]
        
    def render(self, screen, font):
        """Draws the shelf icon and triggers the render method for all nested spots."""
        screen.blit(self.icon, self.rect)
        for spot in self.spots:
            spot.render(screen, font)

class shelfSpot(GameObject):
    """
    An individual slot on a shelf that can hold a single ingredient box.
    
    Attributes:
        open (bool): Whether the spot is currently empty.
        held_ingredient_box (ingredientBox): The box object currently stored in this spot.
    """
    def __init__(self, x, y, w, h):
        """Initializes an empty shelf spot."""
        super().__init__(x, y, w, h, (0, 0, 0))
        self.open = True
        self.held_ingredient_box = None
    
    def storeIngredientBox(self, player):
        """
        Transfers an ingredient box from the player's active inventory slot to this spot.
        
        Args:
            player (Player): The player object attempting to store an item.
        """
        slot = player.inventory[player.selectedSlot]
        if len(slot) == 0 or (not (isinstance(slot[0], ingredientBox))):
                return
        
        item = slot[0]
        item.setSpot(self)

        if self.open:
                self.held_ingredient_box = item
                self.open = False
                item.updatePosition(self.rect.center)
                item.interactionZone = None
                player.popInventoryItem(item, type(item))
                
    def removeIngredientBox(self):
        """Clears the spot, allowing a new box to be placed."""
        self.open = True
        self.held_ingredient_box = None

    def render(self, screen, font):
        """Renders the spot and its contained box if it is currently occupied."""
        super().render(screen)
        if self.open == False:
            self.held_ingredient_box.render(screen, font)

class ingredientBox(GameObject):
    """
    A container for raw ingredients with a limited quantity.
    
    Attributes:
        ingredient (Ingredient): The type of ingredient stored inside.
        quantity (int): Remaining units before the box is depleted.
        interactionZone (pygame.Rect): Clickable area when the box is on the floor.
    """
    def __init__(self, x, y, ingredient):
        """Initializes the box with a specific ingredient and a default quantity of 10."""
        super().__init__(x, y, 100, 100, (150, 75, 0))
        self.ingredient = ingredient
        self.quantity = 10
        self.interactionZone = pygame.Rect(self.x, self.y + 100, self.w, self.h - 50)
        self.name = f"{self.ingredient.name} Box"
        self.spot = None
        self.icon = IMAGE_LIBRARY["best_box_ever"]
        self.stackable = False

    def updatePosition(self, center):
        """Updates the physical coordinates of the box to align with a shelf spot's center."""
        self.rect.center = center
        self.x = self.rect.x
        self.y = self.rect.y

    def popBox(box, ingredientBoxes, backroomCollisions):
        """
        Static helper to remove a box from the global game tracking lists.
        
        Args:
            box (ingredientBox): The box instance to remove.
            ingredientBoxes (list): The list of all boxes in the room.
            backroomCollisions (list): The list of active collision rects.
        """
        backRoomIndex = -1
        for i in range(len(ingredientBoxes)):
            if box == ingredientBoxes[i]:
                ingredientBoxes[i] = None
                break
        
        for i in range(len(backroomCollisions)):
            if box == backroomCollisions[i]:
                backRoomIndex = i
                break
        backroomCollisions.pop(backRoomIndex)
    
    def pickIngredient(ingredientsList):
        """Returns the 'Coffee Beans' ingredient from a list (currently hardcoded logic)."""
        for i in ingredientsList:
            if i.name == "Coffee Beans":
                return i
    
    def setSpot(self, spot):
        """Links this box to a specific shelf spot."""
        self.spot = spot

    def grabIngredient(self, player):
        """
        Removes one unit from the box and adds it to the player's inventory.
        
        Args:
            player (Player): The player retrieving the ingredient.
        """
        player.addInventoryItem(self.ingredient, type(self.ingredient))
        self.quantity -= 1
        if self.quantity == 0:
            self.spot.removeIngredientBox()

    def render(self, screen, font):
        """Draws the box icon, ingredient name, and interaction zone if applicable."""
        ingredName = font.render(f'{self.ingredient.name}', True, (255, 255, 255))
        screen.blit(self.icon, self.rect)
        screen.blit(ingredName, (self.rect.center[0] - 20, self.rect.center[1] - 5))
        if self.interactionZone != None:
            pygame.draw.rect(screen, (255, 255, 0), self.interactionZone, 2)        

class DoorEntry(GameObject):
    """A floor rug representing a transition point between different cafe rooms."""
    def __init__(self, x, y, w, h):
        """Initializes the entry point with a rug graphic."""
        super().__init__(x, y, w, h, color=WHITE)
        self.icon = IMAGE_LIBRARY["sick_rug"]
        self.icon_rect = self.icon.get_rect(topleft=(x, y))
    
    def render(self, screen):
        """Renders the entry rug at its designated coordinates."""
        screen.blit(self.icon, self.rect)