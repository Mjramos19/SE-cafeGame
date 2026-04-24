"""
Unit Tests: Backroom objects/system

Runs against the REAL backroom classes with a mock player for simplified actions.

Requirements covered:
  Req24 - Initialize stocking shelf upon game start
  Req25 - Store ingredient box from player's selected slot
  Req26 - Don't store an ingredient box when selected slot is empty
  Req27 - Update box position upon storing box
  Req28 - Decrease box ingredient quantity upon grabbing ingredient
  Req29 - Remove ingredient box from spot when quantity reaches 0
  Req30 - Don't allow player to store ingredient in box when box is full
  Req31 - Create each shelf spot in an open state upon initialization
  Req32 - Initialize refrigerator upon game start
  Req33 - Initialize door entry mat upon game start
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

import pygame
import backroom
from items import Ingredient


class DummyPlayer:
    """Simple player object for testing backroom methods."""

    def __init__(self, inventory, selected_slot=0):
        self.inventory = inventory
        self.selected_slot = selected_slot
        self.items_added = []
        self.items_removed = []

    def add_item_to_inv(self, item, item_type):
        """Simulates adding an item to inventory."""
        self.items_added.append((item, item_type))

    def pop_inv_item(self, item, item_type):
        """
        Simulates removing an item from inventory.

        store_ingredient_box() calls pop_inv_item(item, type(item)) after
        already popping the item from the slot internally — so here we just
        record the call without touching the slot again.
        """
        self.items_removed.append((item, item_type))


class TestBackroom(unittest.TestCase):
    """Unit tests for backroom.py classes"""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once before all tests."""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests."""
        pygame.quit()

    def setUp(self):
        """Set up test objects before each test."""
        # Inject fake surfaces so backroom classes don't need real asset files
        backroom.IMAGE_LIBRARY["fireAhhShelf"]   = pygame.Surface((200, 200))
        backroom.IMAGE_LIBRARY["best_box_ever"]  = pygame.Surface((100, 100))
        backroom.IMAGE_LIBRARY["sick_rug"]       = pygame.Surface((80, 80))
        backroom.IMAGE_LIBRARY["fridge"]         = pygame.Surface((120, 200))
        backroom.IMAGE_LIBRARY["Coffee Beans_icon"] = pygame.Surface((20, 20))
        backroom.IMAGE_LIBRARY["Milk_icon"]      = pygame.Surface((20, 20))
        backroom.IMAGE_LIBRARY["coffee_beans"]   = pygame.Surface((20, 20))
        backroom.IMAGE_LIBRARY["milk"]           = pygame.Surface((20, 20))

        self.screen      = pygame.Surface((800, 600))
        self.font        = pygame.font.SysFont(None, 24)
        self.coffee_beans = Ingredient("Coffee Beans", ["coffee_beans"], True, 18.35, 56)
        self.milk         = Ingredient("Milk",          ["milk"],         True,  3.28, 16)


    # Req24 — StockingShelf initializes correctly
    def test_stocking_shelf(self):
        """Req24 - Tests StockingShelf initialization."""
        shelf = backroom.StockingShelf(100, 200, 500, 400)

        self.assertEqual(shelf.x, 100)
        self.assertEqual(shelf.y, 200)
        self.assertEqual(shelf.w, 500)
        self.assertEqual(shelf.h, 400)
        self.assertEqual(len(shelf.spots), 4)
        self.assertIsInstance(shelf.interaction_zone, pygame.Rect)
        self.assertEqual(shelf.icon, backroom.IMAGE_LIBRARY["fireAhhShelf"])

    # Req31 — Each shelf spot starts open
    def test_shelf_spot(self):
        """Req31 - Tests shelf_spot initialization."""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)
        self.assertEqual(spot.parent, "Shelf")

    # IngredientBox baseline
    def test_ingredient_box(self):
        """Tests IngredientBox initialization."""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)

        self.assertEqual(box.x, 25)
        self.assertEqual(box.y, 35)
        self.assertEqual(box.w, 100)
        self.assertEqual(box.h, 100)
        self.assertEqual(box.ingredient, self.coffee_beans)
        self.assertEqual(box.quantity, 10)
        self.assertEqual(box.name, "Coffee Beans Box")
        self.assertFalse(box.stackable)
        self.assertIsNotNone(box.interaction_zone)

    # Req27 — Box position updates correctly
    def test_update_position(self):
        """Req27 - Tests IngredientBox position update."""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        box.update_position((200, 300))

        self.assertEqual(box.rect.center, (200, 300))
        self.assertEqual(box.x, box.rect.x)
        self.assertEqual(box.y, box.rect.y)

    def test_set_spot(self):
        """Tests setting an IngredientBox shelf spot."""
        box  = backroom.IngredientBox(25, 35, self.coffee_beans)
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        box.set_spot(spot)

        self.assertEqual(box.spot, spot)

    # Req25 — Store ingredient box from player's selected slot
    def test_store_ingredient_box(self):
        """Req25 - Tests storing an ingredient box onto a shelf spot."""
        spot   = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        box    = backroom.IngredientBox(0, 0, self.coffee_beans)
        player = DummyPlayer([[box]], 0)

        spot.store_ingredient_box(player)

        self.assertFalse(spot.open)
        self.assertEqual(spot.held_ingredient_box, box)
        self.assertEqual(box.spot, spot)
        self.assertIsNone(box.interaction_zone)
        # pop_inv_item is called with (box, type(box)) after placement
        self.assertEqual(player.items_removed[0][0], box)

    # Req26 — Nothing happens if selected slot is empty
    def test_store_ingredient_box_empty_slot(self):
        """Req26 - Tests that nothing happens if selected inventory slot is empty."""
        spot   = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        player = DummyPlayer([[]], 0)

        spot.store_ingredient_box(player)

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    def test_remove_ingredient_box(self):
        """Tests removing a box from a shelf spot."""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        box  = backroom.IngredientBox(0, 0, self.coffee_beans)

        spot.held_ingredient_box = box
        spot.open = False

        spot.remove_ingredient_box()

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    # Req28 — Grabbing an ingredient decreases box quantity
    def test_grab_ingredient(self):
        """Req28 - Tests grabbing one ingredient from a box."""
        box    = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[]], 0)
        spot   = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        # Put the box on the spot so quantity > 1 doesn't clear it
        box.spot      = spot
        spot.held_ingredient_box = box
        spot.open     = False
        box.quantity  = 5

        box.grab_ingredient(player)

        self.assertEqual(box.quantity, 4)
        self.assertEqual(player.items_added[0][0], self.coffee_beans)
        # Spot still occupied because quantity > 0
        self.assertFalse(spot.open)

    # Req29 — Last ingredient removes box from spot
    def test_grab_last_ingredient(self):
        """Req29 - Tests grabbing the last ingredient empties the shelf spot."""
        box    = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[]], 0)
        spot   = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        box.spot                 = spot
        spot.held_ingredient_box = box
        spot.open                = False
        box.quantity             = 1

        box.grab_ingredient(player)

        self.assertEqual(box.quantity, 0)
        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    # place_ingredient_in_box
    def test_place_ingredient_in_box(self):
        """Tests placing one ingredient from inventory into a box."""
        box    = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[self.coffee_beans]], 0)

        box.quantity = 7
        box.place_ingredient_in_box(player)

        self.assertEqual(box.quantity, 8)
        # place_ingredient_in_box does a direct slot.pop(0) — the slot shrinks
        self.assertEqual(len(player.inventory[0]), 0)

    # Req30 — Box full: no ingredient added
    def test_place_ingredient_in_box_full(self):
        """Req30 - Tests that no ingredient is added if the box is already full."""
        box    = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[self.coffee_beans]], 0)

        box.quantity = 10
        box.place_ingredient_in_box(player)

        self.assertEqual(box.quantity, 10)
        # Slot untouched because box was full
        self.assertEqual(len(player.inventory[0]), 1)

    # Req33 — DoorEntry initializes correctly
    def test_door_entry(self):
        """Req33 - Tests DoorEntry initialization."""
        door = backroom.DoorEntry(300, 400, 100, 50)

        self.assertEqual(door.x, 300)
        self.assertEqual(door.y, 400)
        self.assertEqual(door.w, 100)
        self.assertEqual(door.h, 50)
        self.assertEqual(door.icon, backroom.IMAGE_LIBRARY["sick_rug"])


    # Req32 — Refrigerator initializes correctly
    def test_refrigerator(self):
        """Req32 - Tests Refrigerator initialization."""
        fridge = backroom.Refrigerator(200, 100, 250, 500)

        self.assertEqual(fridge.x, 200)
        self.assertEqual(fridge.y, 100)
        self.assertEqual(fridge.w, 250)
        self.assertEqual(fridge.h, 500)
        self.assertEqual(len(fridge.spots), 2)
        self.assertEqual(fridge.spots[0].parent, "Fridge")
        self.assertEqual(fridge.spots[1].parent, "Fridge")
        self.assertEqual(fridge.icon, backroom.IMAGE_LIBRARY["fridge"])


if __name__ == "__main__":
    unittest.main()