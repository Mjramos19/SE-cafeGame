#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py

from classes import *
from machines import *
import constants
from recipes import *
from constants import *
from backroom import *
from button import *

pygame.init()
screen = pygame.display.set_mode((1366, 768))

constants.IMAGE_LIBRARY["player_idle_front"] = pygame.image.load("Cafe_Game_Art/player_idle_front.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_idle"] = pygame.image.load("Cafe_Game_Art/ladybug_idle.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_sitting"] = pygame.image.load("Cafe_Game_Art/ladybug_sitting.png").convert_alpha()
constants.IMAGE_LIBRARY["order_screen"] = pygame.image.load("Cafe_Game_Art/order_screen.png").convert()
constants.IMAGE_LIBRARY["bg1"] = pygame.image.load("Cafe_Game_Art/cafe_bg.png").convert_alpha()
constants.IMAGE_LIBRARY["bg1_top"] = pygame.image.load("Cafe_Game_Art/cafe_bg_top.png").convert_alpha()
constants.IMAGE_LIBRARY["bg2"] = pygame.image.load("Cafe_Game_Art/cafe_bg_2.png").convert()
constants.IMAGE_LIBRARY["bg2_top"] = pygame.image.load("Cafe_Game_Art/bg2_top.png").convert_alpha()
constants.IMAGE_LIBRARY["register_icon"] = pygame.image.load("Cafe_Game_Art/register_icon.png").convert_alpha()
constants.IMAGE_LIBRARY["minigame_bg"] = pygame.image.load("Cafe_Game_Art/minigame_bg.png").convert()

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
constants.IMAGE_LIBRARY["coffee_beans"] = pygame.image.load("Cafe_Game_Art/coffee_beans.png").convert_alpha()
#constants.IMAGE_LIBRARY["ground_coffee"] = pygame.image.load("Cafe_Game_Art/ground_coffee.png").convert_alpha()
#constants.IMAGE_LIBRARY["espresso_shot"] = pygame.image.load("Cafe_Game_Art/espresso_shot.png").convert_alpha()

# All Recipes Images


# Pre-scale all images in the library them once
constants.IMAGE_LIBRARY["player_idle_front"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player_idle_front"], (120, 268))
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
constants.IMAGE_LIBRARY["coffee_beans"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["coffee_beans"], ((348, 330)))

# Defines all ingredients
bag_coffee_beans = Ingredient("Coffee Beans", ["coffee_beans"], 18.35, 56)
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


# Front room collision rects
counter3_rect = pygame.Rect(0, 590, 983, 50)
wall_rect2 = pygame.Rect(0, 293, 1400, 10)

# Behind counter / middle collision rects
counter1_rect = pygame.Rect(187, 336, 983, 50)
counter2_rect = pygame.Rect(187, 718, 983, 50)
wall_rect = pygame.Rect(0, 333, 1400, 10)
menu_rect = pygame.Rect(1150, 0, 100, 800)

# Builds all counters (about 165 apart from each other)
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = (Counter(7, 487), Counter(172, 487), Counter(336, 487),
                                           Counter(500, 487), Counter(664, 487), Counter(193, 234),
                                           Counter(358, 234), Counter(522, 234), Counter(686, 234), Counter(850, 234))
# Builds all seats for the customers
s1, s2, s3, s4, s5, s6 = Seat(57, 243, 1), Seat(252, 243, 2), Seat(464, 243, 3), Seat(660, 243, 4), Seat(869, 243, 5), Seat(1064, 243, 6)

# Builds Backroom door objects
doorEntry, doorEntry2 = DoorEntry(15, 345, 155, 50), DoorEntry(15, 718, 155, 50)

# build two registers - one for customers, the other dependent on the first and will display icon, can take order from both and will update the other
register1 = Register(829, 487, 110)
register2 = Register(193, 615, 10)

counterCup = Cup(780,525,20,20)

currentCust = None
currCustomer = None
current_screen = "game"

# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
backroom_collisions = [stockingShelf(900, 200, 200, 500)]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
seats = [s1, s2, s3, s4, s5, s6]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, register2]
backroom_shelves = []

grinder        = Machine(193, 234, "Coffee Grinder",   bag_coffee_beans, [ground_coffee], 1, 3, ["cg_empty", "cg_inprogress", "cg_ready"])
espresso_mach  = Machine(358, 234, "Espresso Machine", ground_coffee,    [espresso_shot], 1, 5, ["em_empty","em_inprogess", "em_ready"])
water_boiler   =  Machine(520, 234, "Water Boiler",     water,             [hot_water], 1, 4, ["wb_empty","wb_inprogress","wb_ready"])

