#   pylint --errors-only main.py
#   pycodestyle --statistics main.py
#   pdoc -o ./html main.py

from classes import GameObject, Player, Table, Counter, Customer, Register, Seat, CupInventory, Order
from machines import Machine, CoffeeGrinder, EspressoMachine, WaterBoiler
import constants
from constants import *
import sys
import pygame
from button import Button


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

constants.IMAGE_LIBRARY["cg_empty"] = pygame.image.load("Machines_art/CoffeeGrinder_art/CGEmpty-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["cg_full"] = pygame.image.load("Machines_art/CoffeeGrinder_art/CGFull-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["cg_inprogress"] = pygame.image.load("Machines_art/CoffeeGrinder_art/CGInprogress-removebg-preview.png").convert_alpha()
constants.IMAGE_LIBRARY["em_empty"] = pygame.image.load("Machines_art/EspressoMachine_art/EMempty.png").convert_alpha()
constants.IMAGE_LIBRARY["em_inprogress"] = pygame.image.load("Machines_art/EspressoMachine_art/EMinprogress.png").convert_alpha()
constants.IMAGE_LIBRARY["em_ready"] = pygame.image.load("Machines_art/EspressoMachine_art/EMready.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_empty"] = pygame.image.load("Machines_art/WaterBoiler_art/WBempty.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_inprogress"] = pygame.image.load("Machines_art/WaterBoiler_art/WBinprogress.png").convert_alpha()
constants.IMAGE_LIBRARY["wb_ready"] = pygame.image.load("Machines_art/WaterBoiler_art/WBready.png").convert_alpha()

# Pre-scale all images in the library once
constants.IMAGE_LIBRARY["player"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player"], (120, 268))
constants.IMAGE_LIBRARY["customer"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["customer"], (120, 268))
constants.IMAGE_LIBRARY["order_screen"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["order_screen"], (1366, 768))
constants.IMAGE_LIBRARY["bg1"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1"], (1366, 768))
constants.IMAGE_LIBRARY["bg1_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg1_top"], (1366, 768))
constants.IMAGE_LIBRARY["bg2"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2"], (1366, 768))
constants.IMAGE_LIBRARY["bg2_top"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["bg2_top"], (1366, 768))
constants.IMAGE_LIBRARY["register_icon"] = pygame.transform.smoothscale(
    constants.IMAGE_LIBRARY["register_icon"], ((17 * 2), (33 * 2))
)

constants.IMAGE_LIBRARY["cg_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_empty"], (150, 200))
constants.IMAGE_LIBRARY["cg_full"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_full"], (150, 200))
constants.IMAGE_LIBRARY["cg_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cg_inprogress"], (150, 200))
constants.IMAGE_LIBRARY["em_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_empty"], (150, 200))
constants.IMAGE_LIBRARY["em_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_inprogress"], (150, 200))
constants.IMAGE_LIBRARY["em_ready"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["em_ready"], (150, 200))
constants.IMAGE_LIBRARY["wb_empty"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_empty"], (130, 200))
constants.IMAGE_LIBRARY["wb_inprogress"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_inprogress"], (130, 200))
constants.IMAGE_LIBRARY["wb_ready"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["wb_ready"], (130, 200))

# front room collision rects
counter3_rect = pygame.Rect(0, 590, 983, 50)
wall_rect2 = pygame.Rect(0, 293, 1400, 10)

# behind counter / middle collision rects
counter1_rect = pygame.Rect(187, 336, 983, 50)
counter2_rect = pygame.Rect(187, 718, 983, 50)
wall_rect = pygame.Rect(0, 333, 1400, 10)
menu_rect = pygame.Rect(1150, 0, 100, 800)

# builds all counters (about 165 apart from each other)
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10 = (
    Counter(7, 487),
    Counter(172, 487),
    Counter(336, 487),
    Counter(500, 487),
    Counter(664, 487),
    Counter(190, 250),
    Counter(358, 234),
    Counter(522, 234),
    Counter(686, 234),
    Counter(850, 234),
)

s1, s2, s3, s4, s5, s6 = (
    Seat(38, 243),
    Seat(253, 243),
    Seat(445, 243),
    Seat(660, 243),
    Seat(850, 243),
    Seat(1064, 243),
)

# Assign seat numbers 1-6 from left to right.
seats = [s1, s2, s3, s4, s5, s6]
for i, seat in enumerate(seats):
    seat.seat_number = i + 1

# build two registers - one for customers, the other dependent on the first and will display icon,
# can take order from both and will update the other
register1 = Register(829, 487, 110)
register2 = Register(193, 615, 10)

currentCust = None
currCustomer = None
current_screen = "game"

# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
back_collisions = [menu_rect]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, register2]
back_shelves = []

# LAVISHA Three machines placed at the back-counter positions
grinder = CoffeeGrinder(
    190, 250,
    constants.IMAGE_LIBRARY["cg_empty"],
    constants.IMAGE_LIBRARY["cg_full"],
    constants.IMAGE_LIBRARY["cg_inprogress"],
    w=150, h=200,
)
espresso_mach = EspressoMachine(
    358, 250,
    constants.IMAGE_LIBRARY["em_empty"],
    constants.IMAGE_LIBRARY["em_inprogress"],
    constants.IMAGE_LIBRARY["em_ready"],
    w=150, h=200,
)
water_boiler = WaterBoiler(
    540, 225,
    constants.IMAGE_LIBRARY["wb_empty"],
    constants.IMAGE_LIBRARY["wb_inprogress"],
    constants.IMAGE_LIBRARY["wb_ready"],
    w=150, h=200,
)
machines = [grinder, espresso_mach, water_boiler]
SHOP_VIEW_NONE = None
SHOP_VIEW_MENU = "MENU"
recipe_button = Button(1190, 342, 160, 78, "Recipe", "RECIPE_MENU", None)
shop_button = Button(1190, 468, 160, 78, "Shop", "SHOP_MENU", None)


class GameManager:
    """
    Holds game-wide progression and UI state.

    This keeps economy, orders, messages, and placeholder upgrade/shop
    data together without changing the gameplay loop structure too much.
    """
    def __init__(self):
        """Initialize the shared game state."""
        self.inventory = CupInventory()
        self.active_orders = [None] * MAX_ACTIVE_ORDERS
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

    def accept_order(self, customer):
        """
        Accept a customer's order if both an order slot and cup slot are available.

        This creates a visual order card and gives the player an empty cup.
        """
        if customer is None:
            return

        order_slot = self.first_empty_order_slot()
        cup_slot = self.inventory.first_empty_slot()

        if order_slot is None or cup_slot is None:
            self.set_message("No empty cup slots")
            return

        color = ORDER_COLORS[order_slot]

        order = Order(
            seat_number=customer.seat_number,
            drink_name="Black Coffee",
            color=color
        )

        customer.order = order
        self.active_orders[order_slot] = order
        self.inventory.add_empty_cup()

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
        self.active_orders = [None] * MAX_ACTIVE_ORDERS
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

    def draw_orders(self, screen):
        """
        Draw the fixed order slots across the top of the screen.
        """
        font = pygame.font.SysFont(None, 28)

        start_x = 200
        y = 20
        card_width = 180
        card_spacing = 200

        for i in range(len(self.active_orders)):
            order = self.active_orders[i]
            x = start_x + i * card_spacing

            rect = pygame.Rect(x, y, card_width, 60)

            # Empty slot outline
            outline_color = ORDER_COLORS[i]
            pygame.draw.rect(screen, outline_color, rect, 3)

            if order is not None:
                drink_text = font.render(order.drink_name, True, constants.WHITE)
                seat_text = font.render(f"Seat {order.seat_number}", True, constants.WHITE)

                screen.blit(drink_text, (x + 10, y + 10))
                screen.blit(seat_text, (x + 10, y + 35))

                if order.resolved:
                    resolved = font.render("Resolved", True, constants.GREEN)
                    screen.blit(resolved, (x + 85, y + 35))

    def draw_inventory(self, screen, player):
        """
        Draw the fixed cup inventory slots in the left-side boxes.
        """
        font = pygame.font.SysFont(None, 22)

        slot_rects = [player.ti_rect, player.bi_rect]

        for i in range(constants.MAX_CUP_SLOTS):
            rect = slot_rects[i]
            outline_color = ORDER_COLORS[i]

            pygame.draw.rect(screen, outline_color, rect, 2)

            cup = self.inventory.slots[i]

            if cup is not None:
                text = "Empty" if cup.is_empty() else cup.contents
                label = font.render(text, True, constants.WHITE)
                screen.blit(label, (rect.x + 60, rect.y + 15))

            if self.inventory.selected_slot == i:
                pygame.draw.rect(screen, constants.GREEN, rect, 3)

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


def cleanup_gone_customers(customers, customersWaiting, all_sprites, customer_group, manager):
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


def get_nearby_seated_customer(player, customers):
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


def findFirstOpen(seats):
    """
    Find and return the first open seat.

    Returns:
        Seat | None: The first open seat, or None if all seats are occupied.
    """
    for c in seats:
        if isinstance(c, Seat) and c.state == "open":
            return c
    return None


def change_counters_pos(view):
    """
    Change counter positions depending on the current cafe view.
    """
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


def main():
    """
    Run the main game loop.
    """
    global currentCust, current_screen

    pygame.display.set_caption("Cafe Sim")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    DebugMode = True

    GameState = "PLAYING"
    CafeView = "FRONT"
    RecipeView = RECIPE_VIEW_NONE
    ShopView = SHOP_VIEW_NONE
    active_machine = None

    # Other entities (Customers)
    customers = []
    customersWaiting = []

    # Shared game-wide state manager
    manager = GameManager()

    # Spawn timer
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player")
    all_sprites.add(player)

    # Machine run button for the current machine UI
    run_button_rect = pygame.Rect(540, 620, 140, 50)

    running = True
    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()

        # Clear expired messages.
        manager.update_message()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if event.button == 1 and recipe_button.is_clicked(event.pos):
                    current_screen = "recipes"
                    RecipeView = RECIPE_VIEW_MENU
                
                if event.button == 1 and shop_button.is_clicked(event.pos):
                    current_screen = "shop"
                    ShopView = SHOP_VIEW_MENU

                # Inventory slot clicking
                # In PLAYING: select/deselect cup slot
                # In MACHINE: load empty cup into machine
                slot_rects = [player.ti_rect, player.bi_rect]

                for i in range(constants.MAX_CUP_SLOTS):
                    if slot_rects[i].collidepoint(mouse_pos):

                        # Normal gameplay: select or deselect slot
                        if GameState == "PLAYING":
                            manager.inventory.select_slot(i)

                        # Machine UI: load empty cup into machine
                        elif GameState == "MACHINE":
                            cup = manager.inventory.slots[i]

                            if cup is None:
                                manager.set_message("No cup in that slot")
                            elif not cup.is_empty():
                                manager.set_message("Only empty cups allowed")
                            else:
                                manager.machine_loaded_slot = i
                                manager.set_message(f"Loaded slot {i + 1}")

                # Run button for machine UI
                if GameState == "MACHINE" and run_button_rect.collidepoint(mouse_pos):
                    if manager.machine_loaded_slot is None:
                        manager.set_message("Load a cup first")
                    else:
                        cup = manager.inventory.slots[manager.machine_loaded_slot]

                        if cup is not None and cup.is_empty():
                            cup.fill("Black Coffee")
                            manager.set_message("Drink created")
                            manager.machine_loaded_slot = None

            elif event.type == pygame.MOUSEMOTION and DebugMode:
                m_x, m_y = pygame.mouse.get_pos()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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

                if event.key == pygame.K_1 and ShopView == SHOP_VIEW_NONE and RecipeView == RECIPE_VIEW_NONE:
                    DebugMode = not DebugMode

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

                if event.key == pygame.K_r:
                    customers.clear()
                    customersWaiting.clear()
                    manager.clear_round_state()
                    Register.customerWaiting = False
                    currentCust = None

                if event.key == pygame.K_q and GameState == "PLAYING":
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        change_counters_pos(CafeView)
                    else:
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        change_counters_pos(CafeView)

                if event.key == pygame.K_e:
                    # Ignore E while already in machine UI.
                    # Machine actions are mouse based
                    if GameState == "MACHINE":
                        continue

                    # Ignore E unless the player is in normal gameplay
                    if GameState != "PLAYING":
                        continue

                    # FRONT VIEW interactions
                    if CafeView == "FRONT":
                        if player.rect.colliderect(register1.interactionZone) and register1.customerWaiting:
                            GameState = "REGISTER"
                            continue

                        nearby_customer = get_nearby_seated_customer(player, customers)

                        if nearby_customer is not None:
                            if manager.inventory.get_selected_cup() is None:
                                manager.set_message("Select a cup first")
                            else:
                                manager.serve_customer(nearby_customer)
                            continue

                    # MIDDLE VIEW interactions
                    elif CafeView == "MIDDLE":
                        if player.rect.colliderect(register2.interactionZone) and register2.customerWaiting:
                            GameState = "REGISTER"
                            continue

                        for m in machines:
                            if m.is_player_nearby(player):
                                active_machine = m
                                manager.machine_loaded_slot = None
                                GameState = "MACHINE"
                                break

                # Accept customer order at register
                if event.key == pygame.K_s and GameState == "REGISTER":
                    if currentCust is None:
                        GameState = "PLAYING"
                        continue

                    # Find open seat first.
                    seat = findFirstOpen(seats)

                    # Do not take the order if there is nowhere for the customer to go.
                    if seat is None:
                        manager.set_message("No open seats available")
                        continue

                    # Reserve the seat and assign it to the customer.
                    seat.reserveSeat(currentCust)
                    currentCust.set_targetSeat(seat)
                    currentCust.seat_number = seat.seat_number
                    currentCust.set_state("walking to table")

                    # Accept the order only after the customer has a seat assignment.
                    manager.accept_order(currentCust)

                    # If the order could not be accepted because cup slots are full,
                    # keep the customer at the register and undo the seat reservation.
                    if currentCust.order is None:
                        seat.openSeat()
                        currentCust.targetSeat = None
                        currentCust.seat_number = None
                        currentCust.targetPosition = None
                        currentCust.set_state("waiting")
                        continue

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

            # Spawn customers into the waiting line
            if (
                event.type == SPAWN_EVENT
                and len(customers) < MAX_CUSTOMERS
                and len(customersWaiting) < MAX_CUSTOMERS_WAITING
                and RecipeView == RECIPE_VIEW_NONE
                and ShopView == SHOP_VIEW_NONE
            ):
                index = len(customersWaiting)
                base_x, base_y = LINE_POSITIONS[index]

                # Center spawn coordinates using the customer sprite size.
                spawn_x = base_x - (constants.IMAGE_LIBRARY["customer"].get_width() // 2)
                spawn_y = base_y - (constants.IMAGE_LIBRARY["customer"].get_height() // 2)

                currCustomer = Customer(
                    spawn_x,
                    spawn_y,
                    "customer",
                    RECIPES_UNLOCKED,
                    linePosition=LINE_POSITIONS[index],
                )

                if index == 0:
                    currentCust = currCustomer

                all_sprites.add(currCustomer)
                customer_group.add(currCustomer)

                customers.append(currCustomer)
                customersWaiting.append(currCustomer)
                register1.setWaiting()

        # Only update customers while no menu is open
        if RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE:
            for c in customers:
                c.update(seats)

        # Remove customers that have left and clean up their orders.
        cleanup_gone_customers(customers, customersWaiting, all_sprites, customer_group, manager)

        # Main game rendering
        if GameState == "PLAYING":
            if RecipeView != RECIPE_VIEW_NONE:
                manager.draw_recipe_screen(screen)
            elif ShopView != SHOP_VIEW_NONE:
                manager.draw_shop_screen(screen)
            else:
                if CafeView == "FRONT":

                    player.handle_movement(keys, front_collisions)

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
                        if currentCust is not None and currentCust.state == "waiting":
                            register1.render(screen)
                        player.render(screen)

                    recipe_button.draw(screen)
                    shop_button.draw(screen)

                    # Serve tooltip for nearby seated customer.
                    nearby_customer = get_nearby_seated_customer(player, customers)
                    if nearby_customer is not None:
                        label = font.render("[E] Serve", True, (255, 255, 255))
                        screen.blit(
                            label,
                            (
                                nearby_customer.rect.centerx - label.get_width() // 2,
                                nearby_customer.rect.top - 24,
                            ),
                        )

                    if DebugMode:
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


                    if currentCust is not None and currentCust.state == "waiting":
                        register2.render(screen)

                    screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))
                    recipe_button.draw(screen)
                    shop_button.draw(screen)

                    for m in machines:
                        if m.is_player_nearby(player):
                            label = font.render(f"[E] {m.name}  ({m.state})", True, (255, 255, 255))
                            screen.blit(label, (m.rect.centerx - label.get_width() // 2, m.rect.top - 24))

                    if DebugMode:
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

                    if DebugMode:
                        for c in back_collisions:
                            pygame.draw.rect(screen, (255, 255, 0), c, 2)
                        for c in middle_counters:
                            pygame.draw.rect(screen, (250, 0, 0), c)

            # Old player inventory hover UI
            mx, my = pygame.mouse.get_pos()
            if player.ti_rect.collidepoint((mx, my)):
                inv_text = font.render(f"{player.top_inventory}", True, (250, 0, 0))
                screen.blit(inv_text, (mx + 10, my))
            if player.bi_rect.collidepoint((mx, my)):
                inv_text = font.render(f"{player.bottom_inventory}", True, (250, 0, 0))
                screen.blit(inv_text, (mx + 10, my))

            if DebugMode:
                pygame.draw.rect(screen, (255, 255, 0), player.get_foot_rect(), 2)

        elif GameState == "REGISTER":
            register1.take_order(screen)

        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, font)
            manager.draw_inventory(screen, player)
            pygame.draw.rect(screen, (80, 80, 80), run_button_rect)
            pygame.draw.rect(screen, constants.WHITE, run_button_rect, 2)

            run_font = pygame.font.SysFont(None, 30)
            run_text = run_font.render("Run", True, constants.WHITE)
            screen.blit(
                run_text,
                (
                    run_button_rect.centerx - run_text.get_width() // 2,
                    run_button_rect.centery - run_text.get_height() // 2
                )
            )

        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        clock.tick(FPS)

        text = font.render(
            f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()}",
            True,
            (230, 230, 230),
        )
        screen.blit(text, (10, 10))

        # Draw money only during gameplay
        if RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE:
            manager.draw_money(screen, font)

        if RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE:
            # Draw order cards, inventory, and temporary message
            manager.draw_orders(screen)
            manager.draw_inventory(screen, player)
            
        manager.draw_message(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()