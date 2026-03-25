from constants import *
#hi

class GameObject:
    '''A GameObject determines an objects' position, dimensions, and display image.'''
    def __init__(self, x, y, w, h, color = None):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = color

    def render(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect)  # make render apply to all after making individual renders


class Player(GameObject, pygame.sprite.Sprite):
    '''The player class.'''
    def __init__(self, x, y, image_key):  # Pass the key for IMAGE_LIBRARY, will need to change to KEYS for animation
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
        '''A function that returns a rectangle that only covers the feet area of the player sprite.'''
        # Returns a rect located at the bottom-center of the player sprite.
        # Calculates the offset so the feet are centered horizontally and sit at the very bottom of the sprite vertically.
        foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
        foot_y = self.y + self.h - self.foot_h
        return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)


    def handle_movement(self, keys, collisions):
        '''A function that updates the player position if keys are pressed, and also handles collisions using the foot rectangle.'''
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

    
    #helper function to update hotbar quantities every frame
    def updateInventoryLengths(self):
        self.inventoryQuants = [len(self.inventory[0]), len(self.inventory[1]), len(self.inventory[2]), len(self.inventory[3])]

    #function add a given object to players inventory
    def addInventoryItem(self, item, type):
        #Loops through inventory slots
        for i in range(NUM_SLOTS):
            #if stack of same item is found, add item to stack
            if len(self.inventory[i]) != 0:
                if isinstance(self.inventory[i][0], type) and isinstance(item, type):
                    self.inventory[i].append(item)
                    self.updateInventoryLengths()
                    return
        #if stack was not found, loop again find first open slot and put it there
        for i in range(NUM_SLOTS):
            if len(self.inventory[i]) == 0:
                self.inventory[i].append(item)
                self.updateInventoryLengths()
                return
            
    
    #function to remove a given object from players inventory
    def popInventoryItem(self, item, type):
        #loop through hot bar
        for i in range(NUM_SLOTS):
            #check if there is an item or stack in that slot and if its type matches item to remove
            if len(self.inventory[i]) > 0 and isinstance(self.inventory[i][0], type):
                #Then loop through that slot list
                for j in range(len(self.inventory[i])):
                    #find that item in slot list
                    if self.inventory[i][j] == item:
                        #remove and return that item
                        removed = self.inventory[i].pop(j)
                        self.updateInventoryLengths()
                        return removed
        
    

    def render(self, screen, debugmode):
        screen.blit(self.sprite, self.rect)

        if debugmode == True:
            pygame.draw.rect(screen, (255, 255, 0), self.get_foot_rect(), 2)


# dirty table aspect - states - money collection
class Table(GameObject):
    def __init__(self, x, y, w=70, h=40, color=TABLE_COLOR, seats = []):
        super().__init__(x, y, w, h, color)
        self.open = True
        self.seats = seats
        self.open = True

class Seat(GameObject):
    def __init__(self, x, y, num, w=70, h=15, color=SEAT_COLOR):
        super().__init__(x, y, w, h, color)
        self.state = "open"
        self.seatedCustomer = None
        self.num = num

    def get_seatX(self):
        return self.rect.x

    def get_seatY(self):
        return self.rect.y

    def reserveSeat(self, customer):
        self.state = "reserved"
        self.seatedCustomer = customer

    def occupySeat(self, customer):
        self.state = "taken"
        self.seatedCustomer = customer

    def openSeat(self):
        self.state = "open"
        self.seatedCustomer = None


class Counter(GameObject):
    '''The counter class defines the placeable part of the counter, not collisions. It takes in an x and y value to place it on the screen.
    It has a set width and height because every counter top is the same, and a set color for debugging view.'''
    def __init__(self, x, y, w=150, h=90, color=COUNTER_COLOR):
        super().__init__(x, y, w, h, color)
        self.x, self.y = x, y
        self.placeable = True


class Register(Counter):
    '''A Register is a child of Counter that handles player interation within the zone and customer lineup behavior, whether a customer is at the register.'''
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
        self.customer_image = IMAGE_LIBRARY["ladybug_idle"] #place holder until parameter is updated.
        self.customer_rect = pygame.Rect(500,200,100,418)


    def setWaiting(self):
        Register.customerWaiting = True

    def take_order(self, screen, currentCust=None):
        """Draws the register order-taking screen and show control hints.
        Parameters:
            screen: The pygame surface to draw on
            currentCust: The current customer at the register."""

        # to do: learn to crop customer to rectangle
        screen.blit(self.order_screen, (0,0))
        screen.blit(self.customer_image, self.customer_rect)

        # Fonts for register UI text
        title_font = pygame.font.SysFont(None, 36)
        body_font = pygame.font.SysFont(None, 28)

        # Main Title
        title_text = title_font.render("Register - Accepting an order gives you an empty cup", True, WHITE)
        screen.blit(title_text, (80, 80))

        # Show current customer order if available
        if currentCust is not None and currentCust.order is not None:
            order_text = body_font.render(
                f"Order: {currentCust.order.drink_name}",
                True,
                WHITE
            )
            screen.blit(order_text, (80, 140))
        elif currentCust is not None and hasattr(currentCust, "orderedItem"):
            order_text = body_font.render(
                f"Order: {currentCust.orderedItem}",
                True,
                WHITE
            )
            screen.blit(order_text, (80, 140))

        # Control hints
        hint_accept = body_font.render("[S] Accept Order", True, WHITE)
        hint_close = body_font.render("[ESC] Leave Register", True, WHITE)

        screen.blit(hint_accept, (80, 220))
        screen.blit(hint_close, (80, 260))


    def render(self, screen):
        if Register.customerWaiting == True:
            screen.blit(self.icon, self.icon_rect)


