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


class Customer(GameObject, pygame.sprite.Sprite):
    """
    An NPC that orders recipes, waits in line, and sits at tables.
    
    Attributes:
        sprite (pygame.Surface): The current visual image of the customer.
        recipesUnlocked (list): The list of available recipes the customer can pick from.
        orderedItem (Recipe): The specific recipe the customer has ordered.
        state (str): The current behavior state (waiting, finding seat, etc.).
        waitBar_length (int): The current satisfaction/timer value.
    """
    def __init__(self, x, y, image_keys, recipesUnlockedList, linePosition):
        """
        Initializes a customer with a random order and a designated line position.
        
        Args:
            x (int): Starting horizontal position.
            y (int): Starting vertical position.
            image_keys (list): Keys for retrieved sprites from IMAGE_LIBRARY.
            recipesUnlockedList (list): List of Recipe objects available for ordering.
            linePosition (tuple): The (x, y) coordinate for the customer's spot in line.
        """
        pygame.sprite.Sprite.__init__(self)

        self.image_keys = image_keys
        try:
            self.sprite = IMAGE_LIBRARY[self.image_keys[0]]
        except:
            self.sprite = pygame.Surface((30 * 4, 67 * 4))
            self.sprite.fill((255, 0, 0))

        super().__init__(x, y, self.sprite.get_width(), self.sprite.get_height(), (0, 0, 0))
        self.image = self.sprite
        self.rect = self.image.get_rect(topleft=(x, y))

        self.recipesUnlocked = recipesUnlockedList
        self.orderedItem = self.pickItem()
        self.state = "waiting"
        self.targetSeat = None
        self.targetPosition = None
        self.linePosition = linePosition
        self.foot_w, self.foot_h = (18 * 4), (8 * 4)

        self.waitBar_length = 10000

        # Drinking / leaving behavior
        self.drink_start_time = None
        self.drink_duration = 1500  # milliseconds
        self.serve_result = None

    def pickItem(self):
        """
        Picks a random item from the list of unlocked recipes.
        
        Returns:
            Recipe: The randomly selected recipe object.
        """
        itemNum = random.randint(0, len(self.recipesUnlocked) - 1)
        return self.recipesUnlocked[itemNum]

    def findSeat(self):
        """Moves the customer toward a target seat and occupies it upon arrival."""

        if self.targetSeat is None:
            return

        target_x, target_y = self.targetSeat.rect.x, self.targetSeat.rect.y

        # calculate remaining distance between customer and seat every iteration
        distanceY = self.targetSeat.rect.y - self.rect.y
        distanceX = self.targetSeat.rect.x - self.rect.x

        reached = self.move_toward_point(target_x, target_y)

        if reached:
            self.rect.center = self.targetSeat.rect.center
            self.x, self.y = self.rect.x, self.rect.y
            self.state = "seated"
            # Changes the direction the customer is seated depending on the seat's number
            self.sprite = IMAGE_LIBRARY[self.image_keys[1]]
            if self.targetSeat.num % 2 != 0:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.targetSeat.occupySeat(self)

            # Now that the customer is sitting, get rid of foot rect. Logic handled in get_foot_rect()
            self.foot_w = 0
            # Also reset wait bar
            self.waitBar_length = 10000

    def move_toward_point(self, target_x, target_y):
        """
        Move toward a point smoothly. Returns True when the point is reached.
        
        Args:
            target_x (int): Horizontal target coordinate.
            target_y (int): Vertical target coordinate.
        """
        if abs(self.rect.x - target_x) <= CUSTOMER_SPEED:
            self.rect.x = target_x
        elif self.rect.x < target_x:
            self.rect.x += CUSTOMER_SPEED
        else:
            self.rect.x -= CUSTOMER_SPEED

        if abs(self.rect.y - target_y) <= CUSTOMER_SPEED:
            self.rect.y = target_y
        elif self.rect.y < target_y:
            self.rect.y += CUSTOMER_SPEED
        else:
            self.rect.y -= CUSTOMER_SPEED

        # Keep x/y synced with rect
        self.x, self.y = self.rect.x, self.rect.y

        return self.rect.x == target_x and self.rect.y == target_y


    def moveUpInLine(self):
        """Move smoothly to the customer's next assigned line position."""
        target_x, target_y = self.linePosition[0], self.linePosition[1]

        reached = self.move_toward_point(target_x, target_y)
        if reached:
            self.state = "waiting"

    def start_drinking(self, result):  # should be finding the result using the check_match() func from recipes
        """
        Put the customer into the drinking state after being served.
        
        Args:
            result (str): Either "correct" or "incorrect".
        """
        # Store whether the serve was correct or incorrect.
        self.serve_result = result

        # Start the timer for the short drinking delay.
        self.drink_start_time = pygame.time.get_ticks()

        # Move the customer into the drinking state.
        self.state = "drinking"

        # Free the seat immediately so it can be reused once the customer
        # finishes this short drinking phase.
        if self.targetSeat is not None:
            self.targetSeat.openSeat()

    def leave_cafe(self):
        """Moves the customer toward the exit coordinate off-screen."""
        self.sprite = IMAGE_LIBRARY[self.image_keys[0]]
          # Change back to walking sprite
        target_x = -self.w - 50
        target_y = self.rect.y

        reached = self.move_toward_point(target_x, target_y)

        if reached:
            self.state = "gone"


    def set_state(self, state):
        """Sets the customer's behavioral state."""
        self.state = state

    def set_targetSeat(self, seat):
        """Assigns a target seat and sets a waypoint in front of it."""
        self.targetSeat = seat
        # First walk up to a point in front of the chair area, then go to the exact seat
        self.targetPosition = (seat.rect.x, 330)

    def render(self, screen, debugmode):
        """Renders customer and satisfaction bar."""
        screen.blit(self.sprite, self.rect)

        waitRect = pygame.Rect(self.rect.x, self.rect.y - 20, self.waitBar_length // 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), waitRect)

        if debugmode == True:
            pygame.draw.rect(screen, (255, 255, 0), self.get_foot_rect(), 1)

    def calculate_tip(self):
        """
        Calculate tip based on remaining wait bar value.
        
        Returns:
            tuple: (base_pay, tip, total)
        """
        base_pay = self.orderedItem.get_price()
        tip_percent = self.waitBar_length / 10000
        tip = round(base_pay * tip_percent, 2)
        total = round(base_pay + tip, 2)
        return base_pay, tip, total


    def update(self, collisions):
        """
        Updates the customer's behavior every frame using a state machine.
        
        Args:
            collisions (list): List of collision boundaries.
        """

        #if customers wait bar is empty, set their state to leaving. Else, decrement by 1
        if self.state == "waiting" or self.state == "seated":
            if self.waitBar_length == 0:
                self.state = "leaving"
            else:
                self.waitBar_length -= 1

        # State 0: Walk in from off-screen to line position
        if self.state == "walking to line":
            target_x, target_y = self.linePosition[0], self.linePosition[1]
            reached = self.move_toward_point(target_x, target_y)
            if reached:
                self.state = "waiting"

        # State 1: Walking toward the table area
        if self.state == "walking to table" and self.targetPosition is not None:
            # Move toward the temporary target position
            reached = self.move_toward_point(
                self.targetPosition[0],
                self.targetPosition[1]
            )

            # Once the temporary position is reached switch state
            if reached:
                self.state = "finding seat"

        # State 2: Move toward assigned seat
        if self.state == "finding seat" and self.targetSeat is not None:
            self.findSeat()

        # State 3: Moving forward in the line
        if self.state == "moving up in line" and self.linePosition is not None:
            self.moveUpInLine()

        # State 4: Pause briefly to simulate drinking
        if self.state == "drinking":
            current_time = pygame.time.get_ticks()

            # Once the drink delay is over, begin leaving.
            if self.drink_start_time is not None:
                if current_time - self.drink_start_time >= self.drink_duration:
                    self.state = "leaving"

        # State 5: Leave the cafe
        if self.state == "leaving":
            self.leave_cafe()

        # Keep customer inside the game window unless they are
        # actively leaving or already gone.
        if self.state != "leaving" and self.state != "gone":
            self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
            self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))

        # Synchronize logical position with sprite position
        self.x, self.y = self.rect.x, self.rect.y

    def get_foot_rect(self):
        """Returns a rectangle that only covers the feet area of the customer sprite."""
        if self.w > 0:
            foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
            foot_y = self.y + self.h - self.foot_h
            return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)

    def __str__(self):
        """Returns current state and assigned seat as a string."""
        return f'State: {self.state}, Target Seat: {self.targetSeat}'