machines = [grinder, espresso_mach, water_boiler]

SHOP_VIEW_NONE = None
SHOP_VIEW_MENU = "MENU"
recipe_button = Button(1190, 342, 160, 78, "Recipes", "RECIPE_MENU", None)
shop_button = Button(1190, 468, 160, 78, "Shop", "SHOP_MENU", None)
# Corner prompt zone for switching cafe view
switch_view_prompt_rect_cafe = pygame.Rect(1025, 675, 100, 100)
switch_view_prompt_rect_middle = pygame.Rect(50, 675, 100, 100)


class GameManager:
    """
    Holds game-wide progression and UI state.

    This keeps economy, orders, messages, and placeholder upgrade/shop
    data together without changing the gameplay loop structure too much.
    """
    def __init__(self):
        """Initialize the shared game state."""
        self.message = ""
        self.message_timer = 0
        self.machine_loaded_slot = None
        self.money = 0

        # Placeholder progression systems for Phase 3
        self.upgrades = [
            {"name": "Faster Grinder", "cost": 25, "purchased": False},
            {"name": "Recipe Unlock", "cost": 40, "purchased": False},
            {"name": "Cafe Decor", "cost": 15, "purchased": False},
        ]

    def set_message(self, text, duration_ms=1500):
        """
        Set a temporary on-screen message.

        Parameters:
            text (str): The message to display.
            duration_ms (int): How long to show the message in milliseconds.
        """
        self.message = text
        self.message_timer = pygame.time.get_ticks() + duration_ms

    def update_message(self):
        """
        Clear the current message once its timer expires.
        """
        current_time = pygame.time.get_ticks()
        if self.message != "" and current_time >= self.message_timer:
            self.message = ""

    def first_empty_order_slot(self):
        """
        Return the index of the first empty order slot.

        Returns:
            int | None: The first empty slot index, or None if all are occupied.
        """
        for i in range(len(self.active_orders)):
            if self.active_orders[i] is None:
                return i
        return None

    def serve_customer(self, customer):
        """
        Attempt to serve the selected cup to the given customer.

        Correct serves resolve the order.
        Incorrect serves still consume the cup and make the customer leave.
        """
        if customer is None:
            return

        cup = self.inventory.get_selected_cup()

        if cup is None:
            self.set_message("Select a cup first")
            return

        if customer.order is None:
            return

        # Determine if the serve is correct.
        if cup.is_empty():
            result = "incorrect"
        elif cup.contents == customer.order.drink_name:
            result = "correct"
        else:
            result = "incorrect"

        # Remove the cup entirely from the selected inventory slot.
        if self.inventory.selected_slot is not None:
            self.inventory.remove_cup(self.inventory.selected_slot)
            self.inventory.selected_slot = None

        # Determine payout
        if result == "correct":
            self.money += 5
            self.set_message("Served Correctly: +$5")
        else:
            self.set_message("Incorrect Serve")

            # Mark the order as resolved.
        customer.order.mark_resolved()

        # Start the short drinking phase.
        customer.start_drinking(result)

    def clear_round_state(self):
        """
        Reset lightweight gameplay state used during testing.
        """
        self.inventory.clear_all()
        self.machine_loaded_slot = None
        self.message = ""
        self.message_timer = 0

    def buy_upgrade(self, upgrade_index):
        """
        Attempt to buy a placeholder upgrade.

        Parameters:
            upgrade_index (int): The index of the upgrade in the list.
        """
        if not (0 <= upgrade_index < len(self.upgrades)):
            return

        upgrade = self.upgrades[upgrade_index]

        if upgrade["purchased"]:
            self.set_message("Already purchased")
            return

        if self.money < upgrade["cost"]:
            self.set_message("Not enough money")
            return

        self.money -= upgrade["cost"]
        upgrade["purchased"] = True
        self.set_message(f"Purchased {upgrade['name']}")

    def handle_time(self, hrs, mins):
        """Takes in the game's hours and minutes and converts them to follow standard clock rules while on a 5 minutes interval."""
        meridiem = "PM" if hrs >= 12 else "AM"
        new_hours = hrs % 12
        if new_hours == 0:
            new_hours = 12
        new_mins = (mins // 5) * 5  # rounds down to nearest 5 minutes
        return f'{new_hours:02d}:{new_mins:02d} {meridiem}'

    def findFirstOpen(self, seats):
        """Finds first open seat in collisions list and returns it. None if all occupied."""
        for c in seats:
            if isinstance(c, Seat) and c.state == "open":
                return c
        return None

    def get_nearby_seated_customer(self, player, customers):
        """
        Return the first seated customer close enough to serve.

        Uses the same general 'nearby interaction' style as machines.
        """
        for customer in customers:
            if customer.state == "seated":
                interaction_rect = customer.rect.inflate(20, 20)
                if player.rect.colliderect(interaction_rect):
                    return customer
        return None

    def cleanup_gone_customers(self, customers, customersWaiting, all_sprites, customer_group, manager):
        """
        Remove customers that have fully left the cafe.

        Also remove their resolved order cards once they are gone.
        """
        global currentCust

        gone_customers = [c for c in customers if c.state == "gone"]

        for customer in gone_customers:
            if customer in customers:
                customers.remove(customer)

            if customer in customersWaiting:
                customersWaiting.remove(customer)

            if customer in all_sprites:
                all_sprites.remove(customer)

            if customer in customer_group:
                customer_group.remove(customer)

            # Remove the customer's resolved order card once they are fully gone.
            if customer.order is not None:
                for i in range(len(manager.active_orders)):
                    if manager.active_orders[i] is customer.order:
                        manager.active_orders[i] = None
                        break
                customer.order = None

        # Recalculate the current waiting customer.
        if len(customersWaiting) > 0:
            currentCust = customersWaiting[0]
        else:
            currentCust = None
            Register.customerWaiting = False

    def drawHotBar(self, playerInventory, selectedSlot, font):
        for i in range(NUM_SLOTS):
            # makes rectangle object for that inventory slot at corresponding inventory position
            slot = pygame.Rect(INVENTORY_POSITIONS[i][0], INVENTORY_POSITIONS[i][1], SLOT_SIZE, SLOT_SIZE)

            # draws the grey slot background at that spot
            pygame.draw.rect(screen, (40, 40, 40), slot)

            # if that inventory slot has an item, draw that icon inside
            if playerInventory[i] != None:
                # placeholder for item pictures
                tempItemPic = pygame.Rect(slot.center[0], slot.center[1], 10, 10)
                pygame.draw.rect(screen, (255, 0, 0), tempItemPic)

            # if that inventory slot is selected, draw thick white border, else: draw thin black border
            if i == selectedSlot:
                pygame.draw.rect(screen, (255, 255, 255), slot, 3)
            else:
                pygame.draw.rect(screen, (0, 0, 0), slot, 2)

            # if the players mouse is hovering over a slot that isn't empty, display that items name next to the slot
            m_x, m_y = pygame.mouse.get_pos()
            if slot.collidepoint((m_x, m_y)):
                if playerInventory[i] != None:
                    spot = playerInventory[i]
                    if spot.name != "Cup":
                        screen.blit(font.render(f'{spot.name}', True, (0, 0, 0)), (slot.x + 60, slot.y + 15))
                    else:
                        screen.blit(font.render(f'{spot.name} with {', '.join(o.name for o in spot.contents)}', True, (0, 0, 0)), (slot.x + 60, slot.y + 15))

    def draw_recipe_screen(self, screen):
        """
        Draw the recipe menu using the same general layout style as the shop screen.
        """
        overlay = pygame.Surface((700, 420))
        overlay.set_alpha(235)
        overlay.fill((25, 25, 25))

        box_x = constants.WIDTH // 2 - 350
        box_y = constants.HEIGHT // 2 - 210
        screen.blit(overlay, (box_x, box_y))
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, 700, 420), 3)

        title_font = pygame.font.SysFont(None, 42)
        body_font = pygame.font.SysFont(None, 28)
        small_font = pygame.font.SysFont(None, 22)

        title = title_font.render("Recipes", True, constants.WHITE)
        screen.blit(title, (box_x + 20, box_y + 20))

        hint_1 = small_font.render("Press ESC to close the recipe menu", True, constants.WHITE)
        hint_2 = small_font.render("Unlocked recipes:", True, constants.WHITE)
        screen.blit(hint_1, (box_x + 20, box_y + 70))
        screen.blit(hint_2, (box_x + 20, box_y + 105))

        item_y = box_y + 155
        for i, recipe in enumerate(RECIPES_UNLOCKED):
            line = body_font.render(f"[{i + 1}] {recipe}", True, constants.WHITE)
            screen.blit(line, (box_x + 30, item_y))
            item_y += 45

        self.draw_message(screen)

    def draw_shop_screen(self, screen):
        """
        Draw the placeholder shop and upgrades overlay.
        """
        overlay = pygame.Surface((700, 420))
        overlay.set_alpha(235)
        overlay.fill((25, 25, 25))

        box_x = constants.WIDTH // 2 - 350
        box_y = constants.HEIGHT // 2 - 210
        screen.blit(overlay, (box_x, box_y))
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, 700, 420), 3)

        title_font = pygame.font.SysFont(None, 42)
        body_font = pygame.font.SysFont(None, 28)
        small_font = pygame.font.SysFont(None, 22)

        title = title_font.render("Shop / Upgrades", True, constants.WHITE)
        screen.blit(title, (box_x + 20, box_y + 20))

        money_text = body_font.render(f"Money: ${self.money}", True, constants.WHITE)
        screen.blit(money_text, (box_x + 20, box_y + 70))

        hint_1 = small_font.render("Press ESC to close the shop", True, constants.WHITE)
        hint_2 = small_font.render("Press 1, 2, or 3 to buy a placeholder upgrade", True, constants.WHITE)
        screen.blit(hint_1, (box_x + 20, box_y + 110))
        screen.blit(hint_2, (box_x + 20, box_y + 135))

        item_y = box_y + 185
        for i, upgrade in enumerate(self.upgrades):
            status = "OWNED" if upgrade["purchased"] else f"${upgrade['cost']}"
            line = body_font.render(
                f"[{i + 1}] {upgrade['name']} - {status}",
                True,
                constants.GREEN if upgrade["purchased"] else constants.WHITE
            )
            screen.blit(line, (box_x + 30, item_y))
            item_y += 55

        self.draw_message(screen)

    def draw_money(self, screen, font):
        """
        Draw the current money total in the HUD.
        """
        money_text = font.render(f"Money: ${self.money}", True, constants.BLACK)
        screen.blit(money_text, (1000, 48))

    def draw_message(self, screen):
        """
        Draw the current temporary on-screen message.
        """
        if self.message == "":
            return

        msg_font = pygame.font.SysFont(None, 30)
        message_x = constants.WIDTH // 2 - 100
        message_y = 120
        outline = msg_font.render(self.message, True, (0, 0, 0))
        text = msg_font.render(self.message, True, (255, 255, 255))
        screen.blit(outline, (message_x - 1, message_y))
        screen.blit(outline, (message_x + 1, message_y))
        screen.blit(outline, (message_x, message_y - 1))
        screen.blit(outline, (message_x, message_y + 1))
        screen.blit(text, (message_x, message_y))

    def change_counters_pos(self, view):
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

    def front_view_rendering(self, player, customers, font, keys, DebugMode):
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
                entity.render(screen, DebugMode)
            screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
            if currentCust != None and currentCust.state == "waiting":
                register1.render(screen)
            pygame.draw.rect(screen, (255, 255, 255), counterCup)
        else:
            for c in customers:
                c.render(screen, DebugMode)
            screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
            if currentCust != None and currentCust.state == "waiting":
                register1.render(screen)
            pygame.draw.rect(screen, (255, 255, 255), counterCup)
            # 3. Draw the player last (on top of everything)
            player.render(screen, DebugMode)

        recipe_button.draw(screen)
        shop_button.draw(screen)

        if player.rect.colliderect(register1.interactionZone) and register1.customerWaiting:
            label = font.render("[E] Take Order", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (
            register1.interactionZone.centerx - label.get_width() // 2, register1.interactionZone.top - 24,), )

        if player.rect.colliderect(switch_view_prompt_rect_cafe):
            label = font.render("[Q] Switch View", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (switch_view_prompt_rect_cafe.centerx - label.get_width() // 2,
                                switch_view_prompt_rect_cafe.top - 12,), )

        if DebugMode == True:
                for c in front_counters:
                    pygame.draw.rect(screen, (250, 0, 0), c)
                pygame.draw.rect(screen, (255, 255, 0), register1.interactionZone, 3)
                for c in front_collisions:
                    pygame.draw.rect(screen, (255, 255, 0), c, 2)

        self.drawHotBar(player.inventory, player.selectedSlot, font)

    def middle_view_rendering(self, player, font, keys, DebugMode):
        player.handle_movement(keys, middle_collisions)
        screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))

        for m in machines:
            m.render(screen, debug=DebugMode)

        player.render(screen, DebugMode)
        if currentCust != None and currentCust.state == "waiting":
            register2.render(screen)

        screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))

        if DebugMode == True:
            for c in middle_collisions:
                pygame.draw.rect(screen, (255, 255, 0), c, 2)
            for c in middle_counters:
                pygame.draw.rect(screen, (250, 0, 0), c)
            pygame.draw.rect(screen, (255, 255, 0), register2.interactionZone, 3)
            pygame.draw.rect(screen, (255, 255, 0), doorEntry, 2)

        recipe_button.draw(screen)
        shop_button.draw(screen)
        if player.rect.colliderect(switch_view_prompt_rect_middle):
            label = font.render("[Q] Switch View", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (switch_view_prompt_rect_middle.centerx - label.get_width() // 2,
                                switch_view_prompt_rect_middle.top - 12,), )

        for m in machines:
            if m.is_player_nearby(player):
                label = font.render(f"[E] {m.name}  ({m.state})", True, (255, 255, 255))
                screen.blit(label, (m.rect.centerx - label.get_width() // 2, m.rect.top - 24))

        self.drawHotBar(player.inventory, player.selectedSlot, font)

    def back_view_rendering(self, player, boxes_list, font, keys, DebugMode):

        player.handle_movement(keys, backroom_collisions)
        screen.fill((0, 0, 0))

        for i in boxes_list:
            if i != None:
                i.render(screen)

        for c in backroom_collisions:
            if isinstance(c, pygame.Rect):
                pygame.draw.rect(screen, (255, 255, 255), c, 2)
            else:
                c.render(screen)

        pygame.draw.rect(screen, (255, 255, 0), doorEntry2, 2)
        player.render(screen, DebugMode)
        self.drawHotBar(player.inventory, player.selectedSlot, font)

        if DebugMode == True:
            for c in backroom_collisions:
                pygame.draw.rect(screen, (255, 255, 0), c, 2)



def main():
    global Customer, currentCust
    pygame.display.set_caption("Cafe Sim")
    font = pygame.font.SysFont(None, 22)

    clock_font = pygame.font.SysFont(None, 45)
    clock = pygame.time.Clock()
    seconds_per_frame = TIME_SPEED / 60
    game_seconds = 21600  # Start day at 6:00 AM

    manager = GameManager()

    DebugMode = True
    GameState = "PLAYING"
    CafeView = "FRONT"
    RecipeView = RECIPE_VIEW_NONE
    ShopView = SHOP_VIEW_NONE

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
    player = Player(40, 600, "player_idle_front")
    all_sprites.add(player)

    """for testing the minigame mode I'm defaulting the player with water"""
    player.inventory[0] = water
    player.inventory[1] = bag_coffee_beans
    is_dragging = False

    # orders list
    orders_list = []

    for recipe in ALL_RECIPES:
        if recipe.locked == False:
            RECIPES_UNLOCKED.append(recipe)

    running = True
    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        m_x, m_y = pygame.mouse.get_pos()

        # manages getting time each frame to make accurate clock for a 10 minutes cafe day
        game_seconds += seconds_per_frame
        if game_seconds >= REAL_DAY_SEC:
            game_seconds = 0
        hours = int(game_seconds // 3600)
        minutes = int((game_seconds % 3600) // 60)

        manager.update_message()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            '''IMPORTANT: here is a spot to add key presses that do what you might need without having the logic behind it'''
            if DebugMode == True:
                if event.type == pygame.MOUSEMOTION:
                    print(f"Mouse position: X={m_x}, Y={m_y}")

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        print("Adding $8")
                        manager.money += 8


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1 and recipe_button.is_clicked(event.pos):
                    current_screen = "recipes"
                    RecipeView = RECIPE_VIEW_MENU

                if event.button == 1 and shop_button.is_clicked(event.pos):
                    current_screen = "shop"
                    ShopView = SHOP_VIEW_MENU


                if GameState == "MACHINE":
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

                if GameState == "BACKROOM":
                    # loops through all backroom objects looking for shelves
                    for obj in backroom_collisions:
                        if isinstance(obj, stockingShelf):
                            # if player is standing in shelf interaction zone and clicks on shelf spot with item in hand, attempt to place it
                            if player.get_foot_rect().colliderect(obj.interactionZone) and player.inventory[player.selectedSlot] != None:
                                if event.button == 1:
                                    for shelfSpot in obj.spots:
                                        if shelfSpot.rect.collidepoint(m_x, m_y):
                                            shelfSpot.storeIngredientBox(player.inventory[player.selectedSlot], player)

            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                if active_machine and active_machine.ingredient and (active_machine.state == "empty" or active_machine.state == "error"):
                    if active_machine.mg_interaction_zone.colliderect(active_machine.ingredient_rect):
                        active_machine.add(active_machine.ingredient, player)


            if event.type == pygame.KEYDOWN:
                if GameState == "PLAYING" and not active_machine:
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
                    customersWaiting.clear()
                    manager.clear_round_state()
                    Register.customerWaiting = False
                    currentCust = None

                if event.key == pygame.K_q and GameState=="PLAYING":
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        manager.change_counters_pos(CafeView)
                    else:
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        manager.change_counters_pos(CafeView)

                # if player presses e inside registers collision zone, and there is a customer, take order
                if event.key == pygame.K_e:
                    if player.get_foot_rect().colliderect(register1.interactionZone) and register1.customerWaiting and CafeView == "FRONT":
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(register2.interactionZone) and register2.customerWaiting and CafeView == "MIDDLE":
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(doorEntry) and GameState == "PLAYING" and CafeView == "MIDDLE":
                        CafeView = "BACKROOM"
                        player.rect.x, player.rect.y = 30, 490
                    elif player.get_foot_rect().colliderect(doorEntry2) and CafeView == "BACKROOM":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 30, 115

                    elif GameState == "MACHINE" and active_machine:
                        if active_machine.state == "ready":
                            result = active_machine.remove_output()
                            if result:
                                print(f"Collected: {result.name}")
                                # also check if the spot has a cup or if the spot is full already
                                player.inventory[player.selectedSlot] = result
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
                            # Finds each ingredient box instance and checks for collision with interactionZone
                            if ingredientBoxes[i] != None:
                                if player.get_foot_rect().colliderect(ingredientBoxes[i].interactionZone):
                                    # grabs corresponding box and adds it to first open hot bar slot
                                    for j in range(len(player.inventory)):
                                        if player.inventory[j] == None:
                                            player.inventory[j] = ingredientBoxes[i]
                                            ingredientBox.popBox(ingredientBoxes[i], ingredientBoxes,backroom_collisions)
                                            numBoxes -= 1
                                            break

                if event.key == pygame.K_ESCAPE:
                    if GameState == "MACHINE":
                        active_machine = None
                    GameState = "PLAYING"
                    if RecipeView != RECIPE_VIEW_NONE:
                        RecipeView = RECIPE_VIEW_NONE
                        current_screen = "game"
                        continue
                    if ShopView != SHOP_VIEW_NONE:
                        ShopView = SHOP_VIEW_NONE
                        current_screen = "game"
                        continue
                    if GameState == "REGISTER":
                        GameState = "PLAYING"
                        continue
                    if GameState == "MACHINE":
                        GameState = "PLAYING"
                        active_machine = None
                        continue

                if event.key == pygame.K_s and GameState == "REGISTER":
                    if currentCust is None:
                        GameState = "PLAYING"
                        continue

                    orders_list.insert(0, currentCust.orderedItem)
                    time.sleep(1) # will need to be updated so the whole game doesn't pause

                    seat = manager.findFirstOpen(seats)  # find open seat
                    if seat is None:
                        manager.set_message("No open seats available")
                        continue

                    # If the order could not be accepted because cup slots are full,
                    # keep the customer at the register and undo the seat reservation.
                    if currentCust.orderedItem is None:
                        seat.openSeat()
                        currentCust.targetSeat = None
                        currentCust.seat_number = None
                        currentCust.targetPosition = None
                        currentCust.set_state("waiting")
                        continue
                    else:
                        seat.reserveSeat(currentCust)
                        currentCust.set_targetSeat(seat)
                        currentCust.set_state("walking to table")

                        for i in range(NUM_SLOTS):
                            if player.inventory[i] == None:
                                player.inventory[i] = Cup(0, 0, 20, 20)
                                break

                        # Remove from line.
                        if len(customersWaiting) > 0:
                            customersWaiting.pop(0)
                        # Move remaining customers up in line.
                        for i in range(len(customersWaiting)):
                            customersWaiting[i].state = "moving up in line"
                            customersWaiting[i].linePosition = LINE_POSITIONS[i]
                        # Update current front-of-line customer.
                        if len(customersWaiting) > 0:
                            currentCust = customersWaiting[0]
                        else:
                            currentCust = None
                            Register.customerWaiting = False

                    GameState = "PLAYING"

                # Placeholder shop purchases
                if ShopView != SHOP_VIEW_NONE:
                    if event.key == pygame.K_1:
                        manager.buy_upgrade(0)
                    elif event.key == pygame.K_2:
                        manager.buy_upgrade(1)
                    elif event.key == pygame.K_3:
                        manager.buy_upgrade(2)
                    continue

                # Pause normal gameplay input while a menu is open
                if RecipeView != RECIPE_VIEW_NONE or ShopView != SHOP_VIEW_NONE:
                    continue


            if event.type == SPAWN_EVENT:
                # if wait line is not current full and total customers not at max, spawn new customer
                if (len(customers) < MAX_CUSTOMERS and len(customersWaiting) < MAX_CUSTOMERS_WAITING and RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE):

                    # Calculate the index for the new customer
                    index = len(customersWaiting)
                    base_x, base_y = LINE_POSITIONS[index]

                    # Center the spawn coordinates
                    spawn_x = base_x - 60
                    spawn_y = base_y - 64

                    # Create the customer using the key "customer" from your IMAGE_LIBRARY
                    '''Each customer we design will have a list of image keys. Eventually we will have s system to make
                    different customers spawn so when a customer is created here, it would not be defaultly set to the ladybug.'''
                    currCustomer = Customer(spawn_x, spawn_y, ["ladybug_idle", "ladybug_sitting"], RECIPES_UNLOCKED,
                                            linePosition=LINE_POSITIONS[index])

                    if index == 0:
                        currentCust = currCustomer

                    all_sprites.add(currCustomer)
                    customer_group.add(currCustomer)

                    customers.append(currCustomer)
                    customersWaiting.append(currCustomer)
                    register1.setWaiting()


                # if ingredient spots open, spawn random ingredient box
                if numBoxes < MAX_INGREDIENT_BOXES:
                    for i in range(MAX_INGREDIENT_BOXES):
                        if ingredientBoxes[i] == None:
                            x, y = BOX_POSITIONS[i]
                            ingredBox = ingredientBox(x, y, "INGREDIENT")
                            ingredientBoxes[i] = ingredBox
                            backroom_collisions.append(ingredBox.rect)
                            numBoxes += 1
                            break

        if RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE:
            for c in customers:
                c.update(seats)

        manager.cleanup_gone_customers(customers, customersWaiting, all_sprites, customer_group, manager)

        if GameState == "PLAYING":
            if RecipeView != RECIPE_VIEW_NONE:
                manager.draw_recipe_screen(screen)
            elif ShopView != SHOP_VIEW_NONE:
                manager.draw_shop_screen(screen)
            else:
                if CafeView == "FRONT":
                    manager.front_view_rendering(player, customers, font, keys, DebugMode)
                elif CafeView == "MIDDLE":
                    manager.middle_view_rendering(player, font, keys, DebugMode)
                else:
                    manager.back_view_rendering(player, ingredientBoxes,font, keys, DebugMode)

        elif GameState == "REGISTER":
            register1.take_order(screen)

        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, DebugMode, font)
            if is_dragging:
                active_machine.ingredient_rect.center = (m_x, m_y)
                active_machine.ingredient.x = active_machine.ingredient_rect.x
                active_machine.ingredient.y = active_machine.ingredient_rect.y

        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        clock.tick(FPS)

        # Handles all text +  rendering
        text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()} | GameState: {GameState}", True, (230, 230, 230))
        orders_text = font.render(f'Orders: {', '.join(o.name for o in orders_list)}', True, (250, 0, 0))
        clock_text = clock_font.render(manager.handle_time(hours, minutes), True, 'black')
        screen.blit(text, (10, 10))
        screen.blit(orders_text, (10, 25))
        screen.blit(clock_text, (1202, 35))

        if (GameState == "PLAYING" and RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE):
            manager.draw_money(screen, font)
            #manager.draw_orders(screen)
            #manager.draw_inventory(screen, player)

        manager.draw_message(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

