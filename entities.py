import random
import sys
import pygame

WIDTH, HEIGHT = 1366, 768

PLAYER_COLOR = (80, 180, 255)
TABLE_COLOR = (140, 110, 70)
REGISTER_COLOR = (0, 0, 0)
COUNTER_COLOR = (140, 110, 70)
SEAT_COLOR = (0, 0, 0)
NPC_COLOR = (255, 220, 80)

PLAYER_SPEED = 5

class Entity:
    def __init__(self, x, y, w, h, color):
        self.x, self.y, self.w, self.h, self.color = x, y, w, h, color
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.color = color

    def update(self, dt):
        pass

    def render(self, screen):
        return pygame.draw.rect(screen, self.color, self.rect)
    


class Player(Entity):
    def __init__(self, x, y, color = PLAYER_COLOR):
        super().__init__(x, y, 28, 28, color)


    def handle_movement(self, keys, collisions):
        # Store old position in case we hit something
        old_x, old_y = self.rect.x, self.rect.y

        # Move
        if keys[pygame.K_LEFT]:  self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]: self.rect.x += PLAYER_SPEED
        if keys[pygame.K_UP]:    self.rect.y -= PLAYER_SPEED
        if keys[pygame.K_DOWN]:  self.rect.y += PLAYER_SPEED

        
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))

        # Collision Check: If new position overlaps obstacle, move back
        for c in collisions:
            if self.rect.colliderect(c.rect):
                self.rect.x, self.rect.y = old_x, old_y
                break
        
        self.x, self.y = self.rect.x, self.rect.y


    def attempt_restock(self):
        pass

    def attempt_brew(self):
        pass

    def deliver(self):
        pass


class Table(Entity):
    def __init__(self, x, y, w=70, h=40, color = TABLE_COLOR):
        super().__init__(x, y, w, h, color)
        self.open = True
    
    def tableOpen(self, customerLeaving):
        pass


class Seat(Entity):
    def __init__(self, x, y, w = 20, h = 20, color = SEAT_COLOR):
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


class Counter(Entity):
    def __init__(self, x, y, w = 40, h = 240, color = COUNTER_COLOR):
        super().__init__(x, y, w, h, color)
        self.placeable = True
        self.top_counter = pygame.Rect(x, y, w, (h)/2)


class Register(Counter):
    def __init__(self, x, y, w = 40, h = 120):
        super().__init__(x, y, w, h, REGISTER_COLOR)
        self.customerWaiting = False
        #interaction box for register
        self.interactionZone = pygame.Rect(self.rect.x - 40, self.rect.y, self.rect.w + 40, self.rect.h)

        if self.customerWaiting == True:
            pass
        # change register imgae to display icon

    def setWaiting(self):
        self.customerWaiting = True

    def take_order(self, screen):
        #bring up order taking screen
        return screen.fill((0,0,0))

    

class Sink(Counter):
    pass




class NPC(Entity):
    def __init__(self, x, y, recipesUnlockedList):
        super().__init__(x, y, 22, 22, NPC_COLOR)
        self.recipesUnlocked = recipesUnlockedList
        self.orderedItem = self.pickItem()
        self.state = "waiting"
        self.targetSeat = None
    
    def pickItem(self):
        #picks a random number and selects that item in the list
        itemNum = random.randint(0, len(self.recipesUnlocked) - 1)
        return self.recipesUnlocked[itemNum]

    def findSeat(self):
        self.rect.center = self.targetSeat.rect.center
    
    def set_state(self, state):
        self.state = state

    def set_targetSeat(self, seat):
        self.targetSeat = seat
    
    def update(self, dt):
        if self.state == "finding seat" and self.targetSeat != None:
            self.findSeat()
            self.state = "seated"

        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))