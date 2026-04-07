from constants import *

class Customer(GameObject, pygame.sprite.Sprite):
    """
    An NPC that orders recipes, waits in line, and sits at tables.
    
    Attributes:
        sprite (pygame.Surface): The current visual image of the customer.
        recipes_unlocked (list): The list of available recipes the customer can pick from.
        ordered_item (Recipe): The specific recipe the customer has ordered.
        state (str): The current behavior state (waiting, finding seat, etc.).
        wait_bar_length (int): The current satisfaction/timer value.
    """
    def __init__(self, x, y, image_keys, recipes_unlocked_list, line_position):
        """
        Initializes a customer with a random order and a designated line position.
        
        Args:
            x (int): Starting horizontal position.
            y (int): Starting vertical position.
            image_keys (list): Keys for retrieved sprites from IMAGE_LIBRARY.
            recipes_unlocked_list (list): List of Recipe objects available for ordering.
            line_position (tuple): The (x, y) coordinate for the customer's spot in line.
        """
        pygame.sprite.Sprite.__init__(self)

        self.image_keys = image_keys
        try:
            self.sprite = IMAGE_LIBRARY[self.image_keys[0]]
        except KeyError:
            self.sprite = pygame.Surface((30 * 4, 67 * 4))
            self.sprite.fill((255, 0, 0))

        super().__init__(x, y, self.sprite.get_width(), self.sprite.get_height(), (0, 0, 0))
        self.image = self.sprite
        self.rect = self.image.get_rect(topleft=(x, y))

        self.recipes_unlocked = recipes_unlocked_list
        self.ordered_item = self.pick_item()
        self.state = "waiting"
        self.target_seat = None
        self.target_position = None
        self.line_position = line_position
        self.foot_w, self.foot_h = (18 * 4), (8 * 4)

        self.wait_bar_length = 10000

        # Drinking / leaving behavior
        self.drink_start_time = None
        self.drink_duration = 1500  # milliseconds
        self.serve_result = None

    def pick_item(self):
        """
        Picks a random item from the list of unlocked recipes.
        
        Returns:
            Recipe: The randomly selected recipe object.
        """
        item_num = random.randint(0, len(self.recipes_unlocked) - 1)
        return self.recipes_unlocked[item_num]

    def find_seat(self):
        """Moves the customer toward a target seat and occupies it upon arrival."""

        if self.target_seat is None:
            return

        target_x, target_y = self.target_seat.rect.x, self.target_seat.rect.y

        reached = self.move_toward_point(target_x, target_y)

        if reached:
            self.rect.center = self.target_seat.rect.center
            self.x, self.y = self.rect.x, self.rect.y
            self.state = "seated"
            # Changes the direction the customer is seated depending on the seat's number
            self.sprite = IMAGE_LIBRARY[self.image_keys[1]]
            if self.target_seat.num % 2 != 0:
                self.sprite = pygame.transform.flip(self.sprite, True, False)
            self.target_seat.occupy_seat(self)

            # Now that the customer is sitting, get rid of foot rect. Logic handled in get_foot_rect()
            self.foot_w = 0
            # Also reset wait bar
            self.wait_bar_length = 10000

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


    def move_up_in_line(self):
        """Move smoothly to the customer's next assigned line position."""
        target_x, target_y = self.line_position[0], self.line_position[1]

        reached = self.move_toward_point(target_x, target_y)
        if reached:
            self.state = "waiting"

    def start_drinking(self, result):
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
        if self.target_seat is not None:
            self.target_seat.open_seat()

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

    def set_target_seat(self, seat):
        """Assigns a target seat and sets a waypoint in front of it."""
        self.target_seat = seat
        # First walk up to a point in front of the chair area, then go to the exact seat
        self.target_position = (seat.rect.x, 330)

    def render(self, screen, debugmode=False):
        """Renders customer and satisfaction bar."""
        screen.blit(self.sprite, self.rect)

        wait_rect = pygame.Rect(self.rect.x, self.rect.y - 20, self.wait_bar_length // 100, 10)
        pygame.draw.rect(screen, (255, 255, 255), wait_rect)

        if debugmode is True:
            pygame.draw.rect(screen, (255, 255, 0), self.get_foot_rect(), 1)

    def calculate_tip(self):
        """
        Calculate tip based on remaining wait bar value.
        
        Returns:
            tuple: (base_pay, tip, total)
        """
        base_pay = self.ordered_item.get_price()
        tip_percent = self.wait_bar_length / 10000
        tip = round(base_pay * tip_percent, 2)
        total = round(base_pay + tip, 2)
        return base_pay, tip, total


    def _update_wait_bar(self):
        """Decrements the wait bar while seated or waiting; triggers leaving when empty."""
        if self.wait_bar_length == 0:
            self.state = "leaving"
        else:
            self.wait_bar_length -= 1

    def _handle_walking_to_line(self):
        """Walks the customer from off-screen to their line position."""
        target_x, target_y = self.line_position[0], self.line_position[1]
        if self.move_toward_point(target_x, target_y):
            self.state = "waiting"

    def _handle_walking_to_table(self):
        """Walks the customer to the waypoint in front of the table area."""
        if self.target_position is None:
            return
        if self.move_toward_point(self.target_position[0], self.target_position[1]):
            self.state = "finding seat"

    def _handle_drinking(self):
        """Waits out the drink timer then transitions to leaving."""
        if self.drink_start_time is not None:
            elapsed = pygame.time.get_ticks() - self.drink_start_time
            if elapsed >= self.drink_duration:
                self.state = "leaving"

    def _clamp_to_screen(self):
        """Keeps the customer inside the game window boundaries."""
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))

    def update(self, collisions):
        """
        Updates the customer's behavior every frame using a state machine.

        Args:
            collisions (list): List of collision boundaries (reserved for future use).
        """
        if self.state in ("waiting", "seated"):
            self._update_wait_bar()

        state_handlers = {
            "walking to line": self._handle_walking_to_line,
            "walking to table": self._handle_walking_to_table,
            "finding seat": self.find_seat,
            "moving up in line": self.move_up_in_line,
            "drinking": self._handle_drinking,
            "leaving": self.leave_cafe,
        }

        handler = state_handlers.get(self.state)
        if handler is not None:
            handler()

        if self.state not in ("leaving", "gone"):
            self._clamp_to_screen()

        # Synchronize logical position with sprite position
        self.x, self.y = self.rect.x, self.rect.y

    def get_foot_rect(self):
        """Returns a rectangle that only covers the feet area of the customer sprite."""
        if self.w > 0:
            foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
            foot_y = self.y + self.h - self.foot_h
            return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)
        return None

    def __str__(self):
        """Returns current state and assigned seat as a string."""
        return f'State: {self.state}, Target Seat: {self.target_seat}'