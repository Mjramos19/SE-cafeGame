#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py
from backroom import *
from recipes import *
from classes import *
from machines import Machine
import constants
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

#Counter cup
counterCup = cup(780,525,20,20)

# builds all counters (about 165 apart from each other)
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = (Counter(7, 487), Counter(172, 487), Counter(336, 487),
                                           Counter(500, 487), Counter(664, 487), Counter(193, 234),
                                           Counter(358, 234), Counter(522, 234), Counter(686, 234), Counter(850, 234))

s1, s2, s3, s4, s5, s6 = Seat(38, 243), Seat(253, 243), Seat(445, 243), Seat(660, 243), Seat(850, 243), Seat(1064, 243)

doorEntry, doorEntry2 = DoorEntry(15, 345, 155, 50), DoorEntry(15, 718, 155, 50)


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
backroom_collisions = [stockingShelf(900, 200, 200, 500)]

#LAVISHA Three machines placed at the back-counter positions (matching c6, c7, c8 widths: 150x90)
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
    #LAVISHA
    active_machine = None


    # Other entities (Customers)
    customers = []
    customersWaiting = []
    ingredientBoxes = [None, None, None, None]
    numBoxes = 0

    # Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player")
    all_sprites.add(player)

    # orders list
    orders = []


    running = True
    while running:
        # These are universal events no matter the state

        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEMOTION and DebugMode==True:
                m_x, m_y = getMousePos()[0], getMousePos()[1]
                print(f"Mouse position: X={m_x}, Y={m_y}")

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.selectedSlot = 0
                elif event.key == pygame.K_2:
                    player.selectedSlot = 1
                elif event.key == pygame.K_3:
                    player.selectedSlot = 2
                elif event.key == pygame.K_4:
                    player.selectedSlot = 3

                elif event.key == pygame.K_0:
                    if DebugMode == False:
                        DebugMode = True
                    else:
                        DebugMode = False

                elif event.key == pygame.K_r:  # R clears the customers for testing
                    customers.clear()

                elif event.key == pygame.K_q and GameState=="PLAYING":
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        change_counters_pos(CafeView)
                    else:
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        change_counters_pos(CafeView)

                # if player presses e inside registers collision zone, and there is a customer, take order
                elif event.key == pygame.K_e:
                    if player.get_foot_rect().colliderect(register1.interactionZone) and register1.customerWaiting:
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(register2.interactionZone) and register2.customerWaiting:
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(doorEntry) and GameState == "PLAYING" and CafeView == "MIDDLE":
                        GameState = "BACKROOM"
                        player.rect.x, player.rect.y = 30, 490
                    elif player.get_foot_rect().colliderect(doorEntry2) and GameState == "BACKROOM":
                        GameState = "PLAYING"
                        player.rect.x, player.rect.y = 30, 115

#LAVISHA - if player presses e near a machine, open machine UI. If they press e again while in the machine UI, run the machine or collect output depending on the state. Pressing escape will exit the machine UI.
                    elif CafeView == "MIDDLE" and GameState == "PLAYING":
                        for m in machines:
                            if m.is_player_nearby(player):
                                active_machine = m
                                GameState = "MACHINE"
                                break
                    
                    elif GameState == "MACHINE" and active_machine:
                        if active_machine.state == "full":
                            active_machine.run_machine()
                        elif active_machine.state == "ready":
                            result = active_machine.remove_output()
                            if result:
                                print(f"Collected: {result.name}")
                            if not active_machine.contents:
                                active_machine.state = "empty"
                    
                    #checking if e was pressed in any backroom box collision zones
                    elif GameState == "BACKROOM":
                        for i in range(len(ingredientBoxes)):
                            #Finds each ingredient box instance and checks for collision with interactionZone
                            if ingredientBoxes[i] != None:
                                if player.get_foot_rect().colliderect(ingredientBoxes[i].interactionZone):
                                    #grabs corresponding box and adds it to first open hot bar slot
                                    for j in range(len(player.inventory)):
                                        if player.inventory[j] == None:
                                            player.inventory[j] = ingredientBoxes[i]
                                            ingredientBox.popBox(ingredientBoxes[i], ingredientBoxes, backroom_collisions)
                                            numBoxes -= 1
                                            break
                                
                elif event.key == pygame.K_ESCAPE:
                    if GameState == "REGISTER":
                        GameState = "PLAYING"
                    elif GameState == "MACHINE":
                        GameState = "PLAYING"
                        active_machine = None

                elif event.key == pygame.K_s and GameState == "REGISTER":

                    orders.insert(0, currentCust.orderedItem)
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
                        cup.cupToInventory(player)

            #If player presses mouse button in backroom, check if cursor is over shelf spot with ingredient object selected
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if GameState == "BACKROOM":
                    #loops through all backroom objects looking for shelves
                    for obj in backroom_collisions:
                        if isinstance(obj, stockingShelf):
                            #if player is standing in shelf interaction zone and clicks on shelf spot with item in hand, attempt to place it
                            if player.get_foot_rect().colliderect(obj.interactionZone) and player.inventory[player.selectedSlot] != None:
                                if event.button == 1:
                                    for shelfSpot in obj.spots:
                                        if shelfSpot.rect.collidepoint(getMousePos()):
                                            shelfSpot.storeIngredientBox(player.inventory[player.selectedSlot], player)
                                
            # if wait line is not current full and total customers not at max, spawn new customer
            elif event.type == SPAWN_EVENT:

                if len(customers) < MAX_CUSTOMERS and len(customersWaiting) < MAX_CUSTOMERS_WAITING:

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
                
                #if ingredient spots open, spawn random ingredient box
                if numBoxes < MAX_INGREDIENT_BOXES:
                    for i in range(MAX_INGREDIENT_BOXES):
                        if ingredientBoxes[i] == None:
                            x, y = BOX_POSITIONS[i]
                            ingredBox = ingredientBox(x, y, "INGREDIENT")
                            ingredientBoxes[i] = ingredBox
                            backroom_collisions.append(ingredBox)
                            numBoxes += 1
                            break
                ''' #Calc index spot position
                    spotIndex = len(ingredientBoxes)

                    #grab box position based on which number in box line
                    x, y = BOX_POSITIONS[spotIndex]

                    #make box object with placeholder "INGREDIENTs"
                    ingredBox = ingredientBox(x, y, "INGREDIENT")

                    #add to list of boxes
                    ingredientBoxes.append(ingredBox)
                    backroom_collisions.append(ingredBox)
                    numBoxes += 1'''


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
                pygame.draw.rect(screen, (255, 255, 255), counterCup)
                
                drawHotBar(player.inventory, player.selectedSlot, font)

            elif CafeView == "MIDDLE":

                player.handle_movement(keys, middle_collisions)
                screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))
                #LAVISHA - render machines and interaction prompts if player is nearby
                for m in machines:
                    m.render(screen, debug=DebugMode)
                player.render(screen)
                if currentCust != None and currentCust.state == "waiting":
                    register2.render(screen)
                screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))
                pygame.draw.rect(screen, (255, 255, 0), doorEntry, 2)

