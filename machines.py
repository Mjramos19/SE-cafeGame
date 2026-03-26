from constants import *

class Machine(GameObject, pygame.sprite.Sprite):
    """
    Represents a functional appliance in the cafe, such as an Espresso Machine or Grinder.
    
    The machine follows a state-based lifecycle: empty -> full -> running -> ready.
    It includes a 'mini_game_mode' for player interaction and internal timers to 
    process ingredients into outputs.
    """
    def __init__(self, x, y, name, machine_input, outputs: list, num_outputs, runtime, mini_game_img_keys, start_button_info, w=150, h=90):
        """
        Initializes the machine with its processing rules and visual assets.
        
        Args:
            x (int): X-coordinate on the counter.
            y (int): Y-coordinate on the counter.
            name (str): The display name of the machine.
            machine_input (Ingredient): The specific ingredient type this machine accepts.
            outputs (list): Possible items this machine can produce.
            num_outputs (int): How many items are produced per cycle.
            runtime (int): Processing time in seconds.
            mini_game_img_keys (list): Keys for empty, running, and ready sprites.
            start_button_info (list): [x, y, w, h] for the minigame start button.
            w (int): Width of the machine's footprint.
            h (int): Height of the machine's footprint.
        """
        pygame.sprite.Sprite.__init__(self)

        self.state = 'empty'
        self.mini_game_img_keys = mini_game_img_keys

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
        self.rect.y -= 50 

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
          
        self.interaction_zone = pygame.Rect(self.rect.x, self.y + self.h, self.rect.width - 40, 100)
        self.interaction_zone.centerx = self.rect.centerx
        self.start_button = pygame.Rect(start_button_info[0], start_button_info[1], start_button_info[2], start_button_info[3])

        self.ingredient = None
        self.ingredient_rect = None

    def get_sprite(self):
        """Returns the appropriate sprite from IMAGE_LIBRARY based on current state."""
        if self.state == 'running':
            self.sprite = self.mini_game_img_keys[1]
        elif self.state == 'ready':
            self.sprite = self.mini_game_img_keys[2]
        else:
            self.sprite = self.mini_game_img_keys[0]
        return IMAGE_LIBRARY[self.sprite]

    def is_player_nearby(self, player):
        """Returns True if the player's feet are within the machine's interaction zone."""
        return player.get_foot_rect().colliderect(self.interaction_zone)

    def setup_minigame(self, ingredient_list):
        """Prepares the local ingredient reference for the minigame view."""
        temp_list = ingredient_list.copy()
        
        if len(temp_list) > 0:
            self.ingredient = temp_list.pop()
        else:
            self.ingredient = None
            
        if self.ingredient != None:
            self.ingredient.x, self.ingredient.y = 20, 500

    def mini_game_mode(self, screen, debug, font):
        """
        Handles the specialized full-screen UI rendering for machine interaction.
        
        This includes scaling the machine sprite, drawing the background, 
        and showing timer progress.
        """
        screen.blit(IMAGE_LIBRARY["minigame_bg"], (0, 0))
        self.minigame_rect = pygame.Rect(400, 100, 400, 590)
        self.mg_interaction_zone = pygame.Rect(400, self.minigame_rect.centery - 100, 400, 200)

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
            """Internal helper to scale the machine sprite for the minigame UI."""
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
        """
        Attempts to load an ingredient into the machine. 
        Sets state to 'error' if input is invalid.
        """
        if ingredient != self.input:
            print(f"cannot add {ingredient} to {self.name}.")
            self.state = "error"
        else:
            self.state = "full"
            player.popInventoryItem(self.ingredient, type(self.ingredient))
            self.ingredient = None

    def run_machine(self, num=0):
        """Starts the production cycle if the machine is currently full."""
        if self.state != "full":
            return
        print("run machine")
        self.selected_output = self.select_output(num)
        self.begin_timer()

    def begin_timer(self):
        """Captures start ticks and transitions machine to the running state."""
        self.timer_start = pygame.time.get_ticks()
        self.state = "running"
        print("machine running")

    def update(self):
        """
        Monitors the active timer. 
        Transitions state to 'ready' and spawns contents once runtime expires.
        """
        if self.state == "running":
            elapsed = pygame.time.get_ticks() - self.timer_start
            if elapsed >= self.runtime * 1000:
                self.state = "ready"
                self.contents = [self.selected_output] * self.num_outputs

    def select_output(self, index=0):
        """Determines which output from the list will be produced."""
        return self.outputs[0]

    def remove_output(self):
        """Returns one item from the machine's contents if the state is 'ready'."""
        if self.state != "ready":
            print("nothing is brewed")
        else:
            if len(self.contents) > 0:
                return self.contents.pop()

    def render(self, screen, debug=False):
        """Draws the machine in the standard cafe view."""
        screen.blit(self.get_sprite(), self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
            pygame.draw.rect(screen, (20, 20, 20), self.rect)