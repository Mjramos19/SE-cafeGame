import pygame
import pytest 
import backroom 

#images for backroom objects
backroom.IMAGE_LIBRARY = {
    "fireAhhShelf": pygame.Surface((500, 300)),
    "best_box_ever": pygame.Surface((100, 100)),
    "sick_rug": pygame.Surface((100, 100)),
}

#fake ingredient object class
class FakeIngred:
    def __init__(self, name):
        self.name = name

#fake player class for tests
class FakePlayer:
    def __init__(self):
        self.selectedSlot = 0
        #only one inventory slot for simple testing
        self.inventory = [[]]
        self.added_items = []
        self.removed_items = []
    
    #keeps track of added items and their type as a tuple
    def addInventoryItem(self, item, item_type):
        self.added_items.append((item, item_type))
    
    #Keeps track of removed items and their type as a tuple
    def popInventoryItem(self, item, item_type):
        self.removed_items.append((item, item_type))
        if item in self.inventory[self.selectedSlot]:
            self.inventory[self.selectedSlot].remove(item)

def test_shelfspot_behavior():
    spot = backroom.ShelfSpot(10, 20, 100, 50)

    #checking nitial state of shelf spots
    assert spot.open == True
    assert spot.held_ingredient_box == None

    #remove box behavior
    ingredient = FakeIngred("Coffee Beans")
    box = backroom.IngredientBox(0, 0, ingredient)

    spot.held_ingredient_box = box
    spot.open = False

    spot.remove_ingredient_box()

    assert spot.open == True
    assert spot.held_ingredient_box == None

def test_ingredientbox_behavior():
    ingredient = FakeIngred("Coffee Beans")
    box = backroom.IngredientBox(0, 0, ingredient)

    #testing initial state of ingredient boxes
    assert box.quantity == 10
    assert box.spot == None
    assert box.stackable == False
    assert box.name == "Coffee Beans Box"

    #update a boxes position
    box.update_position((200, 300))
    assert box.rect.center == (200, 300)

    #set a spot
    spot = backroom.ShelfSpot(10, 20, 100, 50)
    box.set_spot(spot)
    assert box.spot == spot

def test_pick_ingredient_set():
    milk = FakeIngred("Milk")
    beans = FakeIngred("Coffee Beans")
    sugar = FakeIngred("Sugar")

    assert backroom.IngredientBox.pick_ingredient([milk, beans, sugar]) == beans

    assert backroom.IngredientBox.pick_ingredient([milk, sugar]) == None

    assert backroom.IngredientBox.pick_ingredient([]) == None

    assert backroom.IngredientBox.pick_ingredient([FakeIngred("coffee beans")]) == None

def test_store_ingredient_box_set():
    player = FakePlayer()
    spot = backroom.ShelfSpot(10, 20, 100, 50)

    ingredient = FakeIngred("Coffee Beans")
    box = backroom.IngredientBox(0, 0, ingredient)

    player.inventory[0] = [box]
    spot.store_ingredient_box(player)

    assert spot.open == False
    assert spot.held_ingredient_box == box

    #reset
    spot.remove_ingredient_box()

    #set empty inventory
    player.inventory[0] = []
    spot.store_ingredient_box(player)

    assert spot.open is True
    assert spot.held_ingredient_box == None

    #wrong type item
    player.inventory[0] = [ingredient]
    spot.store_ingredient_box(player)

    assert spot.held_ingredient_box == None

    #attempt to store box in an already occupied spot
    existing_box = backroom.IngredientBox(0, 0, ingredient)
    new_box = backroom.IngredientBox(0, 0, FakeIngred("Milk"))

    spot.held_ingredient_box = existing_box
    spot.open = False
    player.inventory[0] = [new_box]

    spot.store_ingredient_box(player)

    assert spot.held_ingredient_box == existing_box

def test_grab_ingredient_set():
    player = FakePlayer()
    spot = backroom.ShelfSpot(10, 20, 100, 50)
    ingredient = FakeIngred("Coffee Beans")
    box = backroom.IngredientBox(0, 0, ingredient)

    box.set_spot(spot)
    spot.open = False
    spot.held_ingredient_box = box

    #grabbing single ingredients from non-edge case
    box.quantity = 5
    box.grab_ingredient(player)
    assert box.quantity == 4
    assert spot.open is False

    #test box dissapearing after final ingredient removed
    box.quantity = 1
    box.grab_ingredient(player)

    assert box.quantity == 0
    assert spot.open is True
    assert spot.held_ingredient_box is None

def test_stocking_shelf_creation():
    #proper creation of shelf and shelf spots
    shelf = backroom.StockingShelf(50, 50, 500, 300)
    assert len(shelf.spots) == 4 