class Table(GameObject):
    """
    A furniture object that holds Seat objects.
    
    Attributes:
        seats (list): The list of individual Seat objects associated with this table.
        open (bool): Whether the table has available seats.
    """
    def __init__(self, x, y, w=70, h=40, color=TABLE_COLOR, seats = []):
        super().__init__(x, y, w, h, color)
        self.open = True
        self.seats = seats
        self.open = True

class Seat(GameObject):
    """
    A specific seating spot for a customer.
    
    Attributes:
        state (str): Current occupancy status (open, reserved, taken).
        seatedCustomer (Customer): The customer assigned to this seat.
        num (int): The unique seat ID for orientation and identification.
    """
    def __init__(self, x, y, num, w=70, h=15, color=SEAT_COLOR):
        super().__init__(x, y, w, h, color)
        self.state = "open"
        self.seatedCustomer = None
        self.num = num

    def get_seatX(self):
        """Returns the horizontal position of the seat."""
        return self.rect.x

    def get_seatY(self):
        """Returns the vertical position of the seat."""
        return self.rect.y

    def reserveSeat(self, customer):
        """Sets seat state to reserved for a specific customer."""
        self.state = "reserved"
        self.seatedCustomer = customer

    def occupySeat(self, customer):
        """Sets seat state to taken by a specific customer."""
        self.state = "taken"
        self.seatedCustomer = customer

    def openSeat(self):
        """Resets the seat to an open state."""
        self.state = "open"
        self.seatedCustomer = None


