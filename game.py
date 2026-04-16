import json
import os

from furniture import *
from items import *
from others import *
from player import *
from customer import *
from machines import *
import constants
from recipes import *
from constants import *
from backroom import *
from button import *

pygame.init()
screen = pygame.display.set_mode((1366, 768))
pygame.mixer.init()

constants.IMAGE_LIBRARY["player_idle_front"] = pygame.image.load("Cafe_Game_Art/player_idle_front.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_idle"] = pygame.image.load("Cafe_Game_Art/ladybug_idle.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_sitting"] = pygame.image.load("Cafe_Game_Art/ladybug_sitting.png").convert_alpha()
constants.IMAGE_LIBRARY["ladybug_register"] = pygame.image.load("Cafe_Game_Art/ladybug_register.png").convert_alpha()
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
constants.IMAGE_LIBRARY["ground_coffee"] = pygame.image.load("Cafe_Game_Art/ground_coffee.png").convert_alpha()


# All Recipes Images
constants.IMAGE_LIBRARY["cup"] = pygame.image.load("Cafe_Game_Art/cup.png").convert_alpha()
constants.IMAGE_LIBRARY["cup_w_lid"] = pygame.image.load("Cafe_Game_Art/cup_w_lid.png").convert_alpha()

#coolist sickest awesomeist images ever - (Michael's backroom art)
constants.IMAGE_LIBRARY["sick_rug"] = pygame.image.load("Cafe_Game_Art/sickestRug.png").convert_alpha()
constants.IMAGE_LIBRARY["best_box_ever"] = pygame.image.load("Cafe_Game_Art/bestBoxEver.png").convert_alpha()
constants.IMAGE_LIBRARY["fireAhhShelf"] = pygame.image.load("Cafe_Game_Art/fireAhShelf.png").convert_alpha()


# Pre-scale all images in the library them once
constants.IMAGE_LIBRARY["player_idle_front"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["player_idle_front"], (120, 268))
constants.IMAGE_LIBRARY["ladybug_idle"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["ladybug_idle"], (120, 268))
constants.IMAGE_LIBRARY["ladybug_register"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["ladybug_register"], (300, 400))
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
constants.IMAGE_LIBRARY["ground_coffee"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["ground_coffee"], ((348, 330)))
constants.IMAGE_LIBRARY["cup"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cup"], ((168, 216)))
constants.IMAGE_LIBRARY["cup_w_lid"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["cup_w_lid"], ((168, 216)))
constants.IMAGE_LIBRARY["sick_rug"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["sick_rug"], (150, 50))
constants.IMAGE_LIBRARY["best_box_ever"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["best_box_ever"], (100, 100))
constants.IMAGE_LIBRARY["fireAhhShelf"] = pygame.transform.smoothscale(constants.IMAGE_LIBRARY["fireAhhShelf"], (500, 300))



# Defines all ingredients
bag_coffee_beans = Ingredient("Coffee Beans", ["coffee_beans"], True, 18.35, 56)
ground_coffee = Ingredient("Ground Coffee",["ground_coffee"], True)
espresso_shot = Ingredient("Espresso Shot",["water"])
espresso_doubleShot = Ingredient("Espresso Double Shot",["water"])
water = Ingredient("Water",["water"], True)
hot_water = Ingredient("Hot Water",["water"])
ice = Ingredient("Ice",["water"])
milk = Ingredient("Milk",["water"], True, 3.28, 16)
steamed_milk = Ingredient("Steamed Milk",["water"])
foamed_milk = Ingredient("Foamed Milk",["water"])
cocoa_powder = Ingredient("Cocoa Powder",["water"], True, 9.40, 64)

# Ingredients List
INGREDIENTS = [bag_coffee_beans, ground_coffee, espresso_shot, water, hot_water, ice, milk, steamed_milk, foamed_milk, cocoa_powder]

# Defines all Recipes
Espresso = Recipe("Espresso Shot" ,[espresso_shot],6.50, "N/A", False)
Iced_Coffee = Recipe("Iced Coffee" ,[espresso_shot, ice],6.50, "N/A")
Americano = Recipe("Americano" ,[hot_water, espresso_shot],7.50, "N/A", False)
Latte = Recipe("Latte" ,[espresso_shot, steamed_milk],6.50, "N/A")
Iced_Latte = Recipe("Iced Latte" ,[espresso_shot, ice, milk],6.50, "N/A")
Hot_Chocolate = Recipe("Hot Chocolate" ,[hot_water, cocoa_powder, steamed_milk],6.50, "N/A")

# Recipes Lists
ALL_RECIPES = [Espresso, Iced_Coffee, Americano, Latte, Iced_Latte, Hot_Chocolate]
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

#counterCup = Cup(["cup", "cup_w_lid"])

currentCust = None
currCustomer = None
current_screen = "game"

# all collision lists for handling perspectives
front_collisions = [menu_rect, counter3_rect, wall_rect2]
middle_collisions = [menu_rect, counter1_rect, counter2_rect, wall_rect]
backroom_collisions = [stockingShelf(50, 30, 500, 300)]

# all interactable spots each scene (counters, register, sink, chairs, doors)
front_counters = [c1, c2, c3, c4, c5, register1, s1, s2, s3, s4, s5, s6]
seats = [s1, s2, s3, s4, s5, s6]
middle_counters = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, register2]
backroom_shelves = []

sink = Sink(1015, 234)

grinder        = Machine(193, 234, "Coffee Grinder",   bag_coffee_beans, [ground_coffee], 1, 3, ["cg_empty", "cg_inprogress", "cg_ready"], (510, 480, 150, 70))
espresso_mach  = Machine(358, 234, "Espresso Machine", ground_coffee,    [espresso_shot], 1, 5, ["em_empty","em_inprogress", "em_ready"], (490, 255, 65, 50))
water_boiler   =  Machine(520, 234, "Water Boiler",     water,             [hot_water], 1, 4, ["wb_empty","wb_inprogress","wb_ready"], (455, 220, 70, 90))

ALL_MACHINES = [grinder, espresso_mach, water_boiler] # when a machine is bought, append to this list

machines = [grinder, espresso_mach, water_boiler]

SHOP_VIEW_NONE = None
SHOP_VIEW_MENU = "MENU"
recipe_button = Button(1190, 342, 160, 78, "Recipes", "RECIPE_MENU", None)
shop_button = Button(1190, 468, 160, 78, "Shop", "SHOP_MENU", None)

# Main menu buttons (centered on 1366x768 screen)
menu_start_button  = Button(483, 320, 400, 70, "Start Game", "PLAYING", None)

# Pause menu buttons
pause_resume_button = Button(483, 280, 400, 70, "Resume",    "PLAYING", None)
pause_quit_button   = Button(483, 380, 400, 70, "Quit to Menu",      "QUIT",    None)

next_day_button = Button(100, 100, 100, 100, "Next Day", "NEXT_DAY", None)
quit_button = Button(266, 100, 100, 100, "Quit to Menu", "QUIT", None)

