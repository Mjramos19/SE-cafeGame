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

PLAYER_SPEED = 1
NPC_SPEED = 1

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
        #Currently placeholder black screen
        return screen.fill((0,0,0))

    

class Sink(Counter):
    def __init__(self):
        pass




class NPC(Entity):
    def __init__(self, x, y, recipesUnlockedList, linePosition):
        super().__init__(x, y, 22, 22, NPC_COLOR)
        self.recipesUnlocked = recipesUnlockedList
        self.orderedItem = self.pickItem()
        self.state = "waiting"
        self.targetSeat = None
        self.targetPosition = None
        self.linePosition = linePosition

    def pickItem(self):
        #picks a random number and selects that item in the list
        itemNum = random.randint(0, len(self.recipesUnlocked) - 1)
        return self.recipesUnlocked[itemNum]

    def findSeat(self, collisions):
        #Set original coordinates for collisions
        '''old_x = self.rect.x
        old_y = self.rect.y'''

        #targest seats x and y coords
        targetX, targetY = self.targetSeat.rect.x, self.targetSeat.rect.y

        #calculate remaining distance between customer and seat every iteration
        distanceY = self.targetSeat.rect.y - self.rect.y
        distanceX = self.targetSeat.rect.x - self.rect.x

        #increment positions by NPC_SPEED
        if self.rect.x < targetX:
            self.rect.x += NPC_SPEED
        elif self.rect.x > targetX:
            self.rect.x -= NPC_SPEED
        
        if self.rect.y < targetY:
            self.rect.y += NPC_SPEED
        elif self.rect.y > targetY:
            self.rect.y -= NPC_SPEED

        #if NPC is close enough that the next iteration would put them past the seat,
        #snap them onto the seat and mark them seated
        if distanceY < NPC_SPEED and distanceX < NPC_SPEED:
            self.rect.center = self.targetSeat.rect.center
            self.state = "seated" 
            self.targetSeat.occupySeat(self)

        '''
        Scrapping collisions for now - cannot find an efficient way to move around seats

        for c in collisions:
            if self.rect.colliderect(c.rect):
                self.rect.y, self.rect.x = old_y, old_x
                break'''

    def moveUpInLine(self):
        #increment the npc's x coordinate by their speed until they reach their new
        #line position
        if self.rect.x != self.linePosition[0]:
            self.rect.x -= NPC_SPEED
        
        #Snap them into their line spot once they get close enough
        #Set their state back to waiting
        if self.rect.x - self.linePosition[0] < NPC_SPEED:
            self.rect.x = self.linePosition[0]
            self.state = "waiting"

    def set_state(self, state):
        self.state = state

    def set_targetSeat(self, seat):
        self.targetSeat = seat
    
    def update(self, collisions):
        #If npc's state is "finding seat", call findseat function to incremement coords until seated
        if self.state == "finding seat" and self.targetSeat != None:
            self.findSeat(collisions)

        #If npc's state is "moving up in line", call moveUpInLine to increment x coord until new
        #spot in line is reached.
        if self.state == "moving up in line" and self.linePosition != None:
            self.moveUpInLine()

        #clamp npc's to screen
        self.rect.x = max(0, min(WIDTH - self.rect.w, self.rect.x))
        self.rect.y = max(0, min(HEIGHT - self.rect.h, self.rect.y))