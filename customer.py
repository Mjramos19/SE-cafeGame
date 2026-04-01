from constants import *

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