delete_save_button1 = Button(483, 320, 20, 20, "D", "DELETE_SAVE", None)
delete_save_button2 = Button(483, 420, 20, 20, "D", "DELETE_SAVE", None)
delete_save_button3 = Button(483, 520, 20, 20, "D", "DELETE_SAVE", None)
save1_button = Button(483, 320, 400, 70, "Save Slot 1", "SAVE1", None)
save2_button = Button(483, 420, 400, 70, "Save Slot 2", "SAVE2", None)
save3_button = Button(483, 520, 400, 70, "Save Slot 3", "SAVE3", None)
save_game1 = {"file": "save1.json","button": save1_button}
save_game2 = {"file": "save2.json","button": save2_button}
save_game3 = {"file": "save3.json","button": save3_button}
current_save_file = None
all_save_files = [save_game1, save_game2, save_game3]

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
        self.active_orders = []
        self.max_orders = 2 # Upgradable via shop later
        self.more_hands_tier = 0 # 0 = none bought, max = 3

        # day sequence variables
        self.money = 0
        self.money_earned_today = 0
        self.day_num = 1
        self.num_customers_today = 0
        self.customers_unhappy_today = 0

        # for taking a name when creating a new save file
        self.name_input_box = pygame.Rect(200, 200, 240, 40)
        self.name_prompt = "Enter Save Name..."
        self.name_input_text = ""
        self.name_input_active = False

        # Shop tab data — each key is a tab label, each value is a list of purchasable items.
        # Adding a new tab and items is as simple as adding to this structure and it gets integrated into the shop screen automatically.
        # tier controls lock order only in the upgrades tab so higher tier items require previous purchases.
        # Other tabs treat all items as independently purchasable so the tier is ignored.
        self.shop_tabs = {
            "Upgrades": [
                {"name": "More Hands I",   "desc": "+2 max orders",  "cost": 50,  "tier": 1, "purchased": False},
                {"name": "More Hands II",  "desc": "+2 max orders",  "cost": 100, "tier": 2, "purchased": False},
                {"name": "More Hands III", "desc": "+2 max orders",  "cost": 150, "tier": 3, "purchased": False},
                {"name": "Deeper Pockets I",   "desc": "+5 to max item stack size", "cost": 50,  "tier": 1, "purchased": False},
                {"name": "Deeper Pockets II",  "desc": "+5 to max item stack size", "cost": 100, "tier": 2, "purchased": False},
                {"name": "Deeper Pockets III", "desc": "+5 to max item stack size", "cost": 200, "tier": 3, "purchased": False},
                {"name": "Faster Grinder", "desc": "Reduces grind time by 35%",   "cost": 75,  "tier": 1, "purchased": False},
                {"name": "Quick Brew",     "desc": "Espresso pulls 50% faster",   "cost": 90,  "tier": 1, "purchased": False},
                {"name": "Extra Speed",   "desc": "Increases movement speed by 50%", "cost": 125, "tier": 1, "purchased": False},
            ],
            "Machines": [
                {"name": "Extra Espresso Machine", "desc": "Adds a second espresso machine", "cost": 200, "tier": 1, "purchased": False},
                {"name": "Second Grinder",         "desc": "Adds a second coffee grinder",   "cost": 180, "tier": 1, "purchased": False},
            ],
            "Cosmetics": [
                {"name": "Floral Wallpaper", "desc": "Redecorate the cafe walls",       "cost": 40, "tier": 1, "purchased": False},
                {"name": "Cozy Rugs",        "desc": "Add warm rugs to the floor",      "cost": 30, "tier": 1, "purchased": False},
                {"name": "Fairy Lights",     "desc": "String lights along the ceiling", "cost": 25, "tier": 1, "purchased": False},
            ],
        }

        # the old upgrade list is kept so existing save/load and buy_upgrade() calls don't break.
        # Points at the Upgrades tab items directly.
        self.upgrades = self.shop_tabs["Upgrades"]

        # Shop UI state — which tab is open and which page of items is showing.
        # ITEMS_PER_PAGE controls how many rows fit before pagination kicks in.
        self.active_tab     = "Upgrades"  # Default tab shown when shop opens
        self.shop_page      = 0           # 0-indexed current page within the active tab
        self.ITEMS_PER_PAGE = 6           # Max rows visible at once before arrows/pages appear

        # This list is used to maintain the order of tabs as defined in shop_tabs, since dict keys don't guarantee order.
        self.tab_order = list(self.shop_tabs.keys())

        # Shop UI and clickable rects — drawn each frame by draw_shop_screen().
        # Initialized here so event handlers never reference an undefined attribute.
        self.shop_tab_rects        = {}   # maps tab name → pygame.Rect
        self.shop_item_rects       = {}   # maps page-local row index → pygame.Rect
        self.shop_item_orig_idx    = {}   # maps page-local row index → original index in the tab's item list (used after sort)
        self.shop_arrow_left_rect  = None # None when no prev page or pygame.Rect
        self.shop_arrow_right_rect = None # None when no next page or pygame.Rect 

        # Recipe menu UI state — which tab is active, which page, and which recipe
        # is currently selected for the detail view.
        self.recipe_active_tab    = "Unlocked"  # Default tab shown when recipe menu opens
        self.recipe_page          = 0            # 0-indexed current page within the active tab
        self.selected_recipe      = None         # Recipe object currently shown in detail view
        self.recipe_cards_per_row = 3            # Number of cards per row in the grid
        self.recipe_rows_per_page = 2            # Rows of cards per page

        # Recipe menu click rects — redrawn each frame by draw_recipe_screen().
        # Initialized here so event handlers never hit an undefined attribute.
        self.recipe_tab_rects        = {}   # maps tab name → pygame.Rect
        self.recipe_card_rects       = {}   # maps page-local card index → pygame.Rect
        self.recipe_card_map         = {}   # maps page-local card index → Recipe object
        self.recipe_arrow_left_rect  = None
        self.recipe_arrow_right_rect = None

        self.save_name = "Empty Slot"

        self.data = {
            "name": self.save_name,
            "money": self.money,
            "day_num": self.day_num,
            "upgrades": self.upgrades,
            "machine_positions": [(grinder.rect.x, grinder.rect.y), (espresso_mach.rect.x, espresso_mach.rect.y), (water_boiler.rect.x, water_boiler.rect.y)]
        }


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

    def clear_round_state(self):
        """
        Reset lightweight gameplay state used during testing.
        """
        #self.inventory.clear_all()
        self.machine_loaded_slot = None
        self.message = ""
        self.message_timer = 0

    def buy_upgrade(self, upgrade_index):
        """
        Attempt to buy an upgrade using the old list index.

        Kept so it works with the older stuff — talks to buy_shop_item()
        using the Upgrades tab as the target.
         upgrade_index (int): The index of the upgrade in the Upgrades tab list.
        """
        self.buy_shop_item("Upgrades", upgrade_index)

    def buy_shop_item(self, tab_name, item_index, player=None):
        """
        Attempt to purchase an item from the given shop tab.

        Handles tier-gating for the Upgrades tab (higher tiers require the
        previous tier to be purchased first). All other tabs treat items as
        independently purchasable with no lock order.

        Parameters:
            tab_name   (str): The tab the item lives in (e.g. "Upgrades").
            item_index (int): The absolute index of the item within that tab's list.
            player     (Player): The player instance, required for upgrades that directly modify
                                player attributes/stats. Optional for upgrades that only modify GameManager state or are purely cosmetic.
        """
        tab_items = self.shop_tabs.get(tab_name)
        if tab_items is None or not (0 <= item_index < len(tab_items)):
            return

        item = tab_items[item_index]

        if item["purchased"]:
            self.set_message("Already purchased!")
            return

        # Tier-based locking only applies to the Upgrades tab
        if tab_name == "Upgrades" and item["tier"] > 1:
            prev = tab_items[item_index - 1]
            if not prev["purchased"]:
                self.set_message(f"Unlock {prev['name']} first!")
                return

        if self.money < item["cost"]:
            self.set_message(f"Need ${item['cost']:.2f} — not enough money!")
            return

        # Deduct cost and mark purchased
        self.money -= item["cost"]
        item["purchased"] = True

        # Apply upgrade purchased effects if in the Upgrades tab, otherwise just show a generic purchase message for now
        # In the future, other tabs can have their own unique effects implemented here
        # So lavisha, adding your placeable machines logic here would be a good call. 
        # You can add machines to the shop by adding them to the shop_tabs structure and then implement the placeable logic in this function.
        # By adding the new machine object to the ALL_MACHINES list and then allowing the player to place it somewhere in the cafe.
        # Actually it may be a good idea to implement the logic elsewhere and then just call it from here when the item is purchased, 
        # to keep this function from getting too cluttered. So you could have a seperate function like place_machine() that gets called when a machine item is purchased, 
        # and that function would handle the actual process of letting the player place the machine in the cafe and adding it to the ALL_MACHINES list once placed.
        if tab_name == "Upgrades":
            name = item["name"]
            # More Hands tiers increase the simultaneous order cap
            if "More Hands" in name:
                # Each tier adds 2 to the max orders
                self.more_hands_tier += 1
                self.max_orders += 2
                self.set_message(f"Purchased {item['name']}! Max orders: {self.max_orders}")
            elif name == "Faster Grinder":
                # Reduce grinder runtime by 35%, minimum 1 second
                grinder.runtime = max(1, round(grinder.runtime * 0.65))
                self.set_message(f"Purchased {item['name']}! Grinder now takes {grinder.runtime}s.")
            elif name == "Quick Brew":
                # Reduce espresso machine brew time by 50%, minimum 1 second
                espresso_mach.runtime = max(1, round(espresso_mach.runtime * 0.5))
                self.set_message(f"Purchased {item['name']}! Espresso machine now takes {espresso_mach.runtime}s.")
            elif name == "Extra Speed":
                # Increase player movement speed by 15%
                if player:
                    player.speed = round(player.speed * 1.5)
                    self.set_message(f"Purchased {item['name']}! Player speed increased.")
                else:
                    self.set_message(f"Purchased {name}!")
            elif "Deeper Pockets" in name:
                # Each tier adds 5 to the max stack size per inventory slot
                if player:
                    player.max_stack_size += 5
                    self.set_message(f"Purchased {name}! Max stack size: {player.max_stack_size}")
                else:
                    self.set_message(f"Purchased {name}!")
            else:
                # Fallback effect for upgrades without an effect implemented yet
                self.set_message(f"Purchased {item['name']}!")
        else:
            # Placeholder effect for Machines / Cosmetics tabs
            self.set_message(f"Purchased {item['name']}!")

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
        """Remove customers that have fully left the cafe. Also remove their resolved order cards once they are gone."""
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
            if customer.ordered_item is not None:
                for i in range(len(manager.active_orders)):
                    if manager.active_orders[i] is customer.ordered_item:
                        manager.active_orders[i] = None
                        break
                customer.ordered_item = None

        # Recalculate the current waiting customer.
        if len(customersWaiting) > 0:
            currentCust = customersWaiting[0]
        else:
            currentCust = None
            Register.customer_waiting = False

    def drawHotBar(self, player, font):
        """
        Draw the player's inventory hotbar on the left side of the screen.

        Uses the fixed INVENTORY_POSITIONS list from constants to position each slot.
        """
        player.update_inv_lengths()

        for i in range(NUM_SLOTS):
            # Position each slot using the fixed coordinates from constants
            slot_x = INVENTORY_POSITIONS[i][0]
            slot_y = INVENTORY_POSITIONS[i][1]

            slot = pygame.Rect(slot_x, slot_y, SLOT_SIZE, SLOT_SIZE)

            # Draw the grey slot background
            pygame.draw.rect(screen, (40, 40, 40), slot)

            quant = player.inventory_quants[i] if i < len(player.inventory_quants) else 0
            quantNum = font.render(f"{quant}", True, (255, 255, 255))
            screen.blit(quantNum, (slot_x + 5, slot_y + 5))

            # If that inventory slot has an item, draw the placeholder icon inside
            if len(player.inventory[i]) > 0:
                tempItemPic = pygame.Rect(slot.center[0], slot.center[1], 10, 10)
                pygame.draw.rect(screen, (255, 0, 0), tempItemPic)

            # Selected slot gets a thick white border; others get a thin black border
            if i == player.selected_slot:
                pygame.draw.rect(screen, (255, 255, 255), slot, 3)
            else:
                pygame.draw.rect(screen, (0, 0, 0), slot, 2)

            # Hovering over a non-empty slot shows the item name beside it
            m_x, m_y = pygame.mouse.get_pos()
            if slot.collidepoint((m_x, m_y)):
                if player.inventory[i] != None:
                    spot_list = player.inventory[i]
                    if len(spot_list) > 0:
                        if spot_list[0].name != "Cup":
                            screen.blit(font.render(f'{spot_list[0].name}', True, (0, 0, 0), (255, 255, 255)), (slot.x + 60, slot.y + 15))
                        else:
                            if spot_list[0].stackable is True:
                                text = font.render("Empty Cup", True, (0, 0, 0), (255, 255, 255))
                                screen.blit(text, (slot.x + 60, slot.y + 15))
                            else:
                                text = font.render(f'Cup with {", ".join(o.name for o in spot_list[0].contents)}', True, (0, 0, 0), (255, 255, 255))
                                screen.blit(text, (slot.x + 60, slot.y + 15))

    def draw_recipe_screen(self, screen):
        """
        Draw the recipe menu overlay with two tabs (Unlocked / Locked),
        a card grid of recipes, pagination, and an info bar.
 
        Layout (top to bottom):
            - Floating "Recipes" title above the box (main-menu gold style)
            - Box: tabs → info bar → card grid → dot indicator
            - Pagination arrows centered vertically on the left/right box edges
 
        Clicking an unlocked card opens the detail view (RECIPE_VIEW_DETAIL).
        Clicking a locked card deducts money and moves it to the unlocked list.
        """
        #dimensions
        BOX_W, BOX_H = 900, 580
        box_x = constants.WIDTH  // 2 - BOX_W // 2
        box_y = constants.HEIGHT // 2 - BOX_H // 2
 
        TAB_H      = 40   # Height of each tab strip
        INFO_H     = 48   # Height of the info bar below tabs
        DOT_AREA_H = 32   # Height reserved for the dot indicator
        ARROW_W    = 30   # Width of the clickable arrow zones on each side
 
        CARD_W     = 180  # Width of each recipe card
        CARD_H     = 160  # Height of each recipe card (image + name above)
        CARD_GAP   = 30   # Gap between cards horizontally and vertically
        IMG_H      = 110  # Height of the placeholder image area inside the card
 
        # Content area between info bar and dot region
        content_y = box_y + TAB_H + INFO_H + CARD_GAP
        content_x = box_x + ARROW_W
        content_w = BOX_W - ARROW_W * 2
 
        #fonts
        title_font = pygame.font.SysFont(None, 90)
        tab_font   = pygame.font.SysFont(None, 30)
        info_font  = pygame.font.SysFont(None, 24)
        name_font  = pygame.font.SysFont(None, 22)
        price_font = pygame.font.SysFont(None, 20)
 
        #colors 
        GOLD         = (220, 180, 120)
        DIM_GRAY     = (120, 120, 120)
        TAB_ACTIVE   = (50, 50, 50)
        TAB_INACTIVE = (20, 20, 20)
        DIVIDER      = (80, 80, 80)
 
        #floating title 
        title_surf = title_font.render("Recipes", True, GOLD)
        title_x    = constants.WIDTH // 2 - title_surf.get_width() // 2
        title_y    = box_y - title_surf.get_height() - 24
        screen.blit(title_surf, (title_x, title_y))
 
        pygame.draw.line(screen, GOLD,
                         (title_x, title_y + title_surf.get_height() + 2),
                         (title_x + title_surf.get_width(), title_y + title_surf.get_height() + 2), 2)
 
        #dark overlay box
        overlay = pygame.Surface((BOX_W, BOX_H))
        overlay.set_alpha(235)
        overlay.fill((25, 25, 25))
        screen.blit(overlay, (box_x, box_y))
 
        #tabs
        tab_names = ["Unlocked", "Locked"]
        tab_w     = BOX_W // len(tab_names)
        self.recipe_tab_rects = {}
 
        for i, tab_name in enumerate(tab_names):
            tx        = box_x + i * tab_w
            ty        = box_y
            is_active = (tab_name == self.recipe_active_tab)
            fill      = TAB_ACTIVE if is_active else TAB_INACTIVE
 
            pygame.draw.rect(screen, fill, (tx, ty, tab_w, TAB_H))
            pygame.draw.rect(screen, DIVIDER, (tx, ty, tab_w, TAB_H), 1)
 
            if is_active:
                pygame.draw.line(screen, (25, 25, 25),
                                 (tx + 1, ty + TAB_H - 1),
                                 (tx + tab_w - 2, ty + TAB_H - 1), 2)
 
            label   = tab_font.render(tab_name, True, constants.WHITE if is_active else DIM_GRAY)
            label_x = tx + tab_w // 2 - label.get_width() // 2
            label_y = ty + TAB_H  // 2 - label.get_height() // 2
            screen.blit(label, (label_x, label_y))
            self.recipe_tab_rects[tab_name] = pygame.Rect(tx, ty, tab_w, TAB_H)
 
        #info bar
        info_y = box_y + TAB_H
        pygame.draw.rect(screen, (30, 30, 30), (box_x, info_y, BOX_W, INFO_H))
        pygame.draw.line(screen, DIVIDER, (box_x, info_y + INFO_H), (box_x + BOX_W, info_y + INFO_H), 1)
 
        # Hint changes depending on which tab is active
        if self.recipe_active_tab == "Unlocked":
            click_hint = "Click a recipe to learn how to make it"
        else:
            click_hint = "Click a recipe to unlock it"
 
        info_items = [f"Money: ${self.money:.2f}", click_hint, "ESC to close"]
        info_segment_w = BOX_W // len(info_items)
        for j, info_text in enumerate(info_items):
            surf = info_font.render(info_text, True, DIM_GRAY)
            ix   = box_x + j * info_segment_w + info_segment_w // 2 - surf.get_width() // 2
            iy   = info_y + INFO_H // 2 - surf.get_height() // 2
            screen.blit(surf, (ix, iy))
            if j < len(info_items) - 1:
                sep_x = box_x + (j + 1) * info_segment_w
                pygame.draw.line(screen, DIVIDER, (sep_x, info_y + 6), (sep_x, info_y + INFO_H - 6), 1)
 
        # card grid
        # Build the list of recipes for the active tab
        if self.recipe_active_tab == "Unlocked":
            tab_recipes = list(RECIPES_UNLOCKED)
        else:
            tab_recipes = [r for r in ALL_RECIPES if r.locked]
 
        cards_per_page = self.recipe_cards_per_row * self.recipe_rows_per_page
        total_pages    = max(1, -(-len(tab_recipes) // cards_per_page))  # ceiling division
        page_recipes   = tab_recipes[self.recipe_page * cards_per_page :
                                     self.recipe_page * cards_per_page + cards_per_page]
 
        self.recipe_card_rects = {}
        self.recipe_card_map   = {}
 
        for card_i, recipe in enumerate(page_recipes):
            col = card_i % self.recipe_cards_per_row
            row = card_i // self.recipe_cards_per_row
 
            # Center the card grid horizontally within the content area
            grid_w = self.recipe_cards_per_row * CARD_W + (self.recipe_cards_per_row - 1) * CARD_GAP
            grid_start_x = content_x + (content_w - grid_w) // 2
 
            cx = grid_start_x + col * (CARD_W + CARD_GAP)
            cy = content_y + row * (CARD_H + CARD_GAP)
 
            card_rect = pygame.Rect(cx, cy, CARD_W, CARD_H)
 
            # Card background
            pygame.draw.rect(screen, (35, 35, 35), card_rect)
            pygame.draw.rect(screen, DIVIDER, card_rect, 1)
 
            # Placeholder image area (black box where drink art will go)
            img_rect = pygame.Rect(cx + 10, cy + 24, CARD_W - 20, IMG_H)
            pygame.draw.rect(screen, (0, 0, 0), img_rect)
 
            # Recipe name centered above the image
            name_surf = name_font.render(recipe.name, True, constants.WHITE)
            name_x    = cx + CARD_W // 2 - name_surf.get_width() // 2
            screen.blit(name_surf, (name_x, cy + 4))
 
            # Unlock cost shown at the bottom of locked cards
            if self.recipe_active_tab == "Locked":
                unlock_cost = recipe.price * 2.5
                cost_surf   = price_font.render(f"${unlock_cost:.2f} to unlock", True, GOLD)
                cost_x      = cx + CARD_W // 2 - cost_surf.get_width() // 2
                screen.blit(cost_surf, (cost_x, cy + CARD_H - 18))
 
            self.recipe_card_rects[card_i] = card_rect
            self.recipe_card_map[card_i]   = recipe
 
        #pagination arrows
        content_h  = BOX_H - TAB_H - INFO_H - DOT_AREA_H
        arrow_cy   = content_y + content_h // 2
        ARROW_SIZE = 10
 
        self.recipe_arrow_left_rect  = None
        self.recipe_arrow_right_rect = None
 
        if total_pages > 1:
            left_color  = constants.WHITE if self.recipe_page > 0 else DIM_GRAY
            right_color = constants.WHITE if self.recipe_page < total_pages - 1 else DIM_GRAY
            left_cx     = box_x + ARROW_W // 2
            right_cx    = box_x + BOX_W - ARROW_W // 2
 
            pygame.draw.polygon(screen, left_color, [
                (left_cx - ARROW_SIZE, arrow_cy),
                (left_cx + ARROW_SIZE, arrow_cy - ARROW_SIZE),
                (left_cx + ARROW_SIZE, arrow_cy + ARROW_SIZE),
            ])
            self.recipe_arrow_left_rect = pygame.Rect(box_x, content_y, ARROW_W, content_h)
 
            pygame.draw.polygon(screen, right_color, [
                (right_cx + ARROW_SIZE, arrow_cy),
                (right_cx - ARROW_SIZE, arrow_cy - ARROW_SIZE),
                (right_cx - ARROW_SIZE, arrow_cy + ARROW_SIZE),
            ])
            self.recipe_arrow_right_rect = pygame.Rect(box_x + BOX_W - ARROW_W, content_y, ARROW_W, content_h)
 
        #dot indicator
        if total_pages > 1:
            DOT_R        = 5
            DOT_GAP      = 16
            dots_total_w = (total_pages - 1) * DOT_GAP
            dot_start_x  = constants.WIDTH // 2 - dots_total_w // 2
            dot_y        = box_y + BOX_H - DOT_AREA_H // 2
 
            for d in range(total_pages):
                dx    = dot_start_x + d * DOT_GAP
                color = constants.WHITE if d == self.recipe_page else DIM_GRAY
                pygame.draw.circle(screen, color, (dx, dot_y), DOT_R)
 
        # White border drawn last so it sits on top of all content
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, BOX_W, BOX_H), 3)
 
        self.draw_message(screen)
 
    def draw_recipe_detail(self, screen):
        """
        Draw the recipe detail overlay on top of the recipe menu.
 
        Shows the step-by-step ingredient chain for the selected recipe,
        explaining which ingredients go into which machine to produce
        each component needed for the final drink.
 
        Layout:
            - Smaller dark box centered on screen
            - Info bar: recipe name on the left, ESC to close on the right
            - Content: one line per production step (ingredient → machine → output)
        """
        if self.selected_recipe is None:
            return
 
        #dimensions
        BOX_W, BOX_H = 620, 380
        box_x = constants.WIDTH  // 2 - BOX_W // 2
        box_y = constants.HEIGHT // 2 - BOX_H // 2
 
        INFO_H    = 44   # Height of the info bar at the top
        ROW_H     = 44   # Height per step row
        ROW_GAP   = 10   # Gap between rows
        ROW_PAD   = 20   # Left padding for row text
 
        # fonts
        info_font = pygame.font.SysFont(None, 24)
        step_font = pygame.font.SysFont(None, 26)
 
        #colors
        GOLD     = (220, 180, 120)
        DIM_GRAY = (120, 120, 120)
        DIVIDER  = (80, 80, 80)
        ARROW_COLOR = (180, 180, 180)
 
        #dark overlay box
        overlay = pygame.Surface((BOX_W, BOX_H))
        overlay.set_alpha(245)
        overlay.fill((20, 20, 20))
        screen.blit(overlay, (box_x, box_y))
 
        #info bar
        pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, BOX_W, INFO_H))
        pygame.draw.line(screen, DIVIDER, (box_x, box_y + INFO_H), (box_x + BOX_W, box_y + INFO_H), 1)
 
        name_surf = info_font.render(self.selected_recipe.name, True, GOLD)
        esc_surf  = info_font.render("ESC to close", True, DIM_GRAY)
        screen.blit(name_surf, (box_x + ROW_PAD, box_y + INFO_H // 2 - name_surf.get_height() // 2))
        screen.blit(esc_surf,  (box_x + BOX_W - esc_surf.get_width() - ROW_PAD,
                                box_y + INFO_H // 2 - esc_surf.get_height() // 2))
 
        # step-by-step ingredient chain
        # Build production steps by mapping each final ingredient back through
        # the machines that produce it. Each step is a tuple of
        # (input_name, machine_name, output_name).
        # Machine input→output relationships mirror the machine definitions in game.py.
        MACHINE_STEPS = [
            ("Coffee Beans", "Coffee Grinder", "Ground Coffee"),
            ("Ground Coffee", "Espresso Machine", "Espresso Shot"),
            ("Water", "Water Boiler", "Hot Water"),
        ]
 
        recipe = self.selected_recipe
        steps  = []
 
        # Find which machines are needed by working backwards from the recipe ingredients
        needed = {ing.name for ing in recipe.ingredients}
        for input_name, machine_name, output_name in MACHINE_STEPS:
            if output_name in needed:
                steps.append((input_name, machine_name, output_name))
                # The machine input may itself need to be produced
                needed.add(input_name)
 
        # Final serve step — shows all ingredients combining into the finished drink
        final_names = " + ".join(ing.name for ing in recipe.ingredients)
        steps.append((final_names, f"serve in Cup as {recipe.name}", ""))
 
        content_y = box_y + INFO_H + ROW_GAP
 
        for step_i, (inp, machine, out) in enumerate(steps):
            ry   = content_y + step_i * (ROW_H + ROW_GAP)
            rect = pygame.Rect(box_x + ROW_PAD, ry, BOX_W - ROW_PAD * 2, ROW_H)
 
            # Alternating row tint for readability
            if step_i % 2 == 1:
                alt = pygame.Surface((BOX_W - ROW_PAD * 2, ROW_H))
                alt.set_alpha(40)
                alt.fill((50, 50, 50))
                screen.blit(alt, (box_x + ROW_PAD, ry))
 
            pygame.draw.rect(screen, DIVIDER, rect, 1)
 
            # Build the step text: input  ->  machine  ->  output
            # Only show the second arrow if there is an output (final serve step has none)
            if out:
                step_text = f"{inp}  ->  {machine}  ->  {out}"
            else:
                step_text = f"{inp}  ->  {machine}"
            step_surf = step_font.render(step_text, True, constants.WHITE)
            screen.blit(step_surf, (box_x + ROW_PAD + 8,
                                    ry + ROW_H // 2 - step_surf.get_height() // 2))
 
        # White border drawn last
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, BOX_W, BOX_H), 3)

    def draw_shop_screen(self, screen):
        """
        Draw the full shop overlay with the tabs, paginated item list,
        an info bar, and pagination dot indicator.

        Layout (top to bottom):
            - Floating "Shop" title above the box (main-menu gold style)
            - Menu: tabs, info bar, items, dot indicator
            - Pagination arrows centered vertically on the left/right edges of the box
        """
        # Dimensions
        BOX_W, BOX_H = 900, 580
        box_x = constants.WIDTH  // 2 - BOX_W // 2
        box_y = constants.HEIGHT // 2 - BOX_H // 2

        TAB_H       = 40  # Height of each tab strip
        INFO_H      = 48  # Height of the info bar below tabs
        DOT_AREA_H  = 32  # Height reserved for the dot indicator at the bottom
        ARROW_W     = 30  # Width of the clickable arrow regions on the sides
        ROW_H       = 62  # Vertical space per item row
        ROW_PADDING = 18  # Left padding for text inside a row
        ROW_GAP     = 12  # Gap between rows (outside the rect)
        ROW_STRIDE  = ROW_H + ROW_GAP  # Total vertical step from one row to the next

        # Content area sits between the info bar and the dot region
        content_y = box_y + TAB_H + INFO_H + ROW_GAP
        content_h = BOX_H - TAB_H - INFO_H - DOT_AREA_H
        content_x = box_x + ARROW_W      # leave room for left arrow
        content_w = BOX_W - ARROW_W * 2  # leave room for right arrow

        # Fonts
        title_font  = pygame.font.SysFont(None, 90)
        tab_font    = pygame.font.SysFont(None, 30)
        info_font   = pygame.font.SysFont(None, 24)
        name_font   = pygame.font.SysFont(None, 28)
        desc_font   = pygame.font.SysFont(None, 22)
        status_font = pygame.font.SysFont(None, 26)

        # Colors
        GOLD         = (220, 180, 120)  # main-menu title color
        DIM_GRAY     = (120, 120, 120)
        ROW_ALT      = (35, 35, 35)    # alternating row tint
        TAB_ACTIVE   = (50, 50, 50)    # active tab fill
        TAB_INACTIVE = (20, 20, 20)    # inactive tab fill
        DIVIDER      = (80, 80, 80)    # thin separator lines

        # Floating Title Above The Box
        title_surf = title_font.render("Shop", True, GOLD)
        title_x    = constants.WIDTH // 2 - title_surf.get_width() // 2
        title_y    = box_y - title_surf.get_height() - 24  # 8 px gap above box
        screen.blit(title_surf, (title_x, title_y))

        # Thin decorative line under the floating title
        pygame.draw.line(screen, GOLD,
                         (title_x, title_y + title_surf.get_height() + 2),
                         (title_x + title_surf.get_width(), title_y + title_surf.get_height() + 2), 2)

        # dark overlay box
        overlay = pygame.Surface((BOX_W, BOX_H))
        overlay.set_alpha(235)
        overlay.fill((25, 25, 25))
        screen.blit(overlay, (box_x, box_y))

        # tabs
        # Tabs are evenly distributed across the full box width so adding a new
        # tab to self.tab_order automatically adjusts all positions.
        num_tabs = len(self.tab_order)
        tab_w    = BOX_W // num_tabs

        self.shop_tab_rects = {}  # rebuilt each frame for click detection in main()

        for i, tab_name in enumerate(self.tab_order):
            tx        = box_x + i * tab_w
            ty        = box_y
            is_active = (tab_name == self.active_tab)
            fill      = TAB_ACTIVE if is_active else TAB_INACTIVE

            pygame.draw.rect(screen, fill, (tx, ty, tab_w, TAB_H))
            pygame.draw.rect(screen, DIVIDER, (tx, ty, tab_w, TAB_H), 1)

            # Active tab: erase the bottom border so it visually "opens" into content
            if is_active:
                pygame.draw.line(screen, (25, 25, 25),
                                 (tx + 1, ty + TAB_H - 1),
                                 (tx + tab_w - 2, ty + TAB_H - 1), 2)

            label   = tab_font.render(tab_name, True, constants.WHITE if is_active else DIM_GRAY)
            label_x = tx + tab_w // 2 - label.get_width() // 2
            label_y = ty + TAB_H  // 2 - label.get_height() // 2
            screen.blit(label, (label_x, label_y))

            self.shop_tab_rects[tab_name] = pygame.Rect(tx, ty, tab_w, TAB_H)

        # info bar 
        info_y = box_y + TAB_H
        pygame.draw.rect(screen, (30, 30, 30), (box_x, info_y, BOX_W, INFO_H))
        pygame.draw.line(screen, DIVIDER, (box_x, info_y + INFO_H), (box_x + BOX_W, info_y + INFO_H), 1)

        # Info items spread across the bar with vertical separators between them
        info_items = [
            f"Money: ${self.money:.2f}",
            f"Max Orders: {self.max_orders}",
            "Click an item to buy",
            "ESC to close",
        ]
        info_segment_w = BOX_W // len(info_items)
        for j, info_text in enumerate(info_items):
            surf = info_font.render(info_text, True, DIM_GRAY)
            ix   = box_x + j * info_segment_w + info_segment_w // 2 - surf.get_width() // 2
            iy   = info_y + INFO_H // 2 - surf.get_height() // 2
            screen.blit(surf, (ix, iy))
            # Vertical separator between segments (skip after the last one)
            if j < len(info_items) - 1:
                sep_x = box_x + (j + 1) * info_segment_w
                pygame.draw.line(screen, DIVIDER, (sep_x, info_y + 6), (sep_x, info_y + INFO_H - 6), 1)

        # paginated item list
        tab_items = self.shop_tabs[self.active_tab]

        # Sort items so locked ones always sink to the bottom of the list.
        # We compute lock state for sorting purposes before slicing the page.
        def is_locked(item, index):
            """Return True if this item should be locked (Upgrades tab tier-gating only)."""
            if self.active_tab == "Upgrades" and item["tier"] > 1:
                return not tab_items[index - 1]["purchased"]
            return False

        def sort_key(pair):
            """Sort order: purchasable (0) → locked (1) → purchased (2)."""
            _, item = pair
            idx = pair[0]
            if item["purchased"]:
                return 2
            if is_locked(item, idx):
                return 1
            return 0

        sorted_items = sorted(enumerate(tab_items), key=sort_key)
        # Strip back to just the items in sorted order for pagination
        sorted_tab_items = [item for _, item in sorted_items]
        # Keep a mapping from sorted position → original index for buy logic
        sorted_index_map = [orig_i for orig_i, _ in sorted_items]

        total_pages    = max(1, -(-len(sorted_tab_items) // self.ITEMS_PER_PAGE))  # ceiling division
        page_items     = sorted_tab_items[self.shop_page * self.ITEMS_PER_PAGE :
                                          self.shop_page * self.ITEMS_PER_PAGE + self.ITEMS_PER_PAGE]
        page_index_map = sorted_index_map[self.shop_page * self.ITEMS_PER_PAGE :
                                          self.shop_page * self.ITEMS_PER_PAGE + self.ITEMS_PER_PAGE]

        self.shop_item_rects    = {}  # rebuilt each frame; maps page-local row → Rect
        self.shop_item_orig_idx = {}  # maps page-local row → original tab_items index

        for row_i, item in enumerate(page_items):
            ry   = content_y + row_i * ROW_STRIDE
            rect = pygame.Rect(content_x, ry, content_w, ROW_H)

            # Alternating row background for readability
            if row_i % 2 == 1:
                alt_surf = pygame.Surface((content_w, ROW_H))
                alt_surf.set_alpha(60)
                alt_surf.fill(ROW_ALT)
                screen.blit(alt_surf, (content_x, ry))

            pygame.draw.rect(screen, DIVIDER, rect, 1)

            # Re-evaluate lock state using the item's original index
            orig_index = page_index_map[row_i]
            locked = is_locked(item, orig_index)

            # Name column (left)
            name_color = DIM_GRAY if locked else constants.WHITE
            name_surf  = name_font.render(item["name"], True, name_color)
            screen.blit(name_surf, (content_x + ROW_PADDING, ry + ROW_H // 2 - name_surf.get_height() // 2))

            # Description column (center, smaller and dimmer)
            desc_surf = desc_font.render(item["desc"], True, DIM_GRAY)
            desc_x    = content_x + content_w // 3
            screen.blit(desc_surf, (desc_x, ry + ROW_H // 2 - desc_surf.get_height() // 2))

            # Status badge (right-aligned)
            if item["purchased"]:
                status_text  = "OWNED"
                status_color = constants.GREEN
            elif locked:
                status_text  = "LOCKED"
                status_color = DIM_GRAY
            else:
                status_text  = f"${item['cost']:.2f}"
                status_color = constants.WHITE

            status_surf = status_font.render(status_text, True, status_color)
            status_x    = content_x + content_w - status_surf.get_width() - ROW_PADDING
            screen.blit(status_surf, (status_x, ry + ROW_H // 2 - status_surf.get_height() // 2))

            self.shop_item_rects[row_i]    = rect
            self.shop_item_orig_idx[row_i] = orig_index

        # pagination arrows (drawn as triangles, centered on box sides)
        arrow_cy   = content_y + content_h // 2  # vertical center of content area
        ARROW_SIZE = 10 # half-height of the triangle

        self.shop_arrow_left_rect  = None
        self.shop_arrow_right_rect = None

        if total_pages > 1:
            left_color  = constants.WHITE if self.shop_page > 0 else DIM_GRAY
            right_color = constants.WHITE if self.shop_page < total_pages - 1 else DIM_GRAY
            left_cx     = box_x + ARROW_W // 2           # center x of left arrow zone
            right_cx    = box_x + BOX_W - ARROW_W // 2   # center x of right arrow zone

            # Left triangle — tip points left
            pygame.draw.polygon(screen, left_color, [
                (left_cx - ARROW_SIZE, arrow_cy),               # tip
                (left_cx + ARROW_SIZE, arrow_cy - ARROW_SIZE),  # top-right
                (left_cx + ARROW_SIZE, arrow_cy + ARROW_SIZE),  # bottom-right
            ])
            self.shop_arrow_left_rect = pygame.Rect(box_x, content_y, ARROW_W, content_h)

            # Right triangle — tip points right
            pygame.draw.polygon(screen, right_color, [
                (right_cx + ARROW_SIZE, arrow_cy),               # tip
                (right_cx - ARROW_SIZE, arrow_cy - ARROW_SIZE),  # top-left
                (right_cx - ARROW_SIZE, arrow_cy + ARROW_SIZE),  # bottom-left
            ])
            self.shop_arrow_right_rect = pygame.Rect(box_x + BOX_W - ARROW_W, content_y, ARROW_W, content_h)

        # dot page indicator (bottom center)
        # Each dot represents one page; filled dot = current page.
        if total_pages > 1:
            DOT_R        = 5   # dot radius
            DOT_GAP      = 16  # center-to-center spacing between dots
            dots_total_w = (total_pages - 1) * DOT_GAP
            dot_start_x  = constants.WIDTH // 2 - dots_total_w // 2
            dot_y        = box_y + BOX_H - DOT_AREA_H // 2

            for d in range(total_pages):
                dx    = dot_start_x + d * DOT_GAP
                color = constants.WHITE if d == self.shop_page else DIM_GRAY
                pygame.draw.circle(screen, color, (dx, dot_y), DOT_R)
        
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, BOX_W, BOX_H), 3)
        self.draw_message(screen)

    def draw_money(self, screen, font):
        """
        Draw the current money total in the HUD.
        """
        money_text = font.render(f"Money: ${self.money:.2f}", True, constants.BLACK)
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

    def draw_menu_screen(self, screen):
        """Draw the main menu with Start and Load options."""
        screen.fill((20, 12, 8))

        title_font = pygame.font.SysFont(None, 90)
        sub_font   = pygame.font.SysFont(None, 30)

        title = title_font.render("Cafe", True, (220, 180, 120))
        screen.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 160))

        hint = sub_font.render("A cozy cafe management game", True, (160, 130, 90))
        screen.blit(hint, (constants.WIDTH // 2 - hint.get_width() // 2, 265))

        menu_start_button.draw(screen)

    def draw_pause_menu(self, screen):
        """Draw the pause menu overlay."""
        overlay = pygame.Surface((constants.WIDTH, constants.HEIGHT))
        overlay.set_alpha(160)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        title_font = pygame.font.SysFont(None, 72)
        title = title_font.render("Paused", True, constants.WHITE)
        screen.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 190))

        pause_resume_button.draw(screen)
        pause_quit_button.draw(screen)

    def draw_load_menu(self, screen):
        """Draw the load menu with Load File options."""
        screen.fill((20, 12, 8))

        title_font = pygame.font.SysFont(None, 90)
        sub_font   = pygame.font.SysFont(None, 30)

        title = title_font.render("Saved Games", True, (220, 180, 120))
        screen.blit(title, (constants.WIDTH // 2 - title.get_width() // 2, 160))

        hint = sub_font.render("Select a saved game file to load", True, (160, 130, 90))
        screen.blit(hint, (constants.WIDTH // 2 - hint.get_width() // 2, 265))

        for save in all_save_files:
            try:
                data = self.load_game(save["file"])
                if data["day_num"] == 1:
                    save["button"].text = f"Empty Slot - New Game"
                else: 
                    save["button"].text = f"{data['name']} - Day {data['day_num']}"
            except:
                save["button"].text = f"Empty Slot - New Game"
            save["button"].draw(screen)

        delete_save_button1.draw(screen)
        delete_save_button2.draw(screen)
        delete_save_button3.draw(screen)

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

        for c in customers:
            if c.ordered_item is not None and (c.state == "finding seat" or c.state == "seated"):
                order_text = font.render(f"{c.ordered_item.get_name()}", True, (255, 255, 255), (0, 0, 0))
                screen.blit(order_text, (c.rect.x, c.rect.y - 50))

        if player.rect.bottom < 610:
            for entity in depth_list:
                entity.render(screen, DebugMode)
            screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
            if currentCust != None and currentCust.state == "waiting":
                register1.render(screen)
            #pygame.draw.rect(screen, (255, 255, 255), counterCup)
        else:
            for c in customers:
                c.render(screen, DebugMode)

            screen.blit(constants.IMAGE_LIBRARY["bg1_top"], (0, 0))
            back_img_positions = []
            back_img_y = 0
            for key, bx in back_img_positions:
                screen.blit(constants.IMAGE_LIBRARY[key], (bx, back_img_y))
            if currentCust != None and currentCust.state == "waiting":
                register1.render(screen)
            #pygame.draw.rect(screen, (255, 255, 255), counterCup)
            # 3. Draw the player last (on top of everything)
            player.render(screen, DebugMode)

        recipe_button.draw(screen)
        shop_button.draw(screen)

        if player.rect.colliderect(register1.interaction_zone) and register1.customer_waiting:
            label = font.render("[E] Take Order", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (
            register1.interaction_zone.centerx - label.get_width() // 2, register1.interaction_zone.top - 24,), )

        if player.rect.colliderect(switch_view_prompt_rect_cafe):
            label = font.render("[Q] Switch View", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (switch_view_prompt_rect_cafe.centerx - label.get_width() // 2,
                                switch_view_prompt_rect_cafe.top - 12,), )

        if DebugMode is True:
            for c in front_counters:
                pygame.draw.rect(screen, (250, 0, 0), c)
            pygame.draw.rect(screen, (255, 255, 0), register1.interaction_zone, 3)
            for c in front_collisions:
                pygame.draw.rect(screen, (255, 255, 0), c, 2)

        self.drawHotBar(player, font)

    def middle_view_rendering(self, player, font, keys, DebugMode):
        player.handle_movement(keys, middle_collisions)
        screen.blit(constants.IMAGE_LIBRARY["bg2"], (0, 0))

        for m in machines:
            m.render(screen, debug=DebugMode)

        sink.render(screen, DebugMode)
        doorEntry.render(screen)
        player.render(screen, DebugMode)
        if currentCust != None and currentCust.state == "waiting":
            register2.render(screen)

        screen.blit(constants.IMAGE_LIBRARY["bg2_top"], (0, 0))

        if DebugMode is True:
            for c in middle_collisions:
                pygame.draw.rect(screen, (255, 255, 0), c, 2)
            for c in middle_counters:
                pygame.draw.rect(screen, (250, 0, 0), c)
            pygame.draw.rect(screen, (255, 255, 0), register2.interaction_zone, 3)
            pygame.draw.rect(screen, (255, 255, 0), doorEntry, 2)

        recipe_button.draw(screen)
        shop_button.draw(screen)
        if player.rect.colliderect(switch_view_prompt_rect_middle):
            label = font.render("[Q] Switch View", True, constants.WHITE, constants.BLACK)
            screen.blit(label, (switch_view_prompt_rect_middle.centerx - label.get_width() // 2,
                                switch_view_prompt_rect_middle.top - 12,), )
        
        if sink.is_player_nearby(player):
            label = font.render(f"[E] Clear Cup | [F] Collect Water", True, (255, 255, 255))
            screen.blit(label, (sink.rect.centerx - label.get_width() // 2, sink.rect.top - 100))

        for m in machines:
            if m.is_player_nearby(player):
                label = font.render(f"[E] {m.name}  ({m.state})", True, (255, 255, 255))
                screen.blit(label, (m.rect.centerx - label.get_width() // 2, m.rect.top - 24))

        self.drawHotBar(player, font)

    def back_view_rendering(self, player, font, keys, DebugMode):
        player.handle_movement(keys, backroom_collisions)
        screen.fill((0, 0, 0))
        for c in backroom_collisions:
            c.render(screen, font)
            if isinstance(c, stockingShelf):
                pygame.draw.rect(screen, (255, 255, 255), c.interactionZone, 2)

        doorEntry2.render(screen)
        player.render(screen, DebugMode)
        self.drawHotBar(player, font)


    def save_game(self, filename):
        """Save the current game state to a JSON file."""
        data_to_save = {
            "name": self.save_name,
            "money": self.money,
            "day_num": self.day_num,
            "upgrades": self.upgrades,
            "machine_positions": [(grinder.rect.x, grinder.rect.y), (espresso_mach.rect.x, espresso_mach.rect.y), (water_boiler.rect.x, water_boiler.rect.y)]
        }
        with open(filename, 'w') as f:
            json.dump(data_to_save, f, indent=4)
            
        
    def load_game(self, filename):
        """Load the game state safely."""
        if not os.path.exists(filename):
            return None  # Return None so the menu knows it's empty
        try:
            with open(filename, 'r') as file:
                return json.load(file)
        except (json.JSONDecodeError, IOError):
            return None
            
    def reset_day(self, player):
        """Reset the game state for a new day within the same load."""
        self.money_earned_today = 0
        self.num_customers_today = 0
        self.customers_unhappy_today = 0
        player.x, player.y = 40, 600
        for machine in ALL_MACHINES:
            machine.state = "empty"

    def reset_new_game(self):
        """Reset the entire game state for starting a new game."""
        self.save_name = "Empty Slot"
        self.money = 0
        self.day_num = 1
        self.upgrades = [{"name": upgrade["name"], "cost": upgrade["cost"], "tier": upgrade["tier"], "purchased": False} for upgrade in self.upgrades]

        ALL_MACHINES = [grinder, espresso_mach, water_boiler]
        for machine in ALL_MACHINES:
            machine.state = "empty"
            machine.x = -300        # puts machine off screen until bought and placed by player, will change to actual position once placed.
            machine.y = 0

        """Reset the unlocked recipes list to only include starting recipes."""
        #RECIPES_UNLOCKED.clear()

        self.data = {
            "name": self.save_name,
            "money": self.money,
            "day_num": self.day_num,
            "upgrades": self.upgrades,
            "machine_positions": [(grinder.rect.x, grinder.rect.y), (espresso_mach.rect.x, espresso_mach.rect.y), (water_boiler.rect.x, water_boiler.rect.y)],
        }

        return self.data   # Return the reset data for any additional handling if needed

    def delete_save_file(self, save):
        """Delete the current save file if it exists."""
        if save is not None and os.path.exists(save["file"]):
            data = self.reset_new_game()  # Get the reset game data
            file = save["file"]
            with open(file, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Deleted save file: {save['file']}")
        else:
            print("No save file to delete.")


    def end_of_day_sequence(self, screen, font):

        screen.fill((0, 0, 0))
        details_text = font.render(f"Game Saved!End of Day {self.day_num-1} || Earned ${self.money_earned_today:.2f} || Total Customers: {self.num_customers_today} || Unhappy: {self.customers_unhappy_today}", True, (255, 255, 255))
        screen.blit(details_text, (constants.WIDTH // 2 - details_text.get_width() // 2, constants.HEIGHT // 2 - details_text.get_height() // 2))

        # updates data
        self.data = {
                "name": self.save_name,
                "money": self.money,
                "day_num": self.day_num,
                "upgrades": self.upgrades,
                "machine_positions": [(grinder.rect.x, grinder.rect.y), (espresso_mach.rect.x, espresso_mach.rect.y), (water_boiler.rect.x, water_boiler.rect.y)],
            }

        next_day_button.draw(screen)
        quit_button.draw(screen)
        


def main():
    global Customer, currentCust
    pygame.display.set_caption("Cafe")
    font = pygame.font.SysFont(None, 22)

    clock_font = pygame.font.SysFont(None, 45)
    clock = pygame.time.Clock()
    seconds_per_frame = TIME_SPEED / 60
    game_seconds = DAY_START  # Start day at 6:00 AM

    manager = GameManager()

    DebugMode = False
    GameState = "MENU_SCREEN"
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
    BOX_SPAWN_EVENT = pygame.USEREVENT + 2 #this will change once boxes spawn after being bought, for now they are automatic
    pygame.time.set_timer(BOX_SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)

        
    all_sprites = pygame.sprite.Group()
    customer_group = pygame.sprite.Group()

    # Player
    player = Player(40, 600, "player_idle_front")
    all_sprites.add(player)

    """for testing the minigame mode I'm defaulting the player with some ingredients"""
    player.inventory[0] = [water, water]
    player.inventory[1] = [bag_coffee_beans, bag_coffee_beans]
    is_dragging = False

    for recipe in ALL_RECIPES:
        if recipe.locked is False:
            RECIPES_UNLOCKED.append(recipe)

    running = True
    while running:
        screen.fill((0, 0, 0))
        keys = pygame.key.get_pressed()
        m_x, m_y = pygame.mouse.get_pos()

        # manages getting time each frame to make accurate clock for a 10 minutes cafe day
        if GameState == "PLAYING" and (ShopView == SHOP_VIEW_NONE and RecipeView == RECIPE_VIEW_NONE):
            game_seconds += seconds_per_frame
            if game_seconds >= REAL_DAY_SEC:
                game_seconds = 0
        hours = int(game_seconds // 3600)
        minutes = int((game_seconds % 3600) // 60)

        # Set the customer spawn timer to start at 8:00 AM and stop at 6:00 PM
        if int(game_seconds) == SEVEN_AM:
            pygame.time.set_timer(SPAWN_EVENT, CUSTOMER_SPAWN_EVERY_MS)
        if int(game_seconds) == DAY_END:
            pygame.time.set_timer(SPAWN_EVENT, 0)

        # checking for day end
        if int(game_seconds) >= DAY_END and GameState == "PLAYING":
            print(f"Day had ended {game_seconds}, {DAY_END}")
            GameState = "END_OF_DAY"
            pygame.mixer.music.load("Audio Files/end_of_day.mp3")
            pygame.mixer.music.play(-1)
            print("playing end of day music")
            manager.day_num += 1
            manager.end_of_day_sequence(screen, font)


        manager.money = 99999
        manager.update_message()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


            if manager.name_input_active:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(manager.name_input_text) > 0:
                            manager.save_name = manager.name_input_text
                            manager.name_input_active = False
                            GameState = "PLAYING"
                    elif event.key == pygame.K_BACKSPACE:
                        manager.name_input_text = manager.name_input_text[:-1]
                    elif event.key == pygame.K_ESCAPE:
                        manager.name_input_active = False 
                    else:
                        if len(manager.name_input_text) < 15:
                            manager.name_input_text += pygame.key.name(event.key)

                continue


            '''IMPORTANT: here is a spot to add key presses that do what you might need without having the logic behind it'''
            if DebugMode is True:
                if event.type == pygame.MOUSEMOTION:
                    #print(f"Mouse position: X={m_x}, Y={m_y}")
                    pass

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b:
                        print("Adding $8")
                        manager.money += 8
                        manager.money_earned_today += 8
                    if event.key == pygame.K_t:
                        game_seconds += 7200
                        print("Advancing 2 hours")
                    if event.key == pygame.K_y:
                        game_seconds += (DAY_END - 2000)  # Fast forward to end of day
                        print("Advancing to 5:55pm")


            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if event.button == 1 and GameState == "MENU_SCREEN":
                    if menu_start_button.is_clicked(event.pos):
                        GameState = "LOAD_MENU"
                    

                elif event.button == 1 and GameState == "LOAD_MENU" and GameState != "MENU_SCREEN":
                    def check_save(save, data):
                        if data is None or data.get("day_num", 1) == 1:
                            manager.reset_new_game()
                        else:
                            # Sync the manager's variables with the loaded file
                            manager.save_name = data.get("name", "Unnamed Save")
                            manager.money = loaded_data.get("money", 0)
                            manager.day_num = loaded_data.get("day_num", 1)
                            manager.upgrades = loaded_data.get("upgrades", manager.upgrades)
                        return save
                            
                    if save1_button.is_clicked(event.pos):
                        loaded_data = manager.load_game("save1.json")
                        save = check_save(save_game1, loaded_data)
                       
                    elif save2_button.is_clicked(event.pos):
                        loaded_data = manager.load_game("save2.json")
                        save = check_save(save_game2, loaded_data)
                        
                    elif save3_button.is_clicked(event.pos):
                        loaded_data = manager.load_game("save3.json")
                        save = check_save(save_game3, loaded_data)


                    if delete_save_button1.is_clicked(event.pos):
                        manager.delete_save_file(save_game1)
                        print("file deleted for slot 1")
                        break
                    elif delete_save_button2.is_clicked(event.pos):
                        manager.delete_save_file(save_game2)
                        print("file deleted for slot 2")
                        break 
                    elif delete_save_button3.is_clicked(event.pos):
                        manager.delete_save_file(save_game3)
                        print("file deleted for slot 3")
                        break
                        
                        
                    current_save_file = save
                    print(f"Current save file set to: {current_save_file}, data: {loaded_data}, GameState: {GameState}")

                    if loaded_data is None or loaded_data.get("day_num", 1) == 1:
                        manager.name_input_active = True
                    else:
                        GameState = "PLAYING"


                elif event.button == 1 and GameState == "PAUSED":
                    if pause_resume_button.is_clicked(event.pos):
                        GameState = "PLAYING"
                    elif pause_quit_button.is_clicked(event.pos):
                        GameState = "MENU_SCREEN"
                    continue


                # Shop mouse interaction. Handles tab switching, page arrows,
                # and item row purchases while the shop overlay is open. 
                # All click rects are redrawn each frame inside draw_shop_screen().
                if ShopView != SHOP_VIEW_NONE and event.button == 1:
                    # Tab clicks — switch the active tab and reset to first page
                    for tab_name, tab_rect in getattr(manager, "shop_tab_rects", {}).items():
                        if tab_rect.collidepoint(event.pos):
                            manager.active_tab = tab_name
                            manager.shop_page  = 0

                    # Left arrow — go to previous page if one exists
                    if (getattr(manager, "shop_arrow_left_rect", None) and
                            manager.shop_arrow_left_rect.collidepoint(event.pos) and
                            manager.shop_page > 0):
                        manager.shop_page -= 1

                    # Right arrow — go to next page if one exists
                    tab_items   = manager.shop_tabs[manager.active_tab]
                    total_pages = max(1, -(-len(tab_items) // manager.ITEMS_PER_PAGE))
                    if (getattr(manager, "shop_arrow_right_rect", None) and
                            manager.shop_arrow_right_rect.collidepoint(event.pos) and
                            manager.shop_page < total_pages - 1):
                        manager.shop_page += 1

                    # Item row clicks — attempt purchase of the clicked item.
                    # Uses shop_item_orig_idx because items are sorted (locked to bottom),
                    # so the page-local row index no longer matches the tab list index directly.
                    for row_i, item_rect in getattr(manager, "shop_item_rects", {}).items():
                        if item_rect.collidepoint(event.pos):
                            orig_index = manager.shop_item_orig_idx.get(row_i, row_i)
                            manager.buy_shop_item(manager.active_tab, orig_index, player)

                    continue  # Skip other click handling when interacting with the shop

                # Recipe Menu mouse interaction
                # Handles tab switching, page arrows, card clicks (view detail or
                # unlock), and detail view dismissal while the recipe overlay is open.
                # All click rects are redrawn each frame inside draw_recipe_screen().
                if RecipeView != RECIPE_VIEW_NONE and event.button == 1:
 
                    if RecipeView == RECIPE_VIEW_DETAIL:
                        # Any click outside the detail box closes the detail view
                        # and returns to the recipe menu
                        RecipeView = RECIPE_VIEW_MENU
                        manager.selected_recipe = None
 
                    elif RecipeView == RECIPE_VIEW_MENU:
                        # Tab clicks — switch active tab and reset to first page
                        for tab_name, tab_rect in getattr(manager, "recipe_tab_rects", {}).items():
                            if tab_rect.collidepoint(event.pos):
                                manager.recipe_active_tab = tab_name
                                manager.recipe_page       = 0
 
                        # Left arrow — previous page
                        if (getattr(manager, "recipe_arrow_left_rect", None) and
                                manager.recipe_arrow_left_rect.collidepoint(event.pos) and
                                manager.recipe_page > 0):
                            manager.recipe_page -= 1
 
                        # Right arrow — next page
                        if manager.recipe_active_tab == "Unlocked":
                            tab_recipes = list(RECIPES_UNLOCKED)
                        else:
                            tab_recipes = [r for r in ALL_RECIPES if r.locked]
                        cards_per_page = manager.recipe_cards_per_row * manager.recipe_rows_per_page
                        total_pages    = max(1, -(-len(tab_recipes) // cards_per_page))
                        if (getattr(manager, "recipe_arrow_right_rect", None) and
                                manager.recipe_arrow_right_rect.collidepoint(event.pos) and
                                manager.recipe_page < total_pages - 1):
                            manager.recipe_page += 1
 
                        # Card clicks
                        for card_i, card_rect in getattr(manager, "recipe_card_rects", {}).items():
                            if card_rect.collidepoint(event.pos):
                                recipe = manager.recipe_card_map.get(card_i)
                                if recipe is None:
                                    break
 
                                if manager.recipe_active_tab == "Unlocked":
                                    # Open the detail view for this recipe
                                    manager.selected_recipe = recipe
                                    RecipeView = RECIPE_VIEW_DETAIL
 
                                else:
                                    # Attempt to unlock the recipe for price * 2.5
                                    unlock_cost = recipe.price * 2.5
                                    if manager.money < unlock_cost:
                                        manager.set_message(f"Need ${unlock_cost:.2f} to unlock {recipe.name}!")
                                    else:
                                        manager.money  -= unlock_cost
                                        recipe.locked   = False
                                        RECIPES_UNLOCKED.append(recipe)
                                        manager.recipe_active_tab = "Unlocked"
                                        manager.recipe_page       = 0
                                        manager.set_message(f"Unlocked {recipe.name}!")
                                break
 
                    continue  # Skip other click handling when interacting with the recipe menu

                elif event.button == 1 and recipe_button.is_clicked(event.pos):
                    current_screen = "recipes"
                    RecipeView = RECIPE_VIEW_MENU

                elif event.button == 1 and shop_button.is_clicked(event.pos):
                    current_screen = "shop"
                    ShopView = SHOP_VIEW_MENU

                elif event.button == 1 and GameState == "END_OF_DAY":
                    if next_day_button.is_clicked(event.pos):
                        pygame.mixer.music.stop()
                        GameState = "PLAYING"
                        game_seconds = DAY_START
                        manager.reset_day(player)
                        customers.clear()
                        customersWaiting.clear()
                        manager.set_message(f"New Day | {manager.day_num}")
                        print(f"Starting next day, data: {manager.data}, GameState: {GameState}")
                    elif quit_button.is_clicked(event.pos):
                        pygame.mixer.music.stop()
                        GameState = "MENU_SCREEN"


                elif GameState == "MACHINE":
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

                elif CafeView == "BACKROOM":
                    #loops through all backroom objects looking for shelves
                    for obj in backroom_collisions:
                        #if shelf
                        if isinstance(obj, stockingShelf):
                            #check if player is colliding with shelf interaction zone
                            if player.get_foot_rect().colliderect(obj.interactionZone):
                                #loops through shelf spots of shelf
                                for shelfSpot in obj.spots:
                                    #players selected inventory slot item
                                    slot = player.inventory[player.selected_slot]
                                    #if player clicks on shelf spot
                                    mouse_pos = pygame.mouse.get_pos()
                                    if shelfSpot.rect.collidepoint(mouse_pos) and event.button == 1:
                                        #if slot has items and items are ingredient voxes, store ingredient box
                                        if len(slot) != 0 and isinstance(slot[0], ingredientBox):
                                            shelfSpot.storeIngredientBox(player)
                                        #else if selected slot is an ingredient
                                        elif shelfSpot.held_ingredient_box != None:
                                            shelfSpot.held_ingredient_box.grabIngredient(player)


            if event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                if active_machine and active_machine.ingredient and (active_machine.state == "empty" or active_machine.state == "error"):
                    if active_machine.mg_interaction_zone.colliderect(active_machine.ingredient_rect):
                        active_machine.add(active_machine.ingredient, player)


            if event.type == pygame.KEYDOWN:

                if GameState == "PLAYING" and not active_machine:
                    if event.key == pygame.K_1:
                        player.selected_slot = 0
                    elif event.key == pygame.K_2:
                        player.selected_slot = 1
                    elif event.key == pygame.K_3:
                        player.selected_slot = 2
                    elif event.key == pygame.K_4:
                        player.selected_slot = 3

                if event.key == pygame.K_0:
                    if DebugMode is False:
                        DebugMode = True
                    else:
                        DebugMode = False

                if event.key == pygame.K_r:  # R clears the customers for testing
                    customers.clear()
                    customersWaiting.clear()
                    manager.clear_round_state()
                    Register.customer_waiting = False
                    currentCust = None

                if event.key == pygame.K_p and GameState == "PLAYING":
                    GameState = "PAUSED"

                if event.key == pygame.K_q and GameState=="PLAYING":
                    if CafeView == "FRONT":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 20, 520
                        manager.change_counters_pos(CafeView)
                    elif CafeView == "MIDDLE":
                        CafeView = "FRONT"
                        player.rect.x, player.rect.y = 1005, 520
                        manager.change_counters_pos(CafeView)

                if event.key == pygame.K_f:
                    if player.get_foot_rect().colliderect(sink.interaction_zone) and CafeView == "MIDDLE":
                        result = player.add_item_to_inv(water, Ingredient)
                        if result is True:
                            manager.set_message("Collected water!")
                        else:
                            manager.set_message("Cannot collect water: Inventory Full")

                # if player presses e inside registers collision zone, and there is a customer, take order
                if event.key == pygame.K_e:
                    if player.get_foot_rect().colliderect(register1.interaction_zone) and register1.customer_waiting and CafeView == "FRONT":
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(register2.interaction_zone) and register2.customer_waiting and CafeView == "MIDDLE":
                        GameState = "REGISTER"
                    elif player.get_foot_rect().colliderect(doorEntry) and GameState == "PLAYING" and CafeView == "MIDDLE":
                        CafeView = "BACKROOM"
                        player.rect.x, player.rect.y = 30, 490
                    elif player.get_foot_rect().colliderect(doorEntry2) and CafeView == "BACKROOM":
                        CafeView = "MIDDLE"
                        player.rect.x, player.rect.y = 30, 115
                      
                    elif player.get_foot_rect().colliderect(sink.interaction_zone) and CafeView == "MIDDLE":
                        result = sink.clear_cup(player)
                        if result is True:
                            manager.set_message("Cup emptied!")
                        else:
                            manager.set_message("No cup with contents selected to clear!")

                    elif CafeView == "FRONT" and len(manager.active_orders) > 0:
                        nearby = manager.get_nearby_seated_customer(player, customers)
                        if nearby and nearby.state == "seated":
                            customer_order = nearby.ordered_item
                            if len(player.inventory[player.selected_slot]) > 0 and type(player.inventory[player.selected_slot][0]) == Cup:
                                player_hand = player.inventory[player.selected_slot][0]
                                if customer_order.check_match(player_hand) is True:
                                    base_pay, tip, total = nearby.calculate_tip()
                                    manager.money += total
                                    manager.money_earned_today += total  
                                    manager.set_message(f"Delivered! ${base_pay:.2f} + ${tip:.2f} tip = ${total:.2f}", 2500)
                                    nearby.start_drinking("correct")
                                else:
                                    nearby.start_drinking("incorrect")
                                    manager.set_message("Customer rejected the order!", 2500)
                                    manager.customers_unhappy_today += 1

                                manager.active_orders.remove(customer_order)
                                player.inventory[player.selected_slot].pop(0) 


                    elif GameState == "MACHINE" and active_machine:
                        if active_machine.state == "ready":
                            result = active_machine.remove_output()
                            if result:
                                curr_slot = player.inventory[player.selected_slot]
                                # also check if the spot has a cup or if the spot is full already
                                if len(curr_slot) > 0: 
                                    if type(curr_slot[0]) == Cup: 
                                        cup = curr_slot[0]
                                        print("player holding a cup")

                                        if cup.contents:
                                            print("cup has something in it already")
                                            if result.an_input is False:
                                                # adding check for max_capacity
                                                if len(cup.contents) < cup.max_capacity:
                                                    print("ingredient added to current cup")
                                                    cup.contents.append(result)
                                                    cup.update()
                                                else:
                                                    manager.set_message("Output cannot be collected: Cup is Full Capacity")
                                                    active_machine.state = "ready" 
                                                    active_machine.contents.append(result) #add the result back to the machine since it couldn't be collected
                                            else:
                                                if player.add_item_to_inv(result, Ingredient) is False:
                                                    active_machine.state = "ready"  
                                                    active_machine.contents.append(result)
                                                    manager.set_message("Output cannot be collected: Must Use A Cup")
                                        else:
                                            print("trying to add to empty cup")
                                            if result.an_input is False:
                                                pulled_cup = curr_slot.pop(0) #pull the cup out of the inventory
                                                #pulled_cup = copy.deepcopy(pulled_cup)
                                                pulled_cup.contents.append(result) #add the machine output to the cup's contents
                                                pulled_cup.update()
                                                print("pulled cup:", pulled_cup.name, "with contents:", [o.name for o in pulled_cup.contents], pulled_cup.stackable)
                                                
                                                if player.add_item_to_inv(pulled_cup, Cup) is False:
                                                    manager.set_message("Output cannot be collected: Inventory Full")
                                                    pulled_cup.contents.remove(result) #remove the machine output from the cup's contents since it can't be added to inventory
                                                    pulled_cup.update()
                                                    curr_slot.append(pulled_cup) #add the cup back to the inventory
                                                    active_machine.state = "ready" 
                                                    active_machine.contents.append(result) #add the result back to the machine since it couldn't be collected
                                            else:
                                                manager.set_message("Output cannot be collected with a cup.")
                                                active_machine.state = "ready" 
                                                active_machine.contents.append(result)
        

                                    elif isinstance(curr_slot[0], Ingredient):
                                            print("player holding an ingredient:", curr_slot[0].name)
                                            if result.an_input is True:
                                                print(f'{result.name}, {result.an_input}')
                                                if player.add_item_to_inv(result, Ingredient) is False:
                                                    active_machine.set_state("ready")  
                                                    active_machine.contents.append(result)
                                                    manager.set_message("Output cannot be collected: Inventory Full")
                                            else:
                                                print(f'{result.name}, {result.an_input}')
                                                active_machine.state = "ready"
                                                active_machine.contents.append(result)
                                                manager.set_message("Output cannot be collected: Must Use A Cup")
                                    else:
                                        print("player holding something else")

                                else:
                                    print("player holding nothing. Result:", result.name, result.an_input)
                                    if result.an_input is True:
                                        player.add_item_to_inv(result, Ingredient)
                                        print("added to empty")
                                    else: 
                                        print("could not add to empty")
                                        manager.set_message("Output cannot be collected: Must Use A Cup")
                                        active_machine.state = "ready"
                                        active_machine.contents.append(result)
                                    

                            if not active_machine.contents:
                                active_machine.state = "empty"


                    elif CafeView == "MIDDLE" and GameState == "PLAYING":
                        for m in machines:
                            if m.is_player_nearby(player):
                                active_machine = m
                                active_machine.setup_minigame(player.inventory[player.selected_slot])
                                GameState = "MACHINE"
                                break

                    #checking if e was pressed in any backroom box collision zones
                    elif CafeView == "BACKROOM" and GameState == "PLAYING":
                        print("checking backroom interactions")
                        for i in range(len(ingredientBoxes)):
                            #Finds each ingredient box instance and checks for collision with interaction_zone
                            if ingredientBoxes[i] != None:
                                if player.get_foot_rect().colliderect(ingredientBoxes[i].interactionZone):
                                    #grabs corresponding box and adds it to first open hot bar slot
                                    result = player.add_item_to_inv(ingredientBoxes[i], ingredientBox)
                                    if result is True:
                                        ingredientBox.popBox(ingredientBoxes[i], ingredientBoxes, backroom_collisions)
                                        numBoxes -= 1
                                    else:
                                        manager.set_message("Cannot pick up box: Inventory Full")

                if event.key == pygame.K_ESCAPE:
                    if GameState == "MENU_SCREEN":
                        continue
                    if RecipeView != RECIPE_VIEW_NONE:
                        if RecipeView == RECIPE_VIEW_DETAIL:
                            # ESC from detail view returns to the recipe menu, not all the way out
                            RecipeView = RECIPE_VIEW_MENU
                            manager.selected_recipe = None
                        else:
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
                    if GameState == "PAUSED":
                        GameState = "PLAYING"
                        continue
                    if GameState == "PLAYING":
                        GameState = "PAUSED"
                        continue

                if event.key == pygame.K_s and GameState == "REGISTER":
                    if currentCust is None:
                        GameState = "PLAYING"
                        continue

                    active_count = sum(1 for o in manager.active_orders if o is not None)
                    if active_count >= manager.max_orders:
                        manager.set_message(f"Can't take more than {manager.max_orders} orders at once!")
                        GameState = "PLAYING"
                        continue

                    manager.active_orders.insert(0, currentCust.ordered_item)

                    seat = manager.findFirstOpen(seats)  # find open seat
                    if seat is None:
                        manager.set_message("No open seats available")
                        continue

                    # If the order could not be accepted because cup slots are full,
                    # keep the customer at the register and undo the seat reservation.
                    if currentCust.ordered_item is None:
                        seat.open_seat()
                        currentCust.target_seat = None
                        currentCust.seat_number = None
                        currentCust.target_position = None
                        currentCust.set_state("waiting")
                        continue
                    else:
                        seat.reserve_seat(currentCust)
                        currentCust.set_target_seat(seat)
                        currentCust.set_state("walking to table")

                        # When taking an order, create a cup object, then add it.
                        new_cup_instance = Cup(["cup", "cup_w_lid"])
                        player.add_item_to_inv(new_cup_instance, Cup)

                        # Remove from line.
                        if len(customersWaiting) > 0:
                            customersWaiting.pop(0)
                        # Move remaining customers up in line.
                        for i in range(len(customersWaiting)):
                            customersWaiting[i].state = "moving up in line"
                            customersWaiting[i].line_position = LINE_POSITIONS[i]
                        # Update current front-of-line customer.
                        if len(customersWaiting) > 0:
                            currentCust = customersWaiting[0]
                        else:
                            currentCust = None
                            Register.customer_waiting = False

                    GameState = "PLAYING"

                # Pause normal gameplay input while a menu is open
                if RecipeView != RECIPE_VIEW_NONE or ShopView != SHOP_VIEW_NONE:
                    continue


            if event.type == SPAWN_EVENT and GameState not in ("MENU_SCREEN", "PAUSED"):
                # if wait line is not current full and total customers not at max, spawn new customer
                if (len(customers) < MAX_CUSTOMERS and len(customersWaiting) < MAX_CUSTOMERS_WAITING and RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE):

                    # Calculate the index for the new customer
                    index = len(customersWaiting)
                    spawn_x = CUSTOMER_ENTRY_X
                    spawn_y = CUSTOMER_ENTRY_Y

                    # Create the customer using the key "customer" from your IMAGE_LIBRARY
                    '''Each customer we design will have a list of image keys. Eventually we will have s system to make
                    different customers spawn so when a customer is created here, it would not be defaultly set to the ladybug.'''
                    currCustomer = Customer(spawn_x, spawn_y, ["ladybug_idle", "ladybug_sitting"], RECIPES_UNLOCKED,
                                            line_position=LINE_POSITIONS[index])
                    manager.num_customers_today += 1
                    
                    currCustomer.set_state("walking to line")
                    if index == 0:
                        currentCust = currCustomer

                    all_sprites.add(currCustomer)
                    customer_group.add(currCustomer)

                    customers.append(currCustomer)
                    customersWaiting.append(currCustomer)

            if event.type == BOX_SPAWN_EVENT and GameState not in ("MENU_SCREEN", "PAUSED"):
                # if ingredient spots open, spawn random ingredient box
                if numBoxes < MAX_INGREDIENT_BOXES:
                    for i in range(MAX_INGREDIENT_BOXES):
                        if ingredientBoxes[i] is None:
                            x, y = BOX_POSITIONS[i]
                            ingredBox = ingredientBox(x, y, ingredientBox.pickIngredient(INGREDIENTS))
                            ingredientBoxes[i] = ingredBox
                            backroom_collisions.append(ingredBox)
                            numBoxes += 1
                            break

        if RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE and GameState not in ("MENU_SCREEN", "PAUSED"):
            for c in customers:
                c.update(seats)

        if GameState not in ("MENU_SCREEN", "PAUSED"):
            manager.cleanup_gone_customers(customers, customersWaiting, all_sprites, customer_group, manager)

        if GameState == "MENU_SCREEN":
            manager.draw_menu_screen(screen)

        elif GameState == "LOAD_MENU":
            manager.draw_load_menu(screen)

        elif GameState == "END_OF_DAY":
            manager.save_game(current_save_file["file"])
            manager.end_of_day_sequence(screen, font)

        elif GameState == "PAUSED":
            frozen_keys = {k: False for k in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_ESCAPE]}  # no inputs while paused
            if CafeView == "FRONT":
                manager.front_view_rendering(player, customers, font, frozen_keys, DebugMode)
            elif CafeView == "MIDDLE":
                manager.middle_view_rendering(player, font, frozen_keys, DebugMode)
            else:
                manager.back_view_rendering(player, font, frozen_keys, DebugMode)
            manager.draw_pause_menu(screen)

        elif GameState == "PLAYING":
            if RecipeView != RECIPE_VIEW_NONE:
                manager.draw_recipe_screen(screen)
                # Detail view draws on top of the recipe menu
                if RecipeView == RECIPE_VIEW_DETAIL:
                    manager.draw_recipe_detail(screen)
            elif ShopView != SHOP_VIEW_NONE:
                manager.draw_shop_screen(screen)
            else:
                if CafeView == "FRONT":
                    manager.front_view_rendering(player, customers, font, keys, DebugMode)
                elif CafeView == "MIDDLE":
                    manager.middle_view_rendering(player, font, keys, DebugMode)
                else:
                    manager.back_view_rendering(player,font, keys, DebugMode)

        elif GameState == "REGISTER":
            register1.take_order(screen, currentCust)

        elif GameState == "MACHINE" and active_machine:
            active_machine.mini_game_mode(screen, DebugMode, font)
            if is_dragging:
                active_machine.ingredient_rect.center = (m_x, m_y)
                active_machine.ingredient.x = active_machine.ingredient_rect.x
                active_machine.ingredient.y = active_machine.ingredient_rect.y

        # checking for prompt name box at start of new save
        if manager.name_input_active:
            pygame.draw.rect(screen, (50, 50, 50), manager.name_input_box) # Dark grey box
            pygame.draw.rect(screen, (0, 255, 255), manager.name_input_box, 2) # Cyan border

            if len(manager.name_input_text) == 0:
                prompt_surface = font.render(manager.name_prompt, True, (255, 255, 255))
                screen.blit(prompt_surface, (manager.name_input_box.x + 5, manager.name_input_box.y + 5))

            name_surface = font.render(manager.name_input_text, True, (255, 255, 255))
            screen.blit(name_surface, (manager.name_input_box.x + 5, manager.name_input_box.y + 5))

        # Update machine timers every frame regardless of game state
        for m in machines:
            m.update()

        if currentCust != None and currentCust.state == "waiting" and GameState == "PLAYING":
            register1.set_waiting()

        clock.tick(FPS)

        # Handles all text + rendering (skip HUD on menu/pause)
        if GameState not in ("MENU_SCREEN","PAUSED", "LOAD_MENU"):
            for item in manager.active_orders:
                if item is None:
                    manager.active_orders.remove(item)
            orders_text = font.render(f'Orders: {', '.join(o.name for o in manager.active_orders)}', True, (250, 0, 0), (255, 255, 255))
            clock_text = clock_font.render(manager.handle_time(hours, minutes), True, 'black')
            screen.blit(orders_text, (10, 25))
            screen.blit(clock_text, (1202, 35))
            if DebugMode is True:
                text = font.render(f"Customers: {len(customers)} | R to clear Customers | FPS: {clock.get_fps()} | GameState: {GameState}", True, (230, 230, 230))
                screen.blit(text, (10, 10))

        if (GameState == "PLAYING" and RecipeView == RECIPE_VIEW_NONE and ShopView == SHOP_VIEW_NONE):
            manager.draw_money(screen, font)


        manager.draw_message(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()