class Sink(Counter):
    '''A Sink is a child of Counter that handles clearing the player's inventory cup of its contents.'''
    def __init__(self, x, y):
        super().__init__(x, y)
        pass


class Customer(GameObject, pygame.sprite.Sprite):
    '''The Customer class creates a customer object that walks to the register, will line up, will order a recipe, and
    will seat itself. Once the order is delivered, te customer will exit the level. A customer has a satisfaction bar determined by time.'''
    def __init__(self, x, y, image_keys, recipesUnlockedList, linePosition):
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

        self.waitBar_length = 10000

        # Drinking / leaving behavior
        self.drink_start_time = None
        self.drink_duration = 1500  # milliseconds
        self.serve_result = None

    def pickItem(self):
        '''A function that picks a random number and selects that item in the list of unlocked recipes.'''
        itemNum = random.randint(0, len(self.recipesUnlocked) - 1)
        return self.recipesUnlocked[itemNum]

    def findSeat(self):
        '''A function that finds a seat, calculates the distance and movement for customer to get to seat, and will occupy the seat once there.'''

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
        """Move toward a point smoothly. Returns True when the point is reached."""
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
        """Move smoothly to the customer's next line position."""
        target_x = self.linePosition[0] - (self.w // 2)
        target_y = self.linePosition[1] - (self.h // 2)

        reached = self.move_toward_point(target_x, target_y)
        if reached:
            self.state = "waiting"

    def start_drinking(self, result):  # should be finding the result using the check_match() func from recipes
        """Put the customer into the drinking state after being served.
        Parameters:
            result (str): Either "correct" or "incorrect". This is stored
            so later systems such as money, ratings, or tips can react
            to the serve result."""
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
        """
        Move the customer toward the exit.
        For now, the customer walks to the right side of the screen.
        Once they move off-screen, their state becomes 'gone'.
        """
        target_x = -self.w - 50
        target_y = self.rect.y

        reached = self.move_toward_point(target_x, target_y)

        if reached:
            self.state = "gone"


    def set_state(self, state):
        self.state = state

    def set_targetSeat(self, seat):
        self.targetSeat = seat
        # First walk up to a point in front of the chair area, then go to the exact seat
        self.targetPosition = (seat.rect.x, 330)

    def render(self, screen, debugmode):
        screen.blit(self.sprite, self.rect)
        #renders customers wait bar
        #Length of each bar is measured by customers waitBar_length attribute
        waitRect = pygame.Rect(self.rect.x, self.rect.y - 20, self.waitBar_length // 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), waitRect)

        waitRect = pygame.Rect(self.rect.x, self.rect.y - 20, self.waitBar_length // 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), waitRect)

        if debugmode == True:
            pygame.draw.rect(screen, (255, 255, 0), self.get_foot_rect(), 1)


    def update(self, collisions):
        """
        Updates the customer's behavior every frame.

        This function controls the state machine for the customer. Depending on
        the current state, the customer will:
        - Walk toward the seating area
        - Find and move to their assigned seat
        - Move up in the waiting line
        - Pause briefly to simulate drinking
        - Leave the cafe after being served
        """

        #if customers wait bar is empty, set their state to leaving. Else, decrement by 1
        if self.state == "waiting" or self.state == "seated":
            if self.waitBar_length == 0:
                self.state = "leaving"
            else:
                self.waitBar_length -= 1


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
        
        #if customers wait bar is empty, set their state to leaving. Else, decrement by 1
        if self.state == "waiting" or self.state == "seated":
            if self.waitBar_length == 0:
                self.state == "leaving"
            else:
                self.waitBar_length -= 1

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
        '''A function that returns a rectangle that only covers the feet area of the player sprite.'''
        if self.w > 0:
            foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
            foot_y = self.y + self.h - self.foot_h
            return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)

    def __str__(self):
        return f'State: {self.state}, Target Seat: {self.targetSeat}'


class Cup(GameObject):
    def __init__(self, x, y, w, h, ):
        super().__init__(x, y, w, h, color=WHITE)
        self.name = "Cup"
        self.contents = []

class sink(GameObject):
    def __init__(self, x, y, w, h):
        super().__init__(x, y, w, h)

'''
class Cup:
    """Represents a drink container held in the player's inventory. A cup may be empty or filled with a specific drink."""

    def __init__(self):
        self.contents: Optional[str] = None

    def is_empty(self) -> bool:
        return self.contents is None

    def fill(self, drink_name) -> None:
        self.contents = drink_name

    def clear(self) -> None:
        self.contents = None


class Order:
    """Represents a customer's drink order."""

    def __init__(self, seat_number, drink_name, color):
        self.seat_number = seat_number
        self.drink_name = drink_name
        self.color = color
        self.resolved = False

    def mark_resolved(self) -> None:
        self.resolved = True


class CupInventory:
    """Holds the player's cup inventory."""
    def __init__(self):
        self.slots: list[Optional[Cup]] = [None] * MAX_CUP_SLOTS
        self.selected_slot: Optional[int] = None

    def first_empty_slot(self):
        for i in range(len(self.slots)):
            if self.slots[i] is None:
                return i
        return None

    def add_empty_cup(self):
        slot = self.first_empty_slot()
        if slot is None:
            return False

        self.slots[slot] = Cup()
        return True

    def remove_cup(self, slot):
        self.slots[slot] = None

    def select_slot(self, slot):
        if 0 <= slot < len(self.slots):
            if self.selected_slot == slot:
                self.selected_slot = None
            else:
                self.selected_slot = slot

    def get_selected_cup(self):
        if self.selected_slot is None:
            return None
        return self.slots[self.selected_slot]

    def clear_all(self):
        """Clear all cup slots and remove any current selection"""
        for i in range(len(self.slots)):
            self.slots[i] = None

        self.selected_slot = None'''
