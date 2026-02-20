from entities import Player, Table, Counter, NPC, Register, Seat
import random
import sys
import entities
import pygame

FPS = 60
PLAYING = "playing"
REGISTER = "register"


BG_COLOR = (35, 35, 45)

NPC_SPAWN_EVERY_MS = 1200
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
        Seat(800, 230)
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
        dt = clock.tick(FPS) / 1000.0  #seconds
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #if wait line is not current full and total customers not at max, spawn new customer
            if event.type == SPAWN_EVENT and len(npcs) < MAX_NPCS and len(npcsWaiting) < 4:
                if len(npcsWaiting) > 0:
                    x = npcsWaiting[-1].x + 30
                    y = npcsWaiting[-1].y
                    currNPC = NPC(x, y, recipes_unlocked)
                else:
                    x = 250
                    y = 350
                    #sets current customer to the one in front of the line
                    currNPC = NPC(x, y, recipes_unlocked)
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
                
                if event.key == pygame.K_s and gameState == REGISTER:
                    seat = findFirstOpen(collisions)
                    if seat:
                        seat.reserveSeat(currentCust)
                        currentCust.set_targetSeat(seat)
                        currentCust.set_state("finding seat")
                        npcsWaiting.pop(0)
                        seat.occupySeat(currentCust)
                        gameState = PLAYING




        if gameState == PLAYING:
            screen.fill(BG_COLOR)
            #player movement
            player.handle_movement(keys, collisions)

            player.render(screen)

            for npc in npcs:
                npc.update(dt)

            #Spawn all collideable objects
            for c in collisions:
                c.render(screen)

            #Spawn all npc objects
            for npc in npcs:
                npc.render(screen)
        
            pygame.draw.rect(screen, (255,0,0), register.interactionZone, 2)

            #Spawn player object
            player.render(screen)

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
