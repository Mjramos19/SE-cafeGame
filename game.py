#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py

from classes import *
from machines import *
import constants
from recipes import *
from constants import *
from backroom import *

pygame.init()
screen = pygame.display.set_mode((1366, 768))

constants.IMAGE_LIBRARY["player"] = pygame.image.load("Cafe_Game_Art/player.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_idle"] = pygame.image.load("Cafe_Game_Art/ladybug_idle.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_sitting"] = pygame.image.load("Cafe_Game_Art/ladybug_sitting.png").convert_alpha()
constants.IMAGE_LIBRARY["order_screen"] = pygame.image.load("Cafe_Game_Art/order_screen.png").convert()
constants.IMAGE_LIBRARY["bg1"] = pygame.image.load("Cafe_Game_Art/cafe_bg.png").convert_alpha()
constants.IMAGE_LIBRARY["bg1_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_top.png").convert_alpha()
constants.IMAGE_LIBRARY["bg2"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2.png").convert()
constants.IMAGE_LIBRARY["bg2_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2_top.png").convert_alpha()
constants.IMAGE_LIBRARY["register_icon"] = pygame.image.load("Cafe_Game_Art/register_icon.png").convert_alpha()
constants.IMAGE_LIBRARY["minigame_bg"] = pygame.image.load("Cafe_Game_Art/minigame background.png").convert()

# All Machine Images
constants.IMAGE_LIBRARY["cg_empty"] = pygame.image.load("Cafe_Game_Art/CGEmpty-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["cg_ready"] = pygame.image.load("Cafe_Game_Art/CGFull-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["cg_inprogress"] = pygame.image.load("Cafe_Game_Art/CGInprogress-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["em_empty"] = pygame.image.load("Cafe_Game_Art/EMempty.png").convert_alpha()
constants.IMAGE_LIBRARY["em_inprogress"] = pygame.image.load("Cafe_Game_Art/EMinprogress.png").convert_alpha()
constants.IMAGE_LIBRARY["em_ready"] = pygame.image.load("Cafe_Game_Art/EMready.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_empty"] = pygame.image.load("Cafe_Game_Art/WBempty.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_inprogress"] = pygame.image.load("Cafe_Game_Art/WBinprogress.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_ready"] = pygame.image.load("Cafe_Game_Art/WBready.png").convert_alpha()

# All Ingredient Images
constants.IMAGE_LIBRARY["water"] = pygame.image.load("Cafe_Game_Art/water.png").convert_alpha()

# Pre-scale all images in the library them once
constants.IMAGE_LIBRARY["player"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player"], (120, 268))
constants.IMAGE_LIBRARY["ladybug_idle"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["ladybug_idle"], (120, 268))
constants.IMAGE_LIBRARY["ladybug_sitting"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["ladybug_sitting"], (101, 180))
constants.IMAGE_LIBRARY["order_screen"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["order_screen"], (1366, 768))
constants.IMAGE_LIBRARY["bg1"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1"], (1366, 768))
constants.IMAGE_LIBRARY["bg1_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1_top"], (1366, 768))
constants.IMAGE_LIBRARY["bg2"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2"], (1366, 768))
constants.IMAGE_LIBRARY["bg2_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2_top"], (1366, 768))
constants.IMAGE_LIBRARY["register_icon"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["register_icon"], ((17*2), (33*2)))
constants.IMAGE_LIBRARY["minigame_bg"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["minigame_bg"], (1366, 768))
constants.IMAGE_LIBRARY["cg_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_empty"], (150, 200))
constants.IMAGE_LIBRARY["cg_ready"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_ready"], (150, 200))
constants.IMAGE_LIBRARY["cg_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_inprogress"], (150, 200))
constants.IMAGE_LIBRARY["em_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_empty"], (150, 200))
constants.IMAGE_LIBRARY["em_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_inprogress"], (150, 200))
constants.IMAGE_LIBRARY["em_ready"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_ready"], (150, 200))
constants.IMAGE_LIBRARY["wb_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_empty"], (130, 200))
constants.IMAGE_LIBRARY["wb_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_inprogress"], (130, 200))
constants.IMAGE_LIBRARY["wb_ready"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_ready"], (130, 200))
constants.IMAGE_LIBRARY["water"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["water"], ((348, 330)))

# Defines all ingredients
bag_coffee_beans = Ingredient("Coffee Beans", ["water"], 18.35, 56)
ground_coffee = Ingredient("Ground Coffee",["water"])
espresso_shot = Ingredient("Espresso Shot",["water"])
espresso_doubleShot = Ingredient("Espresso Double Shot",["water"])
water = Ingredient("Water",["water"])
hot_water = Ingredient("Hot Water",["water"])
ice = Ingredient("Ice",["water"])
milk = Ingredient("Milk",["water"], 3.28, 16)
steamed_milk = Ingredient("Steamed Milk",["water"])
foamed_milk = Ingredient("Foamed Milk",["water"])
cocoa_powder = Ingredient("Cocoa Powder",["water"], 9.40, 64)
hot_chocolate = Ingredient("Hot Chocolate",["water"])

# Ingredients List
INGREDIENTS = [bag_coffee_beans, ground_coffee, espresso_shot, water, hot_water, ice, milk, steamed_milk, foamed_milk, cocoa_powder, hot_chocolate]

# Defines all Recipes
Espresso = Recipe("Espresso Shot" ,[espresso_shot],6.50, "N/A", False)
Iced_Coffee = Recipe("Iced Coffee" ,[espresso_shot, ice],6.50, "N/A", False)
Americano = Recipe("Americano" ,[hot_water, espresso_shot],6.50, "N/A", False)
Latte = Recipe("Latte" ,[espresso_shot, steamed_milk],6.50, "N/A")
Iced_Latte = Recipe("Iced Latte" ,[espresso_shot, ice, milk],6.50, "N/A")

# Recipes Lists
ALL_RECIPES = [Espresso, Iced_Coffee, Americano, Latte, Iced_Latte]
RECIPES_UNLOCKED = []


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

s1, s2, s3, s4, s5, s6 = Seat(57, 243, 1), Seat(252, 243, 2), Seat(464, 243, 3), Seat(660, 243, 4), Seat(869, 243, 5), Seat(1064, 243, 6)

# Backroom door objects
doorEntry, doorEntry2 = DoorEntry(15, 345, 155, 50), DoorEntry(15, 718, 155, 50)

# build two registers - one for customers, the other dependent on the first and will display icon, can take order from both and will update the other
register1 = Register(829, 487, 110)
register2 = Register(193, 615, 10)

currentCust = None
currCustomer = None


# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
backroom_collisions = [stockingShelf(1200, 200, 100, 500)]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
seats = [s1, s2, s3, s4, s5, s6]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, register2]
backroom_shelves = []