class Counter(GameObject):
    """
    Defines the visual and placeable part of a counter unit.
    
    Attributes:
        placeable (bool): Whether objects can be placed on this unit.
    """
    def __init__(self, x, y, w=150, h=90, color=COUNTER_COLOR):
        super().__init__(x, y, w, h, color)
        self.x, self.y = x, y
        self.placeable = True


class Register(Counter):
    """
    A specialized Counter that handles order-taking and customer queue logic.
    
    Attributes:
        interactionZone (pygame.Rect): The area where the player can trigger interaction.
        icon (pygame.Surface): The visual indicator for a waiting customer.
    """
    # this variable is shared amongst both register objects
    customerWaiting = False
    def __init__(self, x, y, iz_y, w=150, h=90): #will need to update and put a parameter for the current customer image key to be passed through.
        super().__init__(x, y, w, h, REGISTER_COLOR)
        self.placeable = False

        # interaction box for register
        self.interactionZone = pygame.Rect(self.rect.x, self.rect.y + iz_y, self.rect.w, self.rect.h)

        self.icon = IMAGE_LIBRARY["register_icon"]
        self.icon_rect = self.icon.get_rect(topleft=(x+55, y-85))

        # order screen variables
        self.order_screen = IMAGE_LIBRARY["order_screen"]
        self.customer_image = IMAGE_LIBRARY["ladybug_register"] #place holder until parameter is updated.
        self.customer_rect = pygame.Rect(500,75,200,418)


    def setWaiting(self):
        """Sets the shared customerWaiting flag to True."""
        Register.customerWaiting = True

    def take_order(self, screen, currentCust=None):
        """
        Draws the register order-taking screen and UI elements.
        
        Args:
            screen (pygame.Surface): The display surface.
            currentCust (Customer): The customer being served.
        """

        # to do: learn to crop customer to rectangle
        screen.blit(self.order_screen, (0,0))
        screen.blit(self.customer_image, self.customer_rect)

        # Fonts for register UI text
        title_font = pygame.font.SysFont(None, 36)
        body_font = pygame.font.SysFont(None, 28)

        # Main Title
        title_text = title_font.render("Register - Accepting an order gives you an empty cup", True, WHITE)
        screen.blit(title_text, (80, 70))

        # Show current customer order if available
        order_name = "???"
        if currentCust is not None and currentCust.orderedItem is not None:
            order_name = currentCust.orderedItem.get_name()
        
        # Speech buubble position - to the left of the customer
        bubble_x, bubble_y = 60, 100
        bubble_w, bubble_h = 420, 120

        # Draw bubble background
        pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_w, bubble_h), border_radius=20)

        # Draw tail pointing toward customer
        tail_points = [(bubble_x + bubble_w - 60, bubble_y + bubble_h),
                    (bubble_x + bubble_w + 20, bubble_y + bubble_h + 60),
                    (bubble_x + bubble_w - 120, bubble_y + bubble_h)]
        pygame.draw.polygon(screen, WHITE, tail_points)

        # Order text inside the bubble
        order_text = title_font.render(f"I want an {order_name}!", True, BLACK)
        screen.blit(order_text, (bubble_x + 20, bubble_y + 20))

        hint_text = body_font.render("...please :)", True, (80, 80, 80))
        screen.blit(hint_text, (bubble_x + 20, bubble_y + 65))
        # Control hints
        hint_accept = body_font.render("[S] Accept Order", True, WHITE)
        hint_close = body_font.render("[ESC] Leave Register", True, WHITE)

        screen.blit(hint_accept, (80, 300))
        screen.blit(hint_close, (80, 340))


    def render(self, screen):
        """Renders the register icon in the game world."""
        if Register.customerWaiting == True:
            screen.blit(self.icon, self.icon_rect)


class Sink(Counter):
    """
    A specialized Counter that handles clearing the player's inventory cup.
    
    Attributes:
        interactionZone (pygame.Rect): Area where player can interact with the sink.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.placeable = False

        self.interactionZone = pygame.Rect(self.rect.x, self.rect.y + 100, self.rect.w, self.rect.h)

    def clear_cup(self, player):
        """
        Empties the cup in the player's active inventory slot.
        
        Args:
            player (Player): The player instance performing the action.
        """
        curr_slot = player.inventory[player.selectedSlot]
        if curr_slot and isinstance(curr_slot[0], Cup) and curr_slot[0].contents:
            cup_to_clear = curr_slot.pop()

            #cup_to_clear = copy.deepcopy(cup_to_clear)  # Creates a new instance to avoid mutating the original cup in the inventory
            cup_to_clear.contents.clear()
            cup_to_clear.update()
            print(f'{cup_to_clear}')
            added = player.addInventoryItem(cup_to_clear, Cup)
            if not added:
                player.inventory[player.selectedSlot].append(cup_to_clear)
            return True
        return False   
    
    def is_player_nearby(self, player):
        """Checks if the player is within range of the sink."""
        return player.get_foot_rect().colliderect(self.interactionZone)

    def render(self, screen, debugmode):
        """Renders the sink unit visuals."""
        if debugmode == True:
            pygame.draw.rect(screen, WHITE, self.rect) 
            pygame.draw.rect(screen, (0, 0, 255), self.interactionZone, 2)

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