
from classes import GameObject, Player, Table, Counter, Customer, Register, Seat, foodCounter
import constants
from constants import *
import sys
import pygame

pygame.init()
screen = pygame.display.set_mode((1366, 768))
'''
TODO:
* add more machines (one for drinks, one for food for now)
* make customers dissapear after they eat
* Make seperate lists for food and drink active orders and only utilize each list for its given machine
* begin logic for customers coming to get food at counter
* start basic money making
'''


constants.IMAGE_LIBRARY["player"] = pygame.image.load("Cafe_Game_Art/player.png").convert_alpha()
constants.IMAGE_LIBRARY["customer"] = pygame.image.load("Cafe_Game_Art/Customer.png").convert_alpha()
constants.IMAGE_LIBRARY["bg1"] = pygame.image.load("Cafe_Game_Art/cafe_bg.png").convert_alpha()
constants.IMAGE_LIBRARY["bg1_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_top.png").convert_alpha()
constants.IMAGE_LIBRARY["bg2"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2.png").convert()
constants.IMAGE_LIBRARY["bg2_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2_top.png").convert_alpha()

# Pre-scale all images in the library them once
constants.IMAGE_LIBRARY["player"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player"], (120, 268))
constants.IMAGE_LIBRARY["customer"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["customer"], (120, 268))
constants.IMAGE_LIBRARY["bg1"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1"], (1366, 768))
constants.IMAGE_LIBRARY["bg1_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1_top"], (1366, 768))
constants.IMAGE_LIBRARY["bg2"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2"], (1366, 768))
constants.IMAGE_LIBRARY["bg2_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2_top"], (1366, 768))



# front room collision rects
counter3_rect = pygame.Rect(0, 590, 983, 50)
wall_rect2 = pygame.Rect(0, 293, 1400, 10)

# behind counter / middle collision rects
counter1_rect = pygame.Rect(187, 336, 983, 50)
counter2_rect = pygame.Rect(187, 718, 983, 50)
wall_rect = pygame.Rect(0, 333, 1400, 10)
menu_rect = pygame.Rect(1150, 0, 100, 800)

# builds all counters (about 165 apart from each other)
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = (Counter(7, 487), Counter(172, 487), Counter(336, 487),
                                           Counter(500, 487), Counter(664, 487), Counter(193, 234),
                                           Counter(358, 234), Counter(522, 234), Counter(686, 234), Counter(850, 234))

s1, s2, s3, s4, s5, s6 = Seat(38, 243), Seat(253, 243), Seat(445, 243), Seat(660, 243), Seat(850, 243), Seat(1064, 243)


# build two registers - one for customers, the other dependent on the first and will display icon, can take order from both and will update the other
register1 = Register(829, 487)

#oven object
oven = foodCounter(c10.x,c10.y, c10.w, c10.h)
# register2 = Register(200, 150)

currentCust = None
currCustomer = None


# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
back_collisions = [menu_rect]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
seats = [s1, s2, s3, s4, s5, s6]
tables = [Table(150, 200,seats = [s1, s2]), Table(550, 200,seats = [s3, s4]), Table(950, 200,seats = [s5, s6])]
machines = [oven]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10]
back_shelves = []




def main():
    global Customer, currentCust
    pygame.display.set_caption("Cafe Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    DebugMode = True

    GameState = "PLAYING"
    CafeView = "FRONT"


    # Other entities (Customers)
    customers = []
    customersWaiting = []

    # Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player")
    all_sprites.add(player)


    running = True
    while running:
        # These are universal events no matter the state

        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION:
                m_x, m_y = pygame.mouse.get_pos()
                #print(f"Mouse position: X={m_x}, Y={m_y}")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if DebugMode == False:
                        DebugMode = True
                    else:
                        DebugMode = False

                if event.key == pygame.K_r:  # R clears the customers for testing
                    #quick reset Game
                    customers.clear()
                    customersWaiting.clear()
                    player.activeOrders.clear()
                    for s in seats:
                        if isinstance(s, Seat):
                            s.state = "open"
                            s.seatedCustomer = None

                if event.key == pygame.K_q:
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        c1.rect.x, c1.rect.y = 1014, 615
                        c2.rect.x, c2.rect.y = 849, 615
                        c3.rect.x, c3.rect.y = 685, 615
                        c4.rect.x, c4.rect.y = 522, 615
                        c5.rect.x, c5.rect.y = 357, 615
                    else:
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        c1.rect.x, c1.rect.y = 7, 487
                        c2.rect.x, c2.rect.y = 172, 487
                        c3.rect.x, c3.rect.y = 336, 487
                        c4.rect.x, c4.rect.y = 500, 487
                        c5.rect.x, c5.rect.y = 664, 487

                # if player presses e inside registers collission zone, and there is a customer, take order
                if event.key == pygame.K_e and player.rect.colliderect(register1.interactionZone) and register1.customerWaiting: # and register1.customerWaiting:
                    GameState = "REGISTER"
                elif event.key == pygame.K_e and player.rect.colliderect(oven.interactionZone) and len(player.activeOrders) > 0:
                    GameState = "COOKING"
                elif event.key == pygame.K_ESCAPE and GameState == "REGISTER":
                    GameState = "PLAYING"


                elif event.key == pygame.K_s and GameState == "REGISTER":
                    player.activeOrders.append(currentCust.orderedItem)
                    seat = Customer.findFirstOpen(seats)  # find open seat

                    if seat:
                        # reserve open seat
                        seat.reserveSeat(currentCust)

                        # set Customer objects target seat
                        currentCust.set_targetSeat(seat)

                        # set Customer state to finding seat
                        currentCust.set_state("finding seat")

                        # Remove from line
                        customersWaiting.pop(0)

                        if len(customersWaiting) == 0:
                            register1.setOpen()

                        # set every Customer's line position to the next one up and change their state
                        for i in range(0, len(customersWaiting)):
                            customersWaiting[i].state = "moving up in line"
                            customersWaiting[i].linePosition = LINE_POSITIONS[i]

                        # set customer in front of the line to next up
                        if len(customersWaiting) > 0:
                            currentCust = customersWaiting[0]
                        GameState = "PLAYING"

                #Food preparation
                elif event.key == pygame.K_s and GameState == "COOKING":
                    
                    player.foodInHand.append(player.activeOrders.pop(0))

                    GameState = "PLAYING"
                
                #food delivery
                elif event.key == pygame.K_e and GameState == "PLAYING":
                    #Looks for which table the player is interaction with
                    #sends the table address to the players deliver function
                    for t in tables:
                        if isinstance(t, Table): #To be added: "and table.open == False"
                            if player.rect.colliderect(t.interactionZone):
                                player.deliver(t)
                                break
                        
                
            # if wait line is not current full and total customers not at max, spawn new customer
            if event.type == SPAWN_EVENT and len(customers) < MAX_CUSTOMERS and len(
                    customersWaiting) < MAX_CUSTOMERS_WAITING:

                # Calculate the index for the new customer
                index = len(customersWaiting)
                base_x, base_y = LINE_POSITIONS[index]

                # Center the spawn coordinates
                spawn_x = base_x - 60
                spawn_y = base_y - 64

                # Create the customer using the key "customer" from your IMAGE_LIBRARY
                currCustomer = Customer(spawn_x, spawn_y, "customer", RECIPES_UNLOCKED, linePosition=LINE_POSITIONS[index])
                
                if currCustomer.rect.colliderect(player.get_foot_rect()):
                    player.rect.y -= 60
                
                if index == 0:
                    currentCust = currCustomer

                all_sprites.add(currCustomer)
                customer_group.add(currCustomer)

                # Add to tracking lists
                customers.append(currCustomer)
                customersWaiting.append(currCustomer)
                register1.setWaiting()


        if GameState == "PLAYING":

            if CafeView == "FRONT":
                temp_cols = list(front_collisions)
                for c in customers:
                    temp_cols.append(c.get_foot_rect())
                player.handle_movement(keys, temp_cols)

                # handles all layering with renders
                screen.blit(constants.IMAGE_LIBRARY["bg1"], (0, 0))

                depth_list = customers + [player]
                depth_list.sort(key=lambda obj: obj.rect.bottom)

                if player.rect.bottom < 610:
                    for entity in depth_list:
                        entity.render(screen)
                    screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
                else:
                    for c in customers:
                        c.render(screen)
                    screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
                    # 3. Draw the player last (on top of everything)
                    player.render(screen)
                foodInHandText = font.render(f"Food in Hand: {player.foodInHand}", True, (230, 230, 230))
                screen.blit(foodInHandText, (500, 10))


                if DebugMode == True:
                    for c in front_counters:
                        pygame.draw.rect(screen, (250, 0, 0), c)
                    pygame.draw.rect(screen, (255, 255, 0), register1.interactionZone, 3)
                    for c in front_collisions:
                        pygame.draw.rect(screen, (255, 255, 0), c, 2)
                    for t in tables:
                        pygame.draw.rect(screen, (255, 0, 0), t)
                        pygame.draw.rect(screen, (255, 255, 0), t.interactionZone, 2)

            elif CafeView == "MIDDLE":
                player.handle_movement(keys, middle_collisions)
                screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))
                player.render(screen)
                screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))

                if DebugMode == True:
                    for c in middle_collisions:
                        pygame.draw.rect(screen, (255, 255, 0), c, 2)
                    for c in middle_counters:
                        pygame.draw.rect(screen, (250, 0, 0), c)
                    for m in machines:
                        pygame.draw.rect(screen, (255, 255, 0), m.interactionZone, 2)

                oven.render(screen)
                foodInHandText = font.render(f"Food in Hand: {player.foodInHand}", True, (230, 230, 230))
                screen.blit(foodInHandText, (400, 10))

            else:
                player.handle_movement(keys, back_collisions)
                screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))
                player.render(screen)
                screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))

                if DebugMode == True:
                    for c in back_collisions:
                        pygame.draw.rect(screen, (255, 255, 0), c, 2)
                    for c in middle_counters:
                        pygame.draw.rect(screen, (250, 0, 0), c)
                    
                

            '''these things run while playing'''

            for c in customers:
                c.update(seats)


            if DebugMode == True:
                pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

        elif GameState == "REGISTER":
            register1.take_order(screen)
            message = font.render(f"Press S to Take Order and Seat Customer", True, (230, 230, 230))
            screen.blit(message, (500, 500))
        
        elif GameState == "COOKING":
            oven.cookFood(screen)
            message = font.render(f"Press S to Cook Food: {player.activeOrders}", True, (230, 230, 230))
            screen.blit(message, (500, 10))

        clock.tick(FPS)

        text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps():.0f}", True, (230, 230, 230))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
