import unittest
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
        """Simulates removing an item from inventory."""
        self.items_removed.append((item, item_type))
        slot = self.inventory[self.selected_slot]
        if item in slot:
            slot.remove(item)


class TestBackroom(unittest.TestCase):
    """Unit tests for backroom.py classes"""

    @classmethod
    def setUpClass(cls):
        """Initialize pygame once before all tests"""
        pygame.init()

    @classmethod
    def tearDownClass(cls):
        """Quit pygame after all tests"""
        pygame.quit()

    def setUp(self):
        """Set up test objects before each test"""

        #fake images
        backroom.IMAGE_LIBRARY["fireAhhShelf"] = pygame.Surface((200, 200))
        backroom.IMAGE_LIBRARY["best_box_ever"] = pygame.Surface((100, 100))
        backroom.IMAGE_LIBRARY["sick_rug"] = pygame.Surface((80, 80))
        backroom.IMAGE_LIBRARY["fridge"] = pygame.Surface((120, 200))
        backroom.IMAGE_LIBRARY["Coffee Beans_icon"] = pygame.Surface((20, 20))
        backroom.IMAGE_LIBRARY["Milk_icon"] = pygame.Surface((20, 20))

        self.screen = pygame.Surface((800, 600))
        self.font = pygame.font.SysFont(None, 24)

        self.coffee_beans = Ingredient("Coffee Beans", ["coffee_beans"], True, 18.35, 56)
        self.milk = Ingredient("Milk", ["milk"], True, 3.28, 16)

    def test_stocking_shelf(self):
        """Tests StockingShelf initialization"""
        shelf = backroom.StockingShelf(100, 200, 500, 400)

        self.assertEqual(shelf.x, 100)
        self.assertEqual(shelf.y, 200)
        self.assertEqual(shelf.w, 500)
        self.assertEqual(shelf.h, 400)
        self.assertEqual(len(shelf.spots), 4)
        self.assertIsInstance(shelf.interaction_zone, pygame.Rect)
        self.assertEqual(shelf.icon, backroom.IMAGE_LIBRARY["fireAhhShelf"])

    def test_shelf_spot(self):
        """Tests shelf_spot initialization"""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)
        self.assertEqual(spot.parent, "Shelf")

    def test_ingredient_box(self):
        """Tests IngredientBox initialization"""
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

    def test_update_position(self):
        """Tests IngredientBox position update"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        box.update_position((200, 300))

        self.assertEqual(box.rect.center, (200, 300))
        self.assertEqual(box.x, box.rect.x)
        self.assertEqual(box.y, box.rect.y)

    def test_set_spot(self):
        """Tests setting an IngredientBox shelf spot"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        box.set_spot(spot)

        self.assertEqual(box.spot, spot)

    def test_store_ingredient_box(self):
        """Tests storing an ingredient box onto a shelf spot"""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        box = backroom.IngredientBox(0, 0, self.coffee_beans)
        player = DummyPlayer([[box]], 0)

        spot.store_ingredient_box(player)

        self.assertFalse(spot.open)
        self.assertEqual(spot.held_ingredient_box, box)
        self.assertEqual(box.spot, spot)
        self.assertIsNone(box.interaction_zone)
        self.assertEqual(player.items_removed[0][0], box)

    def test_store_ingredient_box_empty_slot(self):
        """Tests that nothing happens if selected inventory slot is empty"""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        player = DummyPlayer([[]], 0)

        spot.store_ingredient_box(player)

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    def test_remove_ingredient_box(self):
        """Tests removing a box from a shelf spot"""
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")
        box = backroom.IngredientBox(0, 0, self.coffee_beans)

        spot.held_ingredient_box = box
        spot.open = False

        spot.remove_ingredient_box()

        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    def test_grab_ingredient(self):
        """Tests grabbing one ingredient from a box"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[]], 0)
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        box.spot = spot
        box.quantity = 5
        box.grab_ingredient(player)

        self.assertEqual(box.quantity, 4)
        self.assertEqual(player.items_added[0][0], self.coffee_beans)
        self.assertFalse(spot.open)  # spot should still stay occupied

    def test_grab_last_ingredient(self):
        """Tests grabbing the last ingredient from a box empties the shelf spot"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[]], 0)
        spot = backroom.shelf_spot(50, 60, 90, 100, "Shelf")

        box.spot = spot
        spot.held_ingredient_box = box
        spot.open = False
        box.quantity = 1

        box.grab_ingredient(player)

        self.assertEqual(box.quantity, 0)
        self.assertTrue(spot.open)
        self.assertIsNone(spot.held_ingredient_box)

    def test_place_ingredient_in_box(self):
        """Tests placing one ingredient from inventory into a box"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[self.coffee_beans]], 0)

        box.quantity = 7
        box.place_ingredient_in_box(player)

        self.assertEqual(box.quantity, 8)
        self.assertEqual(player.items_removed[0][0], self.coffee_beans)

    def test_place_ingredient_in_box_full(self):
        """Tests that no ingredient is added if the box is already full"""
        box = backroom.IngredientBox(25, 35, self.coffee_beans)
        player = DummyPlayer([[self.coffee_beans]], 0)

        box.quantity = 10
        box.place_ingredient_in_box(player)

        self.assertEqual(box.quantity, 10)
        self.assertEqual(len(player.items_removed), 0)

    def test_door_entry(self):
        """Tests DoorEntry initialization"""
        door = backroom.DoorEntry(300, 400, 100, 50)

        self.assertEqual(door.x, 300)
        self.assertEqual(door.y, 400)
        self.assertEqual(door.w, 100)
        self.assertEqual(door.h, 50)
        self.assertEqual(door.icon, backroom.IMAGE_LIBRARY["sick_rug"])

    def test_refrigerator(self):
        """Tests Refrigerator initialization"""
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