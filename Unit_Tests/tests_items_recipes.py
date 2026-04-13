import unittest
from items import *
from recipes import *
from game import *

class TestItemsAndRecipes(unittest.TestCase):
    """Unit tests for the Ingredient and Cup classes in items.py."""

    def setUp(self):
        """Initialize objects before every test."""
        
        # Define Ingredients
        self.bag_coffee_beans = Ingredient("Coffee Beans", ["coffee_beans"], True, 18.35, 56)
        self.ground_coffee = Ingredient("Ground Coffee", ["ground_coffee"], True)
        self.espresso_shot = Ingredient("Espresso Shot", ["water"])
        self.espresso_doubleShot = Ingredient("Espresso Double Shot", ["water"])
        self.water = Ingredient("Water", ["water"], True)
        self.hot_water = Ingredient("Hot Water", ["water"])
        self.ice = Ingredient("Ice", ["water"])
        self.milk = Ingredient("Milk", ["water"], True, 3.28, 16)
        self.steamed_milk = Ingredient("Steamed Milk", ["water"])
        self.foamed_milk = Ingredient("Foamed Milk", ["water"])
        self.cocoa_powder = Ingredient("Cocoa Powder", ["water"], False, 9.40, 64)

        self.ingredients_list = [
            self.bag_coffee_beans, self.ground_coffee, self.espresso_shot, 
            self.water, self.hot_water, self.ice, self.milk, 
            self.steamed_milk, self.foamed_milk, self.cocoa_powder
        ]

        # Define Cups
        self.cup = Cup(["cup", "cup_w_lid"])
        self.cup1 = Cup(["cup", "cup_w_lid"], contents=[self.ice])
        self.cup2 = Cup(["cup", "cup_w_lid"], contents=[self.espresso_shot, self.milk])
        self.cup3 = Cup(["cup", "cup_w_lid"], contents=[self.espresso_doubleShot, self.steamed_milk])
        self.cup4 = Cup(["cup", "cup_w_lid"], contents=[self.hot_water, self.cocoa_powder])
        self.cup5 = Cup(["cup", "cup_w_lid"], contents=[self.hot_water, self.cocoa_powder, self.ice, self.milk, self.steamed_milk])

        self.cups_list = [self.cup, self.cup1, self.cup2, self.cup3, self.cup4, self.cup5]

        self.cup6 = Cup(["cup", "cup_w_lid"], contents=[self.espresso_shot])
        self.cup7 = Cup(["cup", "cup_w_lid"], contents=[self.hot_water, self.espresso_shot])
        
        self.cups_for_recipes = [self.cup, self.cup1, self.cup2, self.cup3, self.cup4, self.cup5, self.cup6, self.cup7]

        # Defines all Recipes
        self.Espresso = Recipe("Espresso Shot" ,[self.espresso_shot],6.50, "N/A", False)
        self.Iced_Coffee = Recipe("Iced Coffee" ,[self.espresso_shot, self.ice],6.50, "N/A")
        self.Americano = Recipe("Americano" ,[self.hot_water, self.espresso_shot],7.50, "N/A", False)
        self.Latte = Recipe("Latte" ,[self.espresso_shot, self.steamed_milk],6.50, "N/A")
        self.Iced_Latte = Recipe("Iced Latte" ,[self.espresso_shot, self.ice, self.milk],6.50, "N/A")
        self.Hot_Chocolate = Recipe("Hot Chocolate" ,[self.hot_water, self.cocoa_powder, self.steamed_milk],6.50, "N/A")

        self.recipes = [self.Espresso, self.Iced_Coffee, self.Americano, self.Latte, self.Iced_Latte, self.Hot_Chocolate]

    def test_ingredients(self):
        """Tests the initialization and properties of an Ingredient object."""
        for ingredient in self.ingredients_list:
            with self.subTest(ingredient=ingredient.name):
                self.assertIsInstance(ingredient.image_keys, list)
                self.assertGreater(len(ingredient.image_keys), 0)
                self.assertIsInstance(ingredient.image, pygame.Surface)
                self.assertIsInstance(ingredient.x, int)
                self.assertIsInstance(ingredient.y, int)
                self.assertIsInstance(ingredient.w, int)
                self.assertIsInstance(ingredient.h, int)
                self.assertIsInstance(ingredient.name, str)
                self.assertIsInstance(ingredient.price, float)
                self.assertIsInstance(ingredient.an_input, bool)
                self.assertIsInstance(ingredient.quantity, int)
                self.assertIsInstance(ingredient.stackable, bool)
                self.assertTrue(ingredient.stackable)

    def test_bag_coffee_beans(self):
        """Tests that the specific properties of the bag of coffee beans ingredient return correctly."""
        self.assertEqual(self.bag_coffee_beans.name, "Coffee Beans")
        self.assertEqual(self.bag_coffee_beans.price, 18.35)
        self.assertTrue(self.bag_coffee_beans.an_input)
        self.assertEqual(self.bag_coffee_beans.quantity, 56)

    def test_ground_coffee(self):
        """Tests that the specific properties of the ground coffee ingredient return correctly."""
        self.assertEqual(self.ground_coffee.name, "Ground Coffee")
        self.assertEqual(self.ground_coffee.price, 0.0)
        self.assertTrue(self.ground_coffee.an_input)
        self.assertEqual(self.ground_coffee.quantity, 0)

    def test_espresso_shot(self):
        """Tests that the specific properties of the espresso shot ingredient return correctly."""
        self.assertEqual(self.espresso_shot.name, "Espresso Shot")
        self.assertEqual(self.espresso_shot.price, 0.0)
        self.assertFalse(self.espresso_shot.an_input)
        self.assertEqual(self.espresso_shot.quantity, 0)

    def test_espresso_doubleShot(self):
        """Tests that the specific properties of the espresso double shot ingredient return correctly."""
        self.assertEqual(self.espresso_doubleShot.name, "Espresso Double Shot")
        self.assertEqual(self.espresso_doubleShot.price, 0.0)
        self.assertFalse(self.espresso_doubleShot.an_input)
        self.assertEqual(self.espresso_doubleShot.quantity, 0)

    def test_water(self):
        """Tests that the specific properties of the water ingredient return correctly."""
        self.assertEqual(self.water.name, "Water")
        self.assertEqual(self.water.price, 0.0)
        self.assertTrue(self.water.an_input)
        self.assertEqual(self.water.quantity, 0)

    def test_hot_water(self):
        """Tests that the specific properties of the hot water ingredient return correctly."""
        self.assertEqual(self.hot_water.name, "Hot Water")
        self.assertEqual(self.hot_water.price, 0.0)
        self.assertFalse(self.hot_water.an_input)
        self.assertEqual(self.hot_water.quantity, 0) 

    def test_ice(self):
        """Tests that the specific properties of the ice ingredient return correctly."""
        self.assertEqual(self.ice.name, "Ice")
        self.assertEqual(self.ice.price, 0.0)
        self.assertFalse(self.ice.an_input)
        self.assertEqual(self.ice.quantity, 0)   

    def test_milk(self):
        """Tests that the specific properties of the milk ingredient return correctly."""
        self.assertEqual(self.milk.name, "Milk")
        self.assertEqual(self.milk.price, 3.28)
        self.assertTrue(self.milk.an_input)
        self.assertEqual(self.milk.quantity, 16)         

    def test_steamed_milk(self):
        """Tests that the specific properties of the steamed milk ingredient return correctly."""
        self.assertEqual(self.steamed_milk.name, "Steamed Milk")
        self.assertEqual(self.steamed_milk.price, 0.0)
        self.assertFalse(self.steamed_milk.an_input)
        self.assertEqual(self.steamed_milk.quantity, 0)

    def test_foamed_milk(self):
        """Tests that the specific properties of the foamed milk ingredient return correctly."""
        self.assertEqual(self.foamed_milk.name, "Foamed Milk")
        self.assertEqual(self.foamed_milk.price, 0.0)
        self.assertFalse(self.foamed_milk.an_input)
        self.assertEqual(self.foamed_milk.quantity, 0)

    def test_cocoa_powder(self):
        """Tests that the specific properties of the cocoa powder ingredient return correctly."""
        self.assertEqual(self.cocoa_powder.name, "Cocoa Powder")
        self.assertEqual(self.cocoa_powder.price, 9.40)
        self.assertFalse(self.cocoa_powder.an_input)
        self.assertEqual(self.cocoa_powder.quantity, 64)
    
    def test_cup(self):
        """Tests the initialization and properties of a Cup object."""
        for cup in self.cups_list:
            with self.subTest(cup=cup.name):
                self.assertIsInstance(cup.image_keys, list)
                self.assertGreater(len(cup.image_keys), 0, "Cup should have at least one image key.")
                self.assertIsInstance(cup.image, pygame.Surface)
                self.assertIsInstance(cup.x, int)
                self.assertIsInstance(cup.y, int)
                self.assertIsInstance(cup.name, str)
                self.assertIsInstance(cup.contents, list or type(None))
                self.assertIsInstance(cup.stackable, bool)
                self.assertEqual(cup.name, "Cup")

    def test_cup_update(self):
        """Tests that the update method correctly changes the stackable status and image based on contents."""
        for cup in self.cups_list:
            cup.update()
            if cup.contents:
                self.assertFalse(cup.stackable, "Cup with contents should not be stackable.")
                self.assertEqual(cup.image, IMAGE_LIBRARY[cup.image_keys[1]], "Cup with contents should use the filled image.")
            else:
                self.assertTrue(cup.stackable, "Empty cup should be stackable.")
                self.assertEqual(cup.image, IMAGE_LIBRARY[cup.image_keys[0]], "Empty cup should use the empty image.")

    def test_Cup(self):
        """Tests the initialization of a Cup object with no contents."""
        self.assertEqual(self.cup.name, "Cup")
        self.assertEqual(self.cup.contents, [])
        self.assertTrue(self.cup.stackable)

    def test_Cup1(self):
        """Tests the initialization of a Cup object with ice as contents."""
        self.assertEqual(self.cup1.name, "Cup")
        self.assertEqual(self.cup1.contents, [self.ice])
        self.assertFalse(self.cup1.stackable)

    def test_Cup2(self):
        """Tests the initialization of a Cup object with espresso shot and milk as contents."""
        self.assertEqual(self.cup2.name, "Cup")
        self.assertEqual(self.cup2.contents, [self.espresso_shot, self.milk])
        self.assertFalse(self.cup2.stackable)

    def test_Cup3(self):
        """Tests the initialization of a Cup object with espresso double shot and steamed milk as contents."""
        self.assertEqual(self.cup3.name, "Cup")
        self.assertEqual(self.cup3.contents, [self.espresso_doubleShot, self.steamed_milk])
        self.assertFalse(self.cup3.stackable)

    def test_Cup4(self):
        """Tests the initialization of a Cup object with hot water and cocoa powder as contents."""
        self.assertEqual(self.cup4.name, "Cup")
        self.assertEqual(self.cup4.contents, [self.hot_water, self.cocoa_powder])
        self.assertFalse(self.cup4.stackable)

    def test_Cup5(self):
        """Tests the initialization of a Cup object with hot water, cocoa powder, ice, milk, and steamed milk as contents."""
        self.assertEqual(self.cup5.name, "Cup")
        self.assertEqual(self.cup5.contents, [self.hot_water, self.cocoa_powder, self.ice, self.milk, self.steamed_milk])
        self.assertFalse(self.cup5.stackable)

    def test_recipe(self):
        """Tests the initialization and properties of a Recipe object."""
        for recipe in self.recipes:
            with self.subTest(recipe=recipe.name):
                self.assertIsInstance(recipe.name, str)
                self.assertIsInstance(recipe.ingredients, list)
                self.assertGreater(len(recipe.ingredients), 0, "Recipe should have at least one ingredient.")
                self.assertIsInstance(recipe.price, float)
                self.assertIsInstance(recipe.locked, bool)

    def test_recipe_values(self):
        """Tests that the specific properties of the recipes return correctly."""
        for recipe in self.recipes:
            with self.subTest(recipe=recipe.name):
                self.assertEqual(recipe.name, recipe.get_name())
                self.assertEqual(recipe.ingredients, recipe.get_ingredients())
                self.assertEqual(recipe.price, recipe.get_price())
                self.assertEqual(recipe.locked, recipe.get_status())

    def test_recipe_status(self):
        """Tests the set_status and get_status methods of the Recipe class."""
        for recipe in self.recipes:
            with self.subTest(recipe=recipe.name):
                recipe.set_status(True)
                self.assertTrue(recipe.get_status(), "Recipe status should be True after setting to True.")
                recipe.set_status(False)
                self.assertFalse(recipe.get_status(), "Recipe status should be False after setting to False.")

    def test_if_recipe(self):
        """Tests the check_match method of the Recipe class with different cups/contents."""
        for recipe in self.recipes:
            with self.subTest(recipe=recipe.name):
                for cup in self.cups_for_recipes:
                    if recipe.check_match(cup):
                        self.assertTrue(recipe.check_match(cup))
                    else:
                        self.assertFalse(recipe.check_match(cup))
                
        self.assertTrue(self.Espresso.check_match(self.cup6))
        self.assertTrue(self.Americano.check_match(self.cup7))
        self.assertFalse(self.Latte.check_match(self.cup6))
        self.assertFalse(self.Iced_Latte.check_match(self.cup7))
        self.assertFalse(self.Hot_Chocolate.check_match(self.cup5))


if __name__ == '__main__':
    unittest.main()

# Testing adding to cup with be done manually in game since it requires interaction with machines and player inventory.
# Rendering will be tested manually as well.
    
