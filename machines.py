
from classes import GameObject
import pygame

from constants import IMAGE_LIBRARY, INGREDIENTS, Ingredient


class Machines(GameObject, pygame.sprite.Sprite):
    def __init__(self, x, y, name, input, outputs: list, num_outputs, runtime, image_key):
        pygame.sprite.Sprite.__init__(self)

        try:
            self.sprite = IMAGE_LIBRARY[image_key]
        except:
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 0))

        super().__init__(x, y, self.sprite.get_width(), self.sprite.get_height(), (0, 0, 0))
        self.rect = self.sprite.get_rect(topleft=(x, y))

        self.x, self.y = x, y
        if isinstance(name, str):
            self.name = name
        if input in INGREDIENTS:
            self.input = input
        for o in outputs:
            if o in INGREDIENTS:
                self.outputs = outputs
        if isinstance(num_outputs, int):
            self.num_outputs = num_outputs
        if isinstance(runtime, int):
            self.runtime = runtime

        self.contents = []
        if len(self.contents) == 0:
            self.state = 'empty'
        # states can be empty, full, running, ready

        self.interaction_zone = pygame.Rect(self.x, self.y - 30, self.w, self.h - 20)
        self.start_button = pygame.Rect(self.x + 20, self.y + 5, self.w - 45, self.h - 45)

    def mini_game_mode(self, screen, image_key):
        '''A function that sets up the minigame mode of the machine. This is where the player can drag an ingredient into the machine and press the button to run the machine.'''
        # once gamestate is minigame mode, this will be called (image, interaction zone, and their locations will be changed) for now there are fillers
        screen.fill((0, 0, 0))
        try:
            self.sprite = IMAGE_LIBRARY[image_key]
        except:
            self.sprite = pygame.Surface((50, 50))
            self.sprite.fill((255, 0, 0))
        self.interaction_zone = pygame.Rect(self.x, self.y - 30, self.w, self.h - 20)
        # needs to update movement of the ingredient as the mouse drags it

        # see if the player dragging the ingredient collides with the machine interaction zone - if so try self.add(ingredient)

    def add(self, ingredient):
        if not isinstance(ingredient, Ingredient):
            print(f"cannot add {ingredient} to {self.name}.")
            #display a red x by the machine
        else:
            self.state = "full"



    def run_machine(self, state, num):
        '''This function will run the machine if the player has filled the machine with the correct input.'''
        # need to include timer bar that will change the state to ready once it has brewed.
        # player tries to press start_button while in minigame mode
        if self.state != "full":
            return  #play an error noise
        else:
            output = self.select_output(num)
            time = self.begin_timer()
            if time == 0:
                self.state = "ready"
                self.contents = [output] * self.num_outputs

    def begin_timer(self):
        time = self.runtime
        #clock logic of time running out
        return time

    def select_output(self, index):
        return self.outputs[0]

    def remove_output(self):
        if self.state != "ready":
            print("nothing is brewed")
        else:
            if len(self.contents) > 0:
                output = self.contents.pop()
                return output  # this output can be added o the player's inventory or drink cup


    def render(self, screen, gamestate, mode):
        # will render different things based on the gamestate
        if gamestate == "FRONT":

            if mode == True:
                pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
            return
        elif gamestate == "MIDDLE":

            if mode == True:
                pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
            return
        elif gamestate == "MINIGAME":
            # this view needs to show the machine close up, the player's inventory/ingredient selected

            if mode == True:
                pygame.draw.rect(screen, (255, 255, 0), self.interaction_zone, 2)
            return







