from constants import *

class Ingredient(GameObject):
    """
    Represents individual items used in recipes or stored in inventory.

    Attributes:
        name (str): The display name of the ingredient.
        image (pygame.Surface): The current sprite for rendering.
        price (float): Cost to purchase the ingredient.
        an_input (bool): True if the item is a raw material for a machine.
        stackable (bool): Determines if multiple units occupy one inventory slot.
    """
    def __init__(self, name, image_keys, an_input=False, price_to_buy=0.0, quantity=0):
        """Sets up ingredient properties and pulls the initial sprite from the library."""
        self.image_keys = image_keys
        self.image = IMAGE_LIBRARY[self.image_keys[0]]
        image_rect = self.image.get_rect()

        # Initialize base GameObject with image dimensions
        super().__init__(x=0, y=0, w=image_rect.width, h=image_rect.height, color=(0, 0, 0))

        self.name = name
        self.price = price_to_buy
        self.an_input = an_input
        self.quantity = quantity
        self.stackable = True

    def render(self, screen):
        """Blits the ingredient's sprite at its current coordinates."""
        screen.blit(self.image, (self.x, self.y))


class Cup(GameObject):
    """
    An object used to hold brewed ingredients.
    
    Attributes:
        contents (list): List of ingredients currently inside the cup.
        stackable (bool): Tracks if the cup can be stacked in inventory.
    """
    def __init__(self, image_keys, contents=None):
        """Initializes cup with empty or pre-filled contents."""
        self.image_keys = image_keys
        self.image = IMAGE_LIBRARY[self.image_keys[0]]
        image_rect = self.image.get_rect()

        super().__init__(x=0, y=0, w=image_rect.width, h=image_rect.height, color=WHITE)
        self.name = "Cup"

        if contents != None:
            self.contents = contents
        else:
            self.contents = []
        #just here for testing with an already made drink
        if self.contents:
            self.stackable = False
        else:
            self.stackable = True

    def update(self):
        """Updates cup state and visuals based on contents."""
        if self.contents:
            self.stackable = False
            self.image = IMAGE_LIBRARY[self.image_keys[1]]
        else:
            self.stackable = True
            self.image = IMAGE_LIBRARY[self.image_keys[0]]

    def render(self, screen):
        """Blits the cup image to the screen."""
        screen.blit(self.image, (self.x, self.y))

    def __str__(self):
        """Returns string representation of the cup's state."""
        return f'Cup that is Stackable:{self.stackable} and contains {[ingredient.name for ingredient in self.contents]}'
