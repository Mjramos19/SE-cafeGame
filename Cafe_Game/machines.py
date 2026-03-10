from constants import *

class Machine(GameObject, pygame.sprite.Sprite):
    def __init__(self, x, y, name, machine_input, outputs: list, num_outputs, runtime, mini_game_img_keys, w=150, h=90):
        pygame.sprite.Sprite.__init__(self)

        # Black square placeholder — replace with real sprites later
        self.sprite = pygame.Surface((w, h))
        self.sprite.fill((0, 0, 0))

        super().__init__(x, y, w, h, (0, 0, 0))
        self.rect = self.sprite.get_rect(topleft=(x, y))

        self.x, self.y = x, y
        self.name = name

        self.input = machine_input
        self.outputs = [o for o in outputs]

        if isinstance(num_outputs, int):
            self.num_outputs = num_outputs
        if isinstance(runtime, int):
            self.runtime = runtime

        self.contents = []
        self.state = 'empty'
        # states: empty, full, running, ready
        self.timer_start = 0
        self.error_start = 0
        self.selected_output = None

        # Interaction zone sits directly in front of (below) the machine.
        # Height of 200 ensures the zone reaches past the counter collision into the
        # area where the player can actually stand (~y=392 in the MIDDLE view).
        self.interaction_zone = pygame.Rect(self.x, self.y + self.h, self.w, 200)
        self.start_button = None

        self.ingredient = None
        self.ingredient_rect = None
        self.mini_game_img_keys = mini_game_img_keys


    def is_player_nearby(self, player):
        '''Returns True if the player's feet are within the machine's interaction zone.'''
        return player.get_foot_rect().colliderect(self.interaction_zone)

    def setup_minigame(self, ingredient):
        self.ingredient = ingredient
        self.ingredient.x, self.ingredient.y = 20, 500


    def mini_game_mode(self, screen, debug):
        """When the player interacts with a machine, the minigame mode is called. This mode has a new interaction zone, start button, and handles the rendering."""

        screen.blit(IMAGE_LIBRARY["minigame_bg"], (0, 0))
        self.mg_interaction_zone = pygame.Rect(400, 100, 400, 200)
        self.start_button = pygame.Rect(450, 210, 70, 70)

        if self.state == "error":
            screen.blit(IMAGE_LIBRARY[self.mini_game_img_keys[0]], (402, 145)) # location of image subject to change with different assets
            elapsed = pygame.time.get_ticks() - self.error_start
            if elapsed >= 1500:
                self.state = "empty"
        elif self.state == "running":
            screen.blit(IMAGE_LIBRARY[self.mini_game_img_keys[1]], (402, 145))
        elif self.state == "ready":
            screen.blit(IMAGE_LIBRARY[self.mini_game_img_keys[2]], (402, 145))

        if self.ingredient:
            screen.blit(self.ingredient.image, (self.ingredient.x, self.ingredient.y))
            self.ingredient_rect = self.ingredient.image.get_rect(topleft=(self.ingredient.x, self.ingredient.y))

        if debug == True:
            pygame.draw.rect(screen, (255, 255, 255), self.mg_interaction_zone, 3)
            pygame.draw.rect(screen, (255, 255, 255), self.start_button)
            if self.ingredient:
                pygame.draw.rect(screen, (255, 255, 255), self.ingredient_rect, 3)

    def add(self, ingredient):
        """Adds the current ingredient to the machine and changes state to full."""
        if ingredient != self.input:
            print(f"cannot add {ingredient} to {self.name}.")
            self.state = "error"
        else:
            self.state = "full"
            self.ingredient = None
            # need to update the code here to include removing the ingredient from the player's inventory. must consider opening the machine with an empty inventory to avoid crahses.

    def run_machine(self, num=0):
        '''Starts running the machine if it has been filled with the correct input.'''
        if self.state != "full":
            return
        print("run machine")
        self.selected_output = self.select_output(num)
        self.begin_timer()

    def begin_timer(self):
        '''Record start time and transition to running state.'''
        self.timer_start = pygame.time.get_ticks()
        self.state = "running"
        print("machine running")

    def update(self):
        '''Check if the running timer has elapsed and transition to ready if so.'''
        if self.state == "running":
            elapsed = pygame.time.get_ticks() - self.timer_start
            if elapsed >= self.runtime * 1000:
                self.state = "ready"
                self.contents = [self.selected_output] * self.num_outputs

    def select_output(self, index=0):
        """Returns the selceted output index from the list of outputs."""
        return self.outputs[0]

    def remove_output(self):
        """Returns the output from the ready machine."""
        if self.state != "ready":
            print("nothing is brewed")
        else:
            if len(self.contents) > 0:
                return self.contents.pop()

    def render(self, screen, debug=False):
        """Renders the machine sprite in cafe view."""
        screen.blit(self.sprite, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)