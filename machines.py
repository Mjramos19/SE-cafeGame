
from classes import GameObject
import pygame
from constants import INGREDIENTS, Ingredient


class Machine(GameObject, pygame.sprite.Sprite):
    def __init__(self, x, y, name, machine_input, outputs: list, num_outputs, runtime, w=150, h=90):
        pygame.sprite.Sprite.__init__(self)

        # Black square placeholder — replace with real sprites later
        self.sprite = pygame.Surface((w, h))
        self.sprite.fill((0, 0, 0))

        super().__init__(x, y, w, h, (0, 0, 0))
        self.rect = self.sprite.get_rect(topleft=(x, y))

        self.x, self.y = x, y
        self.name = name

        if machine_input in INGREDIENTS:
            self.input = machine_input
        self.outputs = [o for o in outputs if o in INGREDIENTS]

        if isinstance(num_outputs, int):
            self.num_outputs = num_outputs
        if isinstance(runtime, int):
            self.runtime = runtime

        self.contents = []
        self.state = 'empty'
        # states: empty, full, running, ready
        self.timer_start = 0
        self.selected_output = None

        # Interaction zone sits directly in front of (below) the machine.
        # Height of 200 ensures the zone reaches past the counter collision into the
        # area where the player can actually stand (~y=392 in the MIDDLE view).
        self.interaction_zone = pygame.Rect(self.x, self.y + self.h, self.w, 200)
        self.start_button = pygame.Rect(self.x + 20, self.y + 5, self.w - 45, self.h - 45)

    def is_player_nearby(self, player):
        '''Returns True if the player's feet are within the machine's interaction zone.'''
        return player.get_foot_rect().colliderect(self.interaction_zone)

    def mini_game_mode(self, screen, font):
        '''Simple machine UI shown when the player opens a machine.'''
        screen.fill((30, 30, 30))
        cx = screen.get_width() // 2

        title = font.render(self.name, True, (255, 255, 255))
        screen.blit(title, (cx - title.get_width() // 2, 100))

        state_text = font.render(f"State: {self.state}", True, (200, 200, 200))
        screen.blit(state_text, (cx - state_text.get_width() // 2, 160))

        if self.state == "empty":
            prompt = font.render("No input loaded.", True, (180, 180, 180))
        elif self.state == "full":
            prompt = font.render(f"Press E to run {self.name}.", True, (100, 255, 100))
        elif self.state == "running":
            elapsed = pygame.time.get_ticks() - self.timer_start
            remaining = max(0, self.runtime - elapsed // 1000)
            prompt = font.render(f"Running... {remaining}s remaining", True, (255, 200, 0))
        elif self.state == "ready":
            prompt = font.render("Output ready! Press E to collect.", True, (100, 255, 100))
        else:
            prompt = font.render("", True, (255, 255, 255))

        screen.blit(prompt, (cx - prompt.get_width() // 2, 260))

        hint = font.render("ESC to close", True, (150, 150, 150))
        screen.blit(hint, (cx - hint.get_width() // 2, 700))

    def add(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            print(f"cannot add {ingredient} to {self.name}.")
        else:
            self.state = "full"

    def run_machine(self, num=0):
        '''Start the machine running if it has been filled with the correct input.'''
        if self.state != "full":
            return
        self.selected_output = self.select_output(num)
        self.begin_timer()

    def begin_timer(self):
        '''Record start time and transition to running state.'''
        self.timer_start = pygame.time.get_ticks()
        self.state = "running"

    def update(self):
        '''Check if the running timer has elapsed and transition to ready if so.'''
        if self.state == "running":
            elapsed = pygame.time.get_ticks() - self.timer_start
            if elapsed >= self.runtime * 1000:
                self.state = "ready"
                self.contents = [self.selected_output] * self.num_outputs

    def select_output(self, index=0):
        return self.outputs[0]

    def remove_output(self):
        if self.state != "ready":
            print("nothing is brewed")
        else:
            if len(self.contents) > 0:
                return self.contents.pop()

    def render(self, screen, debug=False):
        screen.blit(self.sprite, self.rect)
        if debug:
            pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
