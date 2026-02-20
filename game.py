from entities import Player, Table, Counter, NPC
import random
import sys
import entities
import pygame

FPS = 60

BG_COLOR = (35, 35, 45)

NPC_SPAWN_EVERY_MS = 1200
MAX_NPCS = 10
Max_NPC_WAITING = 4

def main():
    pygame.init()
    screen = pygame.display.set_mode((entities.WIDTH, entities.HEIGHT))
    pygame.display.set_caption("Cafe Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    #Player
    player = Player(80, 80)

    counters = [
        Counter(200, 150),
        Counter(0, 150)
        ]
    
    #Tables (no logic yet)
    tables = [
        Table(520, 120),
        Table(650, 120),
        Table(780, 120),
        Table(520, 260),
        Table(650, 260),
        Table(780, 260),
    ]

    foodItems = {
        "Breakfast Bagel" : ["Bagel", "Egg", "Cheese", "Lettuce", "Plate"],
        "Ham Sandwich" : ["Bread", "Ham", "Cheese", "Lettuce", "Plate"]
    }

    drinkItems = {
        "Iced Coffee" : ["Coffee", "Ice", "Cup"],
        "Hot Coffee" : ["Coffee", "Cup"]
    }

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

            

            if event.type == SPAWN_EVENT and len(npcs) < MAX_NPCS and len(npcsWaiting) < 4:
                '''x = random.randint(0, entities.WIDTH - 22)
                y = random.randint(0, entities.HEIGHT - 22)'''
                if len(npcsWaiting) > 0:
                    x = npcsWaiting[-1].x + 30
                    y = npcsWaiting[-1].y
                else:
                    x = 250
                    y = 350
                currNPC = NPC(x, y)
                npcs.append(currNPC)
                npcsWaiting.append(currNPC)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    npcs.clear()  #quick reset


        player.update(dt, keys)
        for npc in npcs:
            npc.update(dt)


        screen.fill(BG_COLOR)

        for c in counters:
            c.draw(screen)

        for t in tables:
            t.draw(screen)

        for npc in npcs:
            npc.draw(screen)

        player.draw(screen)


        text = font.render(f"NPCs: {len(npcs)} | R to clear NPCs", True, (230, 230, 230))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()