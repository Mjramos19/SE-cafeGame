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


    def check_match(self, cup: list):
        """Will take the ingredients of the current drink and try to match it to whatever recipe the customer has as
        their ordered recipe. Is called when trying to deliver and returns True or False."""
        if len(self.ingredients) != len(cup.contents):
            return False
        i = 0
        for item in self.ingredients:
            if item != cup.contents[i]:
                return False
            i += 1
        return True

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
