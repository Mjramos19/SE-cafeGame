from classes import *
import pygame

class stockingShelf(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, (255,0,0))
        self.interactionZone = pygame.Rect(self.x - 150, self.y, self.w - 50, self.h)
        #Makes its own shelf spot objects
        self.spots = [
            shelfSpot(self.rect.x + 30, self.rect.y + 150, 20, 20),
            shelfSpot(self.rect.x + 120, self.rect. y + 150, 20, 20),
            shelfSpot(self.rect.x + 30, self.rect.y + 350, 20, 20),
            shelfSpot(self.rect.x + 120, self.rect.y + 350, 20, 20)
            ]
        
    
    #the shelf renders itself as well as its shelf spots
    def render(self, screen):
        super().render(screen)
        #loop through shelf spot list attribute and render each one
        for spot in self.spots:
            spot.render(screen)
            


class shelfSpot(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h, (0, 0, 0))
        self.open = True
        self.held_ingredient_box = None
    
    #Function for placing a box from hotbar to selected shelf spot
    def storeIngredientBox(self, hotBarItem, player):
        #if selected item is not an ingredient box, do nothing. Else, if spot is empty store box in spot
        if not (isinstance(hotBarItem, ingredientBox)):
                return
        else:
            if self.open == True:
                self.held_ingredient_box = hotBarItem
                self.open = False
                #set boxes new position to shelf spot
                hotBarItem.updatePosition(self.rect.center)
                #remove box interaction zone since its going on shelf
                hotBarItem.interactionZone = None
                #clear hotbar/inventory spot
                player.inventory[player.selectedSlot] = None
    
    def grabIngredient(self):
        pass

    def render(self, screen):
        super().render(screen)
        if self.open == False:
            self.held_ingredient_box.render(screen)


class ingredientBox(GameObject):
    def __init__(self, x, y, ingredient):
        super().__init__(x, y, 100, 100, (150, 75, 0))
        self.ingredient = ingredient
        self.isEmpty = False
        self.interactionZone = pygame.Rect(self.x, self.y + 100, self.w, self.h - 50)

        #not sure yet
        self.ingredientQuantity = ...
    
    #helper function for placing boxes on shelves.
    #Updates the box objects coordinates from previous floor spot to shelf spot when placed
    def updatePosition(self, center):
        self.rect.center = center
        self.x = self.rect.x
        self.y = self.rect.y

    #Helper Function for removing picked up boxes
    def popBox(box, ingredientBoxes, backroomCollisions):
        backRoomIndex = -1
        #loops through the list of ingredientBoxes and removed the selected one
        for i in range(len(ingredientBoxes)):
            if box == ingredientBoxes[i]:
                ingredientBoxes[i] = None
                break
        
        #loops through the list of backroomCollisions and removed selected box from there too
        for i in range(len(backroomCollisions)):
            if box == backroomCollisions[i]:
                backRoomIndex = i
                break
        backroomCollisions.pop(backRoomIndex)


    #renders ingredient boxes as well as their interaction zone if they have (if they are on the floor)
    def render(self, screen):
        super().render(screen)
        font = pygame.font.SysFont(None, 22)
        ingredientType = font.render(f"{self.ingredient}", True, (250, 0, 0))
        screen.blit(ingredientType, (self.rect.x, self.rect.center[1]))
        if self.interactionZone != None:
            pygame.draw.rect(screen, (255, 255, 0), self.interactionZone, 2)

class DoorEntry(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)
        