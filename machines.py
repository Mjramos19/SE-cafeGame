from constants import *

class Machine(GameObject, pygame.sprite.Sprite):
    def __init__(self, x, y, name, machine_input, outputs: list, num_outputs, runtime, mini_game_img_keys, w=150, h=90):
        pygame.sprite.Sprite.__init__(self)

        self.state = 'empty'
        # states: empty, full, running, ready
        self.mini_game_img_keys = mini_game_img_keys

        # Black square placeholder — replace with real sprites later
        try:
            self.sprite = self.get_sprite()
        except:
            self.sprite = pygame.Surface((w, h))
            self.sprite.fill((0, 0, 0))

        super().__init__(x, y, w, h, (0, 0, 0))
        self.counter_space_rect = pygame.rect.Rect(x, y, w, h)
        self.rect = self.sprite.get_rect(topleft=(x,y))
        self.rect.centerx = self.counter_space_rect.centerx
        self.rect.centery = self.counter_space_rect.centery
        self.rect.y -= 50  # accounts for the height above the counter

        self.name = name
        self.input = machine_input
        self.outputs = [o for o in outputs]

        if isinstance(num_outputs, int):
            self.num_outputs = num_outputs
        if isinstance(runtime, int):
            self.runtime = runtime

        self.contents = []

        self.timer_start = 0
        self.error_start = 0
        self.selected_output = None

        # Interaction zone sits directly in front of (below) the machine.
        # Uses the sprite rect's actual width and x so each machine's zone
        # matches its visual footprint exactly, with no overlap between machines.
        self.interaction_zone = pygame.Rect(self.rect.x, self.y + self.h, self.rect.width, 150)
        self.start_button = None

        self.ingredient = None
        self.ingredient_rect = None

    def get_sprite(self):
        if self.state == 'running':
            self.sprite = self.mini_game_img_keys[1]
        elif self.state == 'ready':
            self.sprite = self.mini_game_img_keys[2]
        else:
            self.sprite = self.mini_game_img_keys[0]
        return IMAGE_LIBRARY[self.sprite]


    def is_player_nearby(self, player):
        '''Returns True if the player's feet are within the machine's interaction zone.'''
        return player.get_foot_rect().colliderect(self.interaction_zone)

    def setup_minigame(self, ingredient_list):
        temp_list = ingredient_list.copy()
        
        if len(temp_list) > 0:
            self.ingredient = temp_list.pop()
        else:
            self.ingredient = None
        if self.ingredient != None:
            self.ingredient.x, self.ingredient.y = 20, 500


    def mini_game_mode(self, screen, debug, font):
        """When the player interacts with a machine, the minigame mode is called. This mode has a new interaction zone, start button, and handles the rendering."""

        screen.blit(IMAGE_LIBRARY["minigame_bg"], (0, 0))
        self.minigame_rect = pygame.Rect(400, 100, 400, 590)
        if self.name == "Coffee Grinder":
            self.mg_interaction_zone = pygame.Rect(400, self.minigame_rect.top + 20, 400, 200)
            self.start_button = pygame.Rect(self.minigame_rect.centerx - 35, 480, 70, 70)
        elif self.name == "Espresso Machine":
            self.mg_interaction_zone = pygame.Rect(400, self.minigame_rect.centery - 50, 400, 150)
            self.start_button = pygame.Rect(490, 255, 65, 50)
        elif self.name == "Water Boiler":
                self.mg_interaction_zone = pygame.Rect(400, self.minigame_rect.centery - 50, 400, 200)
                self.start_button = pygame.Rect(455, 220, 70, 90)
        else:
            self.mg_interaction_zone = pygame.Rect(400, self.minigame_rect.centery - 100, 400, 200)
            self.start_button = pygame.Rect(450, 210, 70, 70)

        # might not need this code later
        if self.state == "error":
            elapsed = pygame.time.get_ticks() - self.error_start
            if elapsed >= 1500:
                self.state = "empty"
        elif self.state == "running":
            elapsed = pygame.time.get_ticks() - self.timer_start
            remaining = max(0, self.runtime - elapsed // 1000)
            prompt = font.render(f"Running... {remaining}s remaining", True, (255, 200, 0))
            screen.blit(prompt, (400, 80))

        def scale_image_to_fit(img, rect):
            """Scales the machine image proportionally to fit inside the minigame_mode rect."""
            img_width, img_height = img.get_size()
            rect_width, rect_height = rect.size
            scale_factor = min(rect_width / img_width, rect_height / img_height)
            new_width = int(img_width * scale_factor)
            new_height = int(img_height * scale_factor)
            return pygame.transform.smoothscale(img, (new_width, new_height))

        scaled_image = scale_image_to_fit(self.get_sprite(), self.minigame_rect)
        scaled_rect = scaled_image.get_rect(center=self.minigame_rect.center)
        screen.blit(scaled_image, scaled_rect)

        if self.ingredient:
            screen.blit(self.ingredient.image, (self.ingredient.x, self.ingredient.y))
            self.ingredient_rect = self.ingredient.image.get_rect(topleft=(self.ingredient.x, self.ingredient.y))

        if debug == True:
            pygame.draw.rect(screen, (255, 255, 255), self.mg_interaction_zone, 3)
            pygame.draw.rect(screen, (255, 255, 255), self.start_button)
            pygame.draw.rect(screen, (255, 255, 0), self.minigame_rect, 1)
            if self.ingredient:
                pygame.draw.rect(screen, (255, 255, 255), self.ingredient_rect, 3)

    def add(self, ingredient, player):
        """Adds the current ingredient to the machine and changes state to full."""
        if ingredient != self.input:
            print(f"cannot add {ingredient} to {self.name}.")
            self.state = "error"
        else:
            self.state = "full"
            player.popInventoryItem(self.ingredient, type(self.ingredient))
            self.ingredient = None

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
        screen.blit(self.get_sprite(), self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
            pygame.draw.rect(screen, (20, 20, 20), self.rect)