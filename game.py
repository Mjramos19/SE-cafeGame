from entities import Player, Table, Counter, NPC, Register, Seat
import random
import sys
import entities
import pygame

FPS = 60
PLAYING = "playing"
REGISTER = "register"


BG_COLOR = (35, 35, 45)

#List of line position tuples (x,y)
#paralleled with NPCS waiting list
linePositions = [(250,350), (280,350), (310,350), (340,350)]

NPC_SPAWN_EVERY_MS = 2400
MAX_NPCS = 10
Max_NPC_WAITING = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((1366, 768))
    pygame.display.set_caption("Cafe Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)
    gameState = PLAYING

    #Player
    player = Player(80, 80)
    register = Register(200, 150)
    currentCust = None
    currNPC = None

    collisions = [
        Counter(200, 150),
        Counter(0, 150),
        Table(520, 120),
        Table(650, 120),
        Table(780, 120),
        Table(520, 260),
        Table(650, 260),
        Table(780, 260),
        Seat(780, 230),
        Seat(830, 230),
        Seat(650, 230),
        Seat(700, 230),
        Seat(520, 230),
        Seat(570, 230),
        ]
    
    ingredients = {}

    recipes = []

    recipes_unlocked = ["Breakfast Bagel", "Breakfast Sandwich", "Iced Coffee", "Hot Coffee"]

    #Other entities (NPCs)
    npcs = []
    npcsWaiting = []

    #Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, NPC_SPAWN_EVERY_MS)

    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #if wait line is not current full and total customers not at max, spawn new customer
            if event.type == SPAWN_EVENT and len(npcs) < MAX_NPCS and len(npcsWaiting) < 4:
                #if customers already waiting, put new one in back of line
                if len(npcsWaiting) > 0:
                    x, y = linePositions[len(npcsWaiting)][0], linePositions[len(npcsWaiting)][1]
                    currNPC = NPC(x, y, recipes_unlocked, linePosition = linePositions[len(npcsWaiting) - 1])
                #if customer is first in line, put them at the counter and set currrent customer to that npc
                elif len(npcsWaiting) == 0:
                    x, y = linePositions[0][0], linePositions[0][1]
                    #sets current customer to the one in front of the line
                    currNPC = NPC(x, y, recipes_unlocked, linePosition = linePositions[len(npcsWaiting) - 1])
                    currentCust = currNPC

                npcs.append(currNPC)
                npcsWaiting.append(currNPC)
                register.setWaiting()
                '''DONT FORGET TO SET WAITING BACK TO FALSE WHEN LINE IS EMPTY'''

            if event.type == pygame.KEYDOWN: #quick reset NPCS
                if event.key == pygame.K_r:
                    npcs.clear()

                #if player presses e inside registers collission zone, and there is a customer, take order
                if event.key == pygame.K_e and player.rect.colliderect(register.interactionZone) and register.customerWaiting:
                    gameState = REGISTER
                
                #if player presses esc inside register, return game state to playing and exit register
                if event.key == pygame.K_ESCAPE and gameState == REGISTER:
                    gameState = PLAYING
                
                #Player press s while in register to take order and send customer to seat
                if event.key == pygame.K_s and gameState == REGISTER:
                    seat = findFirstOpen(collisions)
                    if seat:
                        #reserve open seat
                        seat.reserveSeat(currentCust)

                        #set npc objects target seat
                        currentCust.set_targetSeat(seat)

                        #set npc state to finding seat
                        currentCust.set_state("finding seat")

                        #Remove from line
                        npcsWaiting.pop(0)
                        
                        #set every npc's line position to the next one up and change their state
                        for i in range(0, len(npcsWaiting)):
                            npcsWaiting[i].state = "moving up in line"
                            npcsWaiting[i].linePosition = linePositions[i]

                        #set customer in front of the line to next up
                        if len(npcsWaiting) > 0:
                            currentCust = npcsWaiting[0]
                        gameState = PLAYING




        if gameState == PLAYING:
            screen.fill(BG_COLOR)
            #player movement
            player.handle_movement(keys, collisions)

            player.render(screen)

            #Update NPCS positions
            for npc in npcs:
                npc.update(collisions)

            #Spawn all collideable objects
            for c in collisions:
                c.render(screen)

            #Spawn all npc objects
            for npc in npcs:
                npc.render(screen)

            #Register interaction range
            pygame.draw.rect(screen, (255,0,0), register.interactionZone, 2)

            #Spawn player object
            player.render(screen)

            #Spawn register object
            register.render(screen)
        
        elif gameState == REGISTER:
            register.take_order(screen)


        text = font.render(f"NPCs: {len(npcs)} | R to clear NPCs", True, (230, 230, 230))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

#Finds first open seat in collisions list and returns it. None if all occupied
def findFirstOpen(collisions):
        for c in collisions:
            if isinstance(c, Seat) and c.state == "open":
                return c
        return None


if __name__ == "__main__":
    main()
