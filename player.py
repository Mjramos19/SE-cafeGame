from constants import *

class Player(GameObject, pygame.sprite.Sprite):
    """
    The main controllable entity in the cafe.
    
    Attributes:
        sprite (pygame.Surface): The current visual image of the player.
        rect (pygame.Rect): The collision and position rectangle.
        foot_w (int): The width of the specialized foot collision box.
        foot_h (int): The height of the specialized foot collision box.
        selectedSlot (int): The index of the currently active inventory slot.
        inventory (list): A 2D list containing item objects for each slot.
        inventoryQuants (list): A list tracking the quantity of items in each slot.
    """
    def __init__(self, x, y, image_key):  # Pass the key for IMAGE_LIBRARY, will need to change to KEYS for animation
        """
        Initializes the player with a sprite and an empty 4-slot inventory.
        
        Args:
            x (int): Starting horizontal position.
            y (int): Starting vertical position.
            image_key (str): Key to retrieve the player sprite from IMAGE_LIBRARY.
        """
        pygame.sprite.Sprite.__init__(self)
        try:
            self.sprite = IMAGE_LIBRARY[image_key]
        except:
            self.sprite = pygame.Surface((30 * 4, 67 * 4))
            self.sprite.fill((255, 0, 0))

        super().__init__(x, y, self.sprite.get_width(), self.sprite.get_height(), (0, 0, 0))
        self.image = self.sprite
        self.rect = self.image.get_rect(topleft=(x, y))

        self.foot_w = (18 * 4)
        self.foot_h = (8 * 4)

        self.selectedSlot = 0
        self.inventory = [[], [], [], []]
        self.inventoryQuants = [0, 0, 0, 0]


    def get_foot_rect(self):
        """
        Returns a rectangle that only covers the feet area of the player sprite.
        
        Returns:
            pygame.Rect: A rectangle located at the bottom-center of the player.
        """
        # Returns a rect located at the bottom-center of the player sprite.
        # Calculates the offset so the feet are centered horizontally and sit at the very bottom of the sprite vertically.
        foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
        foot_y = self.y + self.h - self.foot_h
        return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)


    def handle_movement(self, keys, collisions):
        """
        Updates the player position if keys are pressed and handles collisions.
        
        Args:
            keys (pygame.key.ScancodeWrapper): The state of all keyboard buttons.
            collisions (list): A list of Rect objects to check against for collisions.
        """
        # Stores old position in case plyer hits something
        old_x, old_y = self.rect.x, self.rect.y

        # Inputs for movement
        if keys[pygame.K_LEFT]:  self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:    self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:  self.rect.y += PLAYER_SPEED

        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))
        self.x, self.y = self.rect.x, self.rect.y

        # Collision Check: If new position overlaps obstacle, move back
        for c in collisions:
            if self.get_foot_rect().colliderect(c):
                self.rect.x, self.rect.y = old_x, old_y
                self.x, self.y = old_x, old_y
                break

    def deliver(self, table):
        """Placeholder for the item delivery function."""
        pass

#helper function to update hotbar quantities every frame
    def updateInventoryLengths(self):
        """Updates the inventoryQuants list with current lengths of inventory slots."""
        self.inventoryQuants = [len(self.inventory[0]), len(self.inventory[1]), len(self.inventory[2]), len(self.inventory[3])]

    #function add a given object to players inventory
    def addInventoryItem(self, item, item_type):
        """
        Adds a given object to the player's inventory, handling stacking logic.
        
        Args:
            item (GameObject): The object to be added.
            item_type (type): The class type of the item for comparison.
        """
        if item.stackable:
            for i in range(NUM_SLOTS):
                slot = self.inventory[i]
                if len(slot) != 0:
                    # Check if it's the same type
                    if isinstance(slot[0], item_type) and isinstance(item, item_type):
                        # Only stack cups if they are both empty
                        if isinstance(item, Cup):
                            if (slot[0] == None and item.contents) or (slot[0].contents and item.contents == None):
                                continue 
                        
                        # Ingredient name check for stackable ingredients
                        if isinstance(item, Ingredient) and slot[0].name != item.name:
                            continue
                        
                        print(slot)
                        slot.append(item)
                        return True

        # Find empty slot logic
        for i in range(NUM_SLOTS):
            if len(self.inventory[i]) == 0:
                self.inventory[i].append(item)
                return True
        return False

    #function to remove a given object from players inventory
    def popInventoryItem(self, item, type):
        """
        Removes a given object from the player's inventory and returns it.
        
        Args:
            item (GameObject): The specific instance to remove.
            type (type): The class type of the item.
        """
        #loop through hot bar
        for i in range(NUM_SLOTS):
            #check if there is an item or stack in that slot and if its type matches item to remove
            if len(self.inventory[i]) > 0 and isinstance(self.inventory[i][0], type):
                #Then loop through that slot list
                for j in range(len(self.inventory[i])):
                    #find that item in slot list
                    if self.inventory[i][j] == item:
                        #remove and return that item
                        print(f'popped {item.name} from inventory space list' + str(self.inventory[i]))
                        return self.inventory[i].pop(j)
                        


    def render(self, screen, debugmode):
        """
        Renders the player sprite and optional debug collision box.
        
        Args:
            screen (pygame.Surface): The display surface to draw on.
            debugmode (bool): Whether to draw the foot collision rectangle.
        """
        screen.blit(self.sprite, self.rect)

        if debugmode == True:
            pygame.draw.rect(screen, (255, 255, 0), self.get_foot_rect(), 2)
