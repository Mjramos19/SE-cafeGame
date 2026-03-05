import random
import pygame
from constants import *


class GameObject:
    '''A GameObject determines an objects' position, dimensions, and display image.'''
    def __init__(self, x, y, w, h, color):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = color

    def render(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect)  # make render apply to all after making individual renders


class Player(GameObject, pygame.sprite.Sprite):
    '''The player class.'''
    def __init__(self, x, y, image_key):  # Pass the key for IMAGE_LIBRARY
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
        self.activeOrders = []
        self.foodInHand = []
        self.top_inventory = []
        self.ti_rect = pygame.Rect(10,340, 50,50)
        self.bottom_inventory = []
        self.bi_rect = pygame.Rect(10,410, 50,50)


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


    def attempt_restock(self):
        pass

    def attempt_brew(self):
        pass

    def deliver(self):
        #loops through each seat at the table in which the player is standing.
        #If the seat is occupied, checks if food in hand matches the item ordered from that customer
        #and delivers it if so
        for seat in table.seats:
            if seat.seatedCustomer != None:
                if seat.seatedCustomer.orderedItem in self.foodInHand and seat.seatedCustomer.state != "eating":
                    seat.seatedCustomer.state = "eating"
                    self.foodInHand.remove(seat.seatedCustomer.orderedItem)

    def render(self, screen):
        screen.blit(self.sprite, self.rect)
        pygame.draw.rect(screen, (0,0,0), self.ti_rect)
        pygame.draw.rect(screen, (0,0,0), self.bi_rect)

# dirty table aspect - states - money collection
class Table(GameObject):
    def __init__(self, x, y, w=70, h=40, color=TABLE_COLOR, seats = []):
        super().__init__(x, y, w, h, color)
        self.open = True
        self.seats = seats
        self.open = True


class Seat(GameObject):
    def __init__(self, x, y, w=70, h=15, color=SEAT_COLOR):
        super().__init__(x, y, w, h, color)
        self.state = "open"
        self.seatedCustomer = None

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
    def __init__(self, x, y, iz_y, w=150, h=90):
        super().__init__(x, y, w, h, REGISTER_COLOR)
        self.placeable = False
        self.customerWaiting = False
        # interaction box for register
        self.interactionZone = pygame.Rect(self.rect.x, self.rect.y + iz_y, self.rect.w, self.rect.h)

        self.icon = IMAGE_LIBRARY["register_icon"]
        self.icon_rect = self.icon.get_rect(topleft=(x+55, y-85))

        # order screen variables
        self.order_screen = IMAGE_LIBRARY["order_screen"]
        self.customer_image = IMAGE_LIBRARY["customer"] #place holder
        self.customer_rect = pygame.Rect(500,200,100,418)
        if self.customerWaiting == True:
            pass  # change register image to display icon


    def setWaiting(self):
        self.customerWaiting = True

    def setOpen(self):
        self.customerWaiting = False

    def take_order(self, screen, currentCust=None):
        '''A function that brings up the order taking screen.'''
        # bring up order taking screen - learn to crop customer to rectangle
        screen.blit(self.order_screen, (0,0))
        screen.blit(self.customer_image, self.customer_rect)





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
    def __init__(self, x, y, image_key, recipesUnlockedList, linePosition):
        pygame.sprite.Sprite.__init__(self)

        try:
            self.sprite = IMAGE_LIBRARY[image_key]
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


    def pickItem(self):
        '''A function that picks a random number and selects that item in the list of unlocked recipes.'''
        itemNum = random.randint(0, len(self.recipesUnlocked) - 1)
        return self.recipesUnlocked[itemNum]

    def findSeat(self, collisions):
        '''A function that finds a seat, calculates the distance and movement for customer to get to seat, and will occupy the seat once there.'''

        # Set original coordinates for collisions
        '''old_x = self.rect.x
        old_y = self.rect.y'''

        # targest seats x and y coords
        targetX, targetY = self.targetSeat.rect.x, self.targetSeat.rect.y

        # calculate remaining distance between customer and seat every iteration
        distanceY = self.targetSeat.rect.y - self.rect.y
        distanceX = self.targetSeat.rect.x - self.rect.x

        # increment positions by CUSTOMER_SPEED
        if self.rect.x < targetX:
            self.rect.x += CUSTOMER_SPEED
        elif self.rect.x > targetX:
            self.rect.x -= CUSTOMER_SPEED

        if self.rect.y < targetY:
            self.rect.y += CUSTOMER_SPEED
        elif self.rect.y > targetY:
            self.rect.y -= CUSTOMER_SPEED

        # if NPC is close enough that the next iteration would put them past the seat,
        # snap them onto the seat and mark them seated
        if distanceY < CUSTOMER_SPEED and distanceX < CUSTOMER_SPEED:
            self.rect.center = self.targetSeat.rect.center
            self.state = "seated"
            self.targetSeat.occupySeat(self)

    def moveUpInLine(self):
        # increment the npc's x coordinate by their speed until they reach their new
        # line position

        target_x = self.linePosition[0] - (self.w // 2)

        if self.rect.x > target_x:
            self.rect.x -= CUSTOMER_SPEED
            # Snap to position if close enough to prevent jitter
            if self.rect.x - target_x < CUSTOMER_SPEED:
                self.rect.x = target_x
                self.state = "waiting"
        elif self.rect.x < target_x:
            self.rect.x += CUSTOMER_SPEED
            if target_x - self.rect.x < CUSTOMER_SPEED:
                self.rect.x = target_x
                self.state = "waiting"


    def set_state(self, state):
        self.state = state

    def set_targetSeat(self, seat):
        self.targetSeat = seat


    def render(self, screen):
        screen.blit(self.sprite, self.rect)


    def update(self, collisions):
        # If npc's state is "finding seat", call findseat function to incremement coords until seated
        if self.state == "finding seat" and self.targetSeat != None:
            self.findSeat(collisions)

        # If npc's state is "moving up in line", call moveUpInLine to increment x coord until new
        # spot in line is reached.
        if self.state == "moving up in line" and self.linePosition != None:
            self.moveUpInLine()

        # clamp npc's to screen
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))

    def get_foot_rect(self):
        '''A function that returns a rectangle that only covers the feet area of the player sprite.'''
        foot_x = self.x + (self.w // 2) - (self.foot_w // 2)
        foot_y = self.y + self.h - self.foot_h
        return pygame.Rect(foot_x, foot_y, self.foot_w, self.foot_h)

    def __str__(self):
        return f'State: {self.state}, Target Seat: {self.targetSeat}'