grinder        = Machine(193, 234, "Coffee Grinder",   bag_coffee_beans, [ground_coffee],            1, 3, ["cg_empty", "cg_inprogress", "cg_ready"])
espresso_mach  = Machine(358, 234, "Espresso Machine", ground_coffee,    [espresso_shot],            1, 5, ["em_empty","em_inprogess", "em_ready"])
water_boiler   =  Machine(520, 234, "Water Boiler",     water,             [hot_water], 1, 4, ["wb_empty","wb_inprogress","wb_ready"])

machines = [grinder, espresso_mach, water_boiler]


def main():
    global Customer, currentCust
    pygame.display.set_caption("Cafe Sim")
    font = pygame.font.SysFont(None, 22)
    clock_font = pygame.font.SysFont(None, 45)
    clock = pygame.time.Clock()
    seconds_per_frame = TIME_SPEED / 60
    game_seconds = 21600  # Start day at 6:00 AM

    DebugMode = True

    GameState = "PLAYING"
    CafeView = "FRONT"

    active_machine = None

    # Other entities (Customers)
    customers = []
    customersWaiting = []
    ingredientBoxes = []

    # Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player")
    all_sprites.add(player)

    """for testing the minigame mode I'm defaulting the player with water"""
    player.inventory[0] = water
    is_dragging = False

    # orders list
    orders_list = []

    for recipe in ALL_RECIPES:
        if recipe.locked == False:
            RECIPES_UNLOCKED.append(recipe)


    running = True
    while running:
        # These are universal events no matter the state

        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        m_x, m_y = pygame.mouse.get_pos()

        game_seconds += seconds_per_frame
        if game_seconds >= REAL_DAY_SEC:
            game_seconds = 0
        hours = int(game_seconds // 3600)
        minutes = int((game_seconds % 3600) // 60)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEMOTION and DebugMode==True:
                #print(f"Mouse position: X={m_x}, Y={m_y}")
                pass

            if event.type == pygame.MOUSEBUTTONDOWN and GameState == "MACHINE":
                if active_machine.start_button != None:
                    if active_machine.start_button.collidepoint((m_x, m_y)) and event.button == 1:
                        # here is where any logic for different outputs would be handled. we can have two start buttons,
                        # have right-click be output 2 ( run_machine(1) ), etc.
                        if active_machine.state == "full":
                            active_machine.run_machine()
                        elif active_machine.state == "empty":
                            active_machine.state = "error"
                            active_machine.error_start = pygame.time.get_ticks()

                    if active_machine.ingredient and active_machine.ingredient_rect.collidepoint((m_x, m_y)):
                        is_dragging = True

            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                if active_machine and active_machine.ingredient and (active_machine.state == "empty" or active_machine.state == "error"):
                    if active_machine.mg_interaction_zone.colliderect(active_machine.ingredient_rect):
                        active_machine.add(active_machine.ingredient)
                        '''
                        if active_machine.add(active_machine.ingredient) == True:
                            player.inventory[player.selectedSlot] = None'''


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    player.selectedSlot = 0
                elif event.key == pygame.K_2:
                    player.selectedSlot = 1
                elif event.key == pygame.K_3:
                    player.selectedSlot = 2
                elif event.key == pygame.K_4:
                    player.selectedSlot = 3

                if event.key == pygame.K_0:
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
                    elif player.rect.colliderect(register2.interactionZone) and register2.customerWaiting:
                        GameState = "REGISTER"
                    elif player.rect.colliderect(doorEntry) and GameState == "PLAYING" and CafeView == "MIDDLE":
                        CafeView = "BACKROOM"
                        player.rect.x, player.rect.y = 30, 490
                    elif player.rect.colliderect(doorEntry2) and CafeView == "BACKROOM":
                        GameState = "PLAYING"
                        player.rect.x, player.rect.y = 30, 115

                    elif GameState == "MACHINE" and active_machine:
                        if active_machine.state == "ready":
                            result = active_machine.remove_output()
                            if result:
                                print(f"Collected: {result.name}")
                                player.inventory.append(result)
                            if not active_machine.contents:
                                active_machine.state = "empty"

                    elif CafeView == "MIDDLE" and GameState == "PLAYING":
                        for m in machines:
                            if m.is_player_nearby(player):
                                active_machine = m
                                active_machine.setup_minigame(player.inventory[player.selectedSlot])
                                GameState = "MACHINE"
                                break

                    #checking if e was pressed in any backroom box collision zones
                    elif GameState == "BACKROOM":
                        for i in range(len(ingredientBoxes)):
                            if player.rect.colliderect(ingredientBoxes[i].interactionZone):
                                #grabs corresponding box and adds it to first open hot bar slot
                                for j in range(len(player.inventory)):
                                    if player.inventory[j] == None:
                                        player.inventory[j] = ingredientBoxes[i]
                                        print(player.inventory)
                                        break

                if event.key == pygame.K_ESCAPE:
                    if GameState == "MACHINE":
                        active_machine = None
                    GameState = "PLAYING"


                if event.key == pygame.K_s and GameState == "REGISTER":
                    if currentCust is None:
                        return

                    orders_list.insert(0, currentCust.orderedItem)
                    time.sleep(1) # will need to be updated so the whole game doesn't pause

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


            if event.type == SPAWN_EVENT:
                # if wait line is not current full and total customers not at max, spawn new customer
                if len(customers) < MAX_CUSTOMERS and len(customersWaiting) < MAX_CUSTOMERS_WAITING:

                    # Calculate the index for the new customer
                    index = len(customersWaiting)
                    base_x, base_y = LINE_POSITIONS[index]

                    # Center the spawn coordinates
                    spawn_x = base_x - 60
                    spawn_y = base_y - 64

                    # Create the customer using the key "customer" from your IMAGE_LIBRARY
                    currCustomer = Customer(spawn_x, spawn_y, ["ladybug_idle", "ladybug_sitting"], RECIPES_UNLOCKED,
                                            linePosition=LINE_POSITIONS[index])

                    if index == 0:
                        currentCust = currCustomer

                    all_sprites.add(currCustomer)
                    customer_group.add(currCustomer)

                    # Add to tracking lists
                    customers.append(currCustomer)
                    customersWaiting.append(currCustomer)
                    register1.setWaiting()

                # if ingredient spots open, spawn random ingredient box
                if len(ingredientBoxes) < MAX_INGREDIENT_BOXES:
                    # Calc index spot position
                    spotIndex = len(ingredientBoxes)

                    # grab box position based on which number in box line
                    x, y = BOX_POSITIONS[spotIndex]

                    # make box object with placeholder "INGREDIENTs"
                    ingredBox = ingredientBox(x, y, "INGREDIENT")

                    # add to list of boxes
                    ingredientBoxes.append(ingredBox)
                    backroom_collisions.append(ingredBox)


        if GameState == "PLAYING":
            if CafeView == "FRONT":
                front_view_rendering(player, customers, font, keys, DebugMode)
            elif CafeView == "MIDDLE":
                middle_view_rendering(player, font, keys, DebugMode)
            else:
                back_view_rendering(player, font, keys, DebugMode)

            '''these things run while playing'''
            for c in customers:
                c.update(seats)

        elif GameState == "REGISTER":
            register1.take_order(screen)

        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, DebugMode)
            if is_dragging:
                active_machine.ingredient_rect.center = (m_x, m_y)
                active_machine.ingredient.x = active_machine.ingredient_rect.x
                active_machine.ingredient.y = active_machine.ingredient_rect.y


        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        clock.tick(FPS)

        # Handles all text rendering
        text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()} | GameState: {GameState}", True, (230, 230, 230))
        orders_text = font.render(f'Orders: {', '.join(o.name for o in orders_list)}', True, (250, 0, 0))
        clock_text = clock_font.render(handle_time(hours, minutes), True, 'black')
        screen.blit(text, (10, 10))
        screen.blit(orders_text, (10, 25))
        screen.blit(clock_text, (1202, 35))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


