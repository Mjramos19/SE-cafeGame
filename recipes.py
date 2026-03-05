import pygame
class Recipes:
    def __init__(self, all_recipes: dict, unlocked_recipes: list, price: float, image_key):
        """
        all_recipes: dict of recipe_name -> list of ingredients
        unlocked_recipes: list of recipe names currently available
        """
        self.all_recipes = all_recipes
        self.unlocked = unlocked_recipes
        self.price = price

        try:
            self.image = IMAGE_LIBRARY[image_key]
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color("white"))

    def match_ingredients_to_recipie(self, ingredients: list):
        """
        Returns the recipe name that matches the given ingredients.
        Order does not matter. Must match exactly.
        """
        if not ingredients:
            return None

        for recipe_name in self.unlocked:
            recipe_ingredients = self.all_recipes.get(recipe_name)

            if recipe_ingredients and sorted(ingredients) == sorted(recipe_ingredients):
                return recipe_name

        return None

    def get_ingredients(self, recipe_name: str):
        """Return ingredient list for a recipe, or None if not found."""
        return self.all_recipes.get(recipe_name)

    def is_unlocked(self, recipe_name):
        """Check whether a recipe is unlocked."""
        return recipe_name in self.unlocked

    def unlock(self, recipe_name):
        """Unlock a recipe if it exists."""
        if recipe_name in self.all_recipes and recipe_name not in self.unlocked:
            self.unlocked.append(recipe_name)

    def lock(self, recipe_name):
        """Lock a recipe."""
        if recipe_name in self.unlocked:
            self.unlocked.remove(recipe_name)

    def get_unlocked(self):
        """Return a copy of unlocked recipes."""
        return list(self.unlocked)
    def get_price(self):
        """Return the price of the recipe."""
        return self.price
