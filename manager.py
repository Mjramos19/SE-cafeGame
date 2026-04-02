from game import *
from machines import *
import constants
from recipes import *
from constants import *
from backroom import *
from button import *

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
        self.active_orders = []
        self.max_orders = 2 # Upgradable via shop later
        self.more_hands_tier = 0 # 0 = none bought, max = 3

        # Placeholder progression systems for Phase 3
        self.upgrades = [
            {"name": "More Hands I",   "cost": 50,  "tier": 1, "purchased": False},
            {"name": "More Hands II",  "cost": 100, "tier": 2, "purchased": False},
            {"name": "More Hands III", "cost": 150, "tier": 3, "purchased": False},
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
        Attempt to buy a placeholder upgrade.

        Parameters:
            upgrade_index (int): The index of the upgrade in the list.
        """
        if not (0 <= upgrade_index < len(self.upgrades)):
            return

        upgrade = self.upgrades[upgrade_index]

        if upgrade["purchased"]:
            self.set_message("Already purchased!")
            return

        # Must buy previous tier first
        if upgrade["tier"] > 1:
            prev = self.upgrades[upgrade_index - 1]
            if not prev["purchased"]:
                self.set_message(f"Unlock {prev['name']} first!")
                return

        if self.money < upgrade["cost"]:
            self.set_message(f"Need ${upgrade['cost']:.2f} - not enough money!")
            return

        self.money -= upgrade["cost"]
        upgrade["purchased"] = True
        self.more_hands_tier += 1
        self.max_orders += 2
        self.set_message(f"Purchased {upgrade['name']}! Max orders: {self.max_orders}")

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
            if customer.orderedItem is not None:
                for i in range(len(manager.active_orders)):
                    if manager.active_orders[i] is customer.orderedItem:
                        manager.active_orders[i] = None
                        break
                customer.orderedItem = None

        # Recalculate the current waiting customer.
        if len(customersWaiting) > 0:
            currentCust = customersWaiting[0]
        else:
            currentCust = None
            Register.customerWaiting = False

    def drawHotBar(self, player, font):
        player.updateInventoryLengths()
        for i in range(NUM_SLOTS):
            # makes rectangle object for that inventory slot at corresponding inventory position
            slot = pygame.Rect(INVENTORY_POSITIONS[i][0], INVENTORY_POSITIONS[i][1], SLOT_SIZE, SLOT_SIZE)

            # draws the grey slot background at that spot
            pygame.draw.rect(screen, (40, 40, 40), slot)

            quantNum = font.render(f"{player.inventoryQuants[i]}", True, (255, 255, 255))
            screen.blit(quantNum, (INVENTORY_POSITIONS[i][0] + 5, INVENTORY_POSITIONS[i][1] + 5))


            # if that inventory slot has an item, draw that icon inside
            if len(player.inventory[i]) > 0:
                # placeholder for item pictures
                tempItemPic = pygame.Rect(slot.center[0], slot.center[1], 10, 10)
                pygame.draw.rect(screen, (255, 0, 0), tempItemPic)

            # if that inventory slot is selected, draw thick white border, else: draw thin black border
            if i == player.selectedSlot:
                pygame.draw.rect(screen, (255, 255, 255), slot, 3)
            else:
                pygame.draw.rect(screen, (0, 0, 0), slot, 2)

            # if the players mouse is hovering over a slot that isn't empty, display that items name next to the slot
            m_x, m_y = pygame.mouse.get_pos()
            if slot.collidepoint((m_x, m_y)):
                if player.inventory[i] != None:
                    spot_list = player.inventory[i]
                    if len(spot_list) > 0:
                        if spot_list[0].name != "Cup":
                            screen.blit(font.render(f'{spot_list[0].name}', True, (0, 0, 0), (255, 255, 255)), (slot.x + 60, slot.y + 15))
                        else:
                            if spot_list[0].stackable == True:
                                text = font.render("Empty Cup", True, (0, 0, 0), (255, 255, 255))
                                screen.blit(text, (slot.x + 60, slot.y + 15))
                            else:
                                text = font.render(f'Cup with {", ".join(o.name for o in spot_list[0].contents)}', True, (0, 0, 0), (255, 255, 255))
                                screen.blit(text, (slot.x + 60, slot.y + 15))

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
        overlay = pygame.Surface((700, 460))
        overlay.set_alpha(235)
        overlay.fill((25, 25, 25))

        box_x = constants.WIDTH // 2 - 350
        box_y = constants.HEIGHT // 2 - 230
        screen.blit(overlay, (box_x, box_y))
        pygame.draw.rect(screen, constants.WHITE, (box_x, box_y, 700, 460), 3)

        title_font = pygame.font.SysFont(None, 42)
        body_font  = pygame.font.SysFont(None, 28)
        small_font = pygame.font.SysFont(None, 22)

        title = title_font.render("Shop / Upgrades", True, constants.WHITE)
        screen.blit(title, (box_x + 20, box_y + 20))

        money_text = body_font.render(f"Money: ${self.money:.2f}", True, constants.WHITE)
        screen.blit(money_text, (box_x + 20, box_y + 65))

        orders_text = small_font.render(f"Current max orders: {self.max_orders}", True, constants.WHITE)
        screen.blit(orders_text, (box_x + 20, box_y + 95))

        hint = small_font.render("Press ESC to close  |  Press 1, 2, 3 to buy", True, constants.WHITE)
        screen.blit(hint, (box_x + 20, box_y + 125))

        item_y = box_y + 170
        for i, upgrade in enumerate(self.upgrades):
            # Locked if previous tier not bought yet
            locked = upgrade["tier"] > 1 and not self.upgrades[i - 1]["purchased"]

            if upgrade["purchased"]:
                status = "OWNED"
                color = constants.GREEN
            elif locked:
                status = "LOCKED"
                color = (120, 120, 120)
            else:
                status = f"${upgrade['cost']:.2f}"
                color = constants.WHITE

            line = body_font.render(
                f"[{i + 1}] {upgrade['name']} (+2 max orders) - {status}",
                True, color
            )
            screen.blit(line, (box_x + 30, item_y))
            item_y += 55

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
        menu_load_button.draw(screen)

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
            if c.orderedItem is not None and (c.state == "finding seat" or c.state == "seated"):
                order_text = font.render(f"{c.orderedItem.get_name()}", True, (255, 255, 255), (0, 0, 0))
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
