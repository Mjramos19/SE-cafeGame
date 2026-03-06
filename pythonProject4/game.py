

#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py



from classes import GameObject, Player, Table, Counter, Customer, Register, Seat
from machines import Machine
import constants
from recipes import *
from constants import *
import sys
import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1366, 768))

constants.IMAGE_LIBRARY["player"] = pygame.image.load("Cafe_Game_Art/player.png").convert_alpha()
constants.IMAGE_LIBRARY["customer"] = pygame.image.load("Cafe_Game_Art/Customer.png").convert_alpha()
constants.IMAGE_LIBRARY["order_screen"] = pygame.image.load("Cafe_Game_Art/order_screen.png").convert()
constants.IMAGE_LIBRARY["bg1"] = pygame.image.load("Cafe_Game_Art/cafe_bg.png").convert_alpha()
constants.IMAGE_LIBRARY["bg1_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_top.png").convert_alpha()
constants.IMAGE_LIBRARY["bg2"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2.png").convert()
constants.IMAGE_LIBRARY["bg2_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2_top.png").convert_alpha()
constants.IMAGE_LIBRARY["register_icon"] = pygame.image.load("Cafe_Game_Art/register_icon.png").convert_alpha()

# Pre-scale all images in the library them once
constants.IMAGE_LIBRARY["player"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player"], (120, 268))
constants.IMAGE_LIBRARY["customer"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["customer"], (120, 268))
constants.IMAGE_LIBRARY["order_screen"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["order_screen"], (1366, 768))
constants.IMAGE_LIBRARY["bg1"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1"], (1366, 768))
constants.IMAGE_LIBRARY["bg1_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1_top"], (1366, 768))
constants.IMAGE_LIBRARY["bg2"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2"], (1366, 768))
constants.IMAGE_LIBRARY["bg2_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2_top"], (1366, 768))
constants.IMAGE_LIBRARY["register_icon"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["register_icon"], ((17*2), (33*2)))


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
register1 = Register(829, 487, 110)
register2 = Register(193, 615, 10)

currentCust = None
currCustomer = None


# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
back_collisions = [menu_rect]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
seats = [s1, s2, s3, s4, s5, s6]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, register2]
back_shelves = []

grinder        = Machine(193, 234, "Coffee Grinder",   bag_coffee_beans, [ground_coffee],            1, 3)
espresso_mach  = Machine(358, 234, "Espresso Machine", ground_coffee,    [espresso_shot],            1, 5)
steamer        = Machine(522, 234, "Milk Steamer",     milk,             [steamed_milk, foamed_milk], 1, 4)
machines = [grinder, espresso_mach, steamer]


def main():
    global Customer, currentCust
    pygame.display.set_caption("Cafe Sim")
    clock = pygame.time.Clock()
    START_TIME = pygame.time.get_ticks()
    font = pygame.font.SysFont(None, 22)

    DebugMode = True

    GameState = "PLAYING"
    CafeView = "FRONT"

    active_machine = None

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

    # orders list
    orders_list = []


    running = True
    while running:
        # These are universal events no matter the state

        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION and DebugMode==True:
                m_x, m_y = pygame.mouse.get_pos()
                print(f"Mouse position: X={m_x}, Y={m_y}")

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if DebugMode == False:
                        DebugMode = True
                    else:
                        DebugMode = False

                if event.key == pygame.K_r:  # R clears the customers for testing
                    customers.clear()

                if event.key == pygame.K_q and GameState=="PLAYING":
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        change_counters_pos(CafeView)
                    else:
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        change_counters_pos(CafeView)

                # if player presses e inside registers collision zone, and there is a customer, take order
                if event.key == pygame.K_e:
                    if player.rect.colliderect(register1.interactionZone) and register1.customerWaiting:
                        GameState = "REGISTER"
                    if player.rect.colliderect(register2.interactionZone) and register2.customerWaiting:
                        GameState = "REGISTER"

                if event.key == pygame.K_ESCAPE and GameState == "REGISTER":
                    GameState = "PLAYING"

                if event.key == pygame.K_e and CafeView == "MIDDLE" and GameState == "PLAYING":
                    for m in machines:
                        if m.is_player_nearby(player):
                            active_machine = m
                            GameState = "MACHINE"
                            break

                if event.key == pygame.K_ESCAPE and GameState == "MACHINE":
                    GameState = "PLAYING"
                    active_machine = None

                if event.key == pygame.K_e and GameState == "MACHINE" and active_machine:
                    if active_machine.state == "full":
                        active_machine.run_machine()
                    elif active_machine.state == "ready":
                        result = active_machine.remove_output()
                        if result:
                            print(f"Collected: {result.name}")
                        if not active_machine.contents:
                            active_machine.state = "empty"


                if event.key == pygame.K_s and GameState == "REGISTER":

                    orders_list.insert(0, currentCust.orderedItem)
                    time.sleep(1)

                    seat = findFirstOpen(seats)  # find open seat

                    if seat:
                        # reserve open seat
                        seat.reserveSeat(currentCust)
                        # set Customer objects target seat
                        currentCust.set_targetSeat(seat)
                        # set Customer state to finding seat
                        currentCust.set_state("finding seat")
                        # Remove from line
                        customersWaiting.pop(0)
                        # set every Customer's line position to the next one up and change their state
                        for i in range(0, len(customersWaiting)):
                            customersWaiting[i].state = "moving up in line"
                            customersWaiting[i].linePosition = LINE_POSITIONS[i]

                        # set customer in front of the line to next up
                        if len(customersWaiting) > 0:
                            currentCust = customersWaiting[0]
                        GameState = "PLAYING"

                
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
                    if currentCust != None and currentCust.state == "waiting":
                        register1.render(screen)
                    # 3. Draw the player last (on top of everything)
                    player.render(screen)


                if DebugMode == True:
                    for c in front_counters:
                        pygame.draw.rect(screen, (250, 0, 0), c)
                    pygame.draw.rect(screen, (255, 255, 0), register1.interactionZone, 3)
                    for c in front_collisions:
                        pygame.draw.rect(screen, (255, 255, 0), c, 2)

            elif CafeView == "MIDDLE":
                player.handle_movement(keys, middle_collisions)
                screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))

                for m in machines:
                    m.render(screen, debug=DebugMode)
                player.render(screen)
                if currentCust != None and currentCust.state == "waiting":
                    register2.render(screen)
                screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))

                for m in machines:
                    if m.is_player_nearby(player):
                        label = font.render(f"[E] {m.name}  ({m.state})", True, (255, 255, 255))
                        screen.blit(label, (m.rect.centerx - label.get_width() // 2, m.rect.top - 24))


                if DebugMode == True:
                    for c in middle_collisions:
                        pygame.draw.rect(screen, (255, 255, 0), c, 2)
                    for c in middle_counters:
                        pygame.draw.rect(screen, (250, 0, 0), c)
                    pygame.draw.rect(screen, (255, 255, 0), register2.interactionZone, 3)


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

            mx, my = pygame.mouse.get_pos()
            if player.ti_rect.collidepoint((mx, my)):
                inventory = font.render(f'{player.top_inventory}', True, (250, 0, 0))
                screen.blit(inventory, (mx+10, my))
            if player.bi_rect.collidepoint((mx, my)):
                inventory = font.render(f'{player.bottom_inventory}', True, (250, 0, 0))
                screen.blit(inventory, (mx+10, my))

            if DebugMode == True:
                pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

        elif GameState == "REGISTER":
            register1.take_order(screen)


        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, font)

        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        clock.tick(FPS)

        text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()} | GameState: {GameState}", True, (230, 230, 230))
        screen.blit(text, (10, 10))
        orders_text = font.render(f'Orders: {', '.join(o.name for o in orders_list)}', True, (250, 0, 0))
        screen.blit(orders_text, (10, 25))


        pygame.display.flip()

    pygame.quit()
    sys.exit()


# Finds first open seat in collisions list and returns it. None if all occupied

def findFirstOpen(seats):
    for c in seats:
        if isinstance(c, Seat) and c.state == "open":
            return c
    return None


def change_counters_pos(view):
    if view == "MIDDLE":
        c1.rect.x, c1.rect.y = 1014, 615
        c2.rect.x, c2.rect.y = 849, 615
        c3.rect.x, c3.rect.y = 685, 615
        c4.rect.x, c4.rect.y = 522, 615
        c5.rect.x, c5.rect.y = 357, 615
    elif view == "FRONT":
        c1.rect.x, c1.rect.y = 7, 487
        c2.rect.x, c2.rect.y = 172, 487
        c3.rect.x, c3.rect.y = 336, 487
        c4.rect.x, c4.rect.y = 500, 487
        c5.rect.x, c5.rect.y = 664, 487

if __name__ == "__main__":
    main()