#LAVISHA - render machines and interaction prompts if player is nearby
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
                
                drawHotBar(player.inventory, player.selectedSlot, font)


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

        #LAVISHA - if in machine UI, render the machine's mini-game mode (which will display prompts based on state and allow player to interact with it using e and escape)
        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, font)
        
        elif GameState == "BACKROOM":
            player.handle_movement(keys, backroom_collisions)
            
            screen.fill((0,0,0))

            for c in backroom_collisions:
                c.render(screen)
                if isinstance(c, stockingShelf):
                    pygame.draw.rect(screen, (255, 255, 0), c.interactionZone, 2)
            
            pygame.draw.rect(screen, (255, 255, 0), doorEntry2, 2)

            player.render(screen)

            drawHotBar(player.inventory, player.selectedSlot, font)

        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        '''if RecipeView == RECIPE_VIEW_MENU:
            screen.fill(UI_BG_COLOR)
            x = RECIPE_START_X
            y = RECIPE_START_Y
            
            for recipe in RECIPES_UNLOCKED:
				recipe_img = constants.IMAGE_LIBRARY.get(recipe)
				if recipe_img:
					recipe_img = pygame.transform.smoothscale(
						recipe_img, RECIPE_ICON_SIZE
					)
					screen.blit(recipe_img, (x, y))

				x += RECIPE_ICON_SIZE[0] + RECIPE_ICON_PADDING
            '''
        clock.tick(FPS)

        text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()}", True, (230, 230, 230))
        screen.blit(text, (10, 10))
        orders_text = font.render(f'Orders: {orders}', True, (250, 0, 0))
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
    

#helper function for generating the hot bar
def drawHotBar(playerInventory, selectedSlot, font):
    for i in range(NUM_SLOTS):
        #makes rectangle object for that inventory slot at corresponding inventory position
        slot = pygame.Rect(INVENTORY_POSITIONS[i][0], INVENTORY_POSITIONS[i][1] ,SLOT_SIZE, SLOT_SIZE)

        #draws the grey slot background at that spot
        pygame.draw.rect(screen, (40, 40, 40), slot)

        #if that inventory slot has an item, draw that icon inside
        if playerInventory[i] != None:
            #placeholder for item pictures
            tempItemPic = pygame.Rect(slot.center[0], slot.center[1], 10, 10)
            pygame.draw.rect(screen, (255, 0, 0), tempItemPic)

        #if that inventory slot is selected, draw thick white border, else: draw thin black border
        if i == selectedSlot:
            pygame.draw.rect(screen, (255, 255, 255), slot, 3)
        else:
            pygame.draw.rect(screen, (0, 0, 0), slot, 2)
        
        #if the players mouse is hovering over a slot that isn't empty, display that items name next to the slot
        if slot.collidepoint(getMousePos()):
            if playerInventory[i] != None:
                screen.blit(font.render(f'{playerInventory[i]}', True, (250, 0, 0)), (slot.x + 60, slot.y + 15))
        

#helper function to get mouse position
def getMousePos():
    return pygame.mouse.get_pos()

if __name__ == "__main__":
    main()