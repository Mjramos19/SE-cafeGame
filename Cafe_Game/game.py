#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py

from classes import *
from machines import *
import constants
from recipes import *
from constants import *

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
constants.IMAGE_LIBRARY["hotwm_red"] = pygame.image.load("Cafe_Game_Art/hot_water_machine_red.png").convert_alpha()
constants.IMAGE_LIBRARY["hotwm_green"] = pygame.image.load("Cafe_Game_Art/hot_water_machine_green.png").convert_alpha()
constants.IMAGE_LIBRARY["hotwm_yellow"] = pygame.image.load("Cafe_Game_Art/hot_water_machine_yellow.png").convert_alpha()
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
constants.IMAGE_LIBRARY["hotwm_red"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["hotwm_red"], ((412, 488)))
constants.IMAGE_LIBRARY["hotwm_green"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["hotwm_green"], ((412, 488)))
constants.IMAGE_LIBRARY["hotwm_yellow"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["hotwm_yellow"], ((412, 488)))
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

#grinder        = Machine(193, 234, "Coffee Grinder",   bag_coffee_beans, [ground_coffee],            1, 3)
#espresso_mach  = Machine(358, 234, "Espresso Machine", ground_coffee,    [espresso_shot],            1, 5)
#steamer        = Machine(0, 0, "Milk Steamer",     milk,             [steamed_milk, foamed_milk], 1, 4)

hot_water_m    = Machine(522, 234, "Hot Water Machine", water, [hot_water], 2, 4, ["hotwm_red", "hotwm_yellow", "hotwm_green"])
#machines = [grinder, espresso_mach, steamer]
machines = [hot_water_m]


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

    # Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player")
    all_sprites.add(player)

    """for testing the minigame mode I'm defaulting the player with water"""
    player.bottom_inventory.append(water)
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
                print(f"Mouse position: X={m_x}, Y={m_y}")
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
                        # i need to handle the active ingredient from the players inventory, assign that as a variable, then put that into minigamemode() not player.bottom
                        # then i can remove the ingredient after it is used
                        active_machine.add(active_machine.ingredient)



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
                            active_machine.setup_minigame(player.bottom_inventory[0])
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
                            player.top_inventory.append(result)
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
                spawn_x, spawn_y = base_x - 60, base_y - 64

                currCustomer = Customer(spawn_x, spawn_y, ["ladybug_idle", "ladybug_sitting"], RECIPES_UNLOCKED, linePosition=LINE_POSITIONS[index])

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
                front_view_rendering(player, customers, font, keys, DebugMode)
            elif CafeView == "MIDDLE":
                middle_view_rendering(player, font, keys, DebugMode)
            else:
                back_view_rendering(player, font, keys, DebugMode)

            '''these things run while playing'''
            for c in customers:
                c.update(seats)

            mx, my = pygame.mouse.get_pos()
            if player.ti_rect.collidepoint((mx, my)):
                inventory = font.render(f'{', '.join(item.name for item in player.top_inventory)}', True, (250, 0, 0))
                screen.blit(inventory, (mx+10, my))
            if player.bi_rect.collidepoint((mx, my)):
                inventory = font.render(f'{', '.join(item.name for item in player.bottom_inventory)}', True, (250, 0, 0))
                screen.blit(inventory, (mx+10, my))


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


def middle_view_rendering(player, font, keys, DebugMode):
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
        pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

def back_view_rendering(player, font, keys, DebugMode):
    player.handle_movement(keys, back_collisions)
    screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))
    player.render(screen, DebugMode)
    screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))
    if DebugMode == True:
        for c in back_collisions:
            pygame.draw.rect(screen, (255, 255, 0), c, 2)
        for c in middle_counters:
            pygame.draw.rect(screen, (250, 0, 0), c)
        pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

if __name__ == "__main__":
    main()