def handle_time(hrs, mins):
    """Takes in the game's hours and minutes and converts them to follow standard clock rules while on a 5 minutes interval."""
    meridiem = "PM" if hrs >= 12 else "AM"
    new_hours = hrs % 12
    if new_hours == 0:
        new_hours = 12
    new_mins = (mins // 5) * 5 #rounds down to nearest 5 minutes
    return f'{new_hours:02d}:{new_mins:02d} {meridiem}'


def findFirstOpen(seats):
    """Finds first open seat in collisions list and returns it. None if all occupied."""
    for c in seats:
        if isinstance(c, Seat) and c.state == "open":
            return c
    return None

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


def front_view_rendering(player, customers, font, keys, DebugMode):
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
            pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

        drawHotBar(player.inventory, player.selectedSlot, font)


def middle_view_rendering(player, font, keys, DebugMode):
    player.handle_movement(keys, middle_collisions)
    screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))

    if DebugMode == True:
        for c in middle_collisions:
            pygame.draw.rect(screen, (255, 255, 0), c, 2)
        for c in middle_counters:
            pygame.draw.rect(screen, (250, 0, 0), c)
        pygame.draw.rect(screen, (255, 255, 0), register2.interactionZone, 3)
        pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)
        pygame.draw.rect(screen, (255, 255, 0), doorEntry, 2)

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

    drawHotBar(player.inventory, player.selectedSlot, font)

def back_view_rendering(player, font, keys, DebugMode):

    player.handle_movement(keys, backroom_collisions)
    screen.fill((0, 0, 0))
    for c in backroom_collisions:
        c.render(screen)
        if isinstance(c, stockingShelf):
            pygame.draw.rect(screen, (255, 255, 255), c.interactionZone, 2)

    pygame.draw.rect(screen, (255, 255, 0), doorEntry2, 2)
    player.render(screen)
    drawHotBar(player.inventory, player.selectedSlot, font)

    if DebugMode == True:
        for c in backroom_collisions:
            pygame.draw.rect(screen, (255, 255, 0), c, 2)
        pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

if __name__ == "__main__":
    main()
