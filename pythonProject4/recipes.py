from constants import *

class Recipe:
    """The Recipe class defines a recipe a customer can order and a player can make."""
    def __init__(self, name: str, ingredients: list, price: float, image_key, locked=True):
        """A recipe includes a name, a list of ingredients, a price, and a sprite."""
        if isinstance(name, str):
            self.name = name
        self.ingredients = ingredients
        if isinstance(price, float):
            self.price = price

        try:
            self.image = IMAGE_LIBRARY[image_key]
        except:
            self.image = pygame.Surface((50, 50))
            self.image.fill(pygame.Color("white"))

        self.locked = locked


    def get_name(self):
        """Returns name of recipe."""
        return self.name

    def get_ingredients(self):
        """Returns the ingredient list to create recipe, in order."""
        return self.ingredients

    def get_price(self):
        """Returns the price of the recipe."""
        return self.price

    def get_status(self):
        """Returns whether the recipe is currently locked or not."""
        return self.locked

    def set_status(self, state):
        """Sets the recipe state as either True (recipe locked) or False (recipe unlocked)."""
        self.locked = state

    def str(self):
        """Returns all attributes of the recipe in a sentence."""
        if self.locked == True:
            state = 'currently'
        else:
            state = 'currently not'
        return f"A/an {self.name} is made with {', '.join(i.name for i in self.ingredients)}, costs ${self.price}, and is {state} locked."

    def render(self):
        """Renders the recipe image. Used in recipe menu."""
        pass


Espresso = Recipe("Espresso Shot" ,[espresso_shot],6.50, "N/A", False)
Iced_Coffee = Recipe("Iced Coffee" ,[espresso_shot, ice],6.50, "N/A", False)
Americano = Recipe("Americano" ,[hot_water, espresso_shot],6.50, "N/A", False)
Latte = Recipe("Latte" ,[espresso_shot, steamed_milk],6.50, "N/A")
Iced_Latte = Recipe("Iced Latte" ,[espresso_shot, ice, milk],6.50, "N/A")


# Recipes Lists
ALL_RECIPES = [Espresso, Iced_Coffee, Americano, Latte, Iced_Latte]
RECIPES_UNLOCKED = []

# do once at the start of each level/day
for recipe in ALL_RECIPES:
    if recipe.locked == False:
        RECIPES_UNLOCKED.append(recipe)