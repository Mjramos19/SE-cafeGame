from constants import *

class Register(Counter):
    """
    A specialized Counter that handles order-taking and customer queue logic.
    
    Attributes:
        interactionZone (pygame.Rect): The area where the player can trigger interaction.
        icon (pygame.Surface): The visual indicator for a waiting customer.
    """
    # this variable is shared amongst both register objects
    customerWaiting = False
    def __init__(self, x, y, iz_y, w=150, h=90): #will need to update and put a parameter for the current customer image key to be passed through.
        super().__init__(x, y, w, h, REGISTER_COLOR)
        self.placeable = False

        # interaction box for register
        self.interactionZone = pygame.Rect(self.rect.x, self.rect.y + iz_y, self.rect.w, self.rect.h)

        self.icon = IMAGE_LIBRARY["register_icon"]
        self.icon_rect = self.icon.get_rect(topleft=(x+55, y-85))

        # order screen variables
        self.order_screen = IMAGE_LIBRARY["order_screen"]
        self.customer_image = IMAGE_LIBRARY["ladybug_register"] #place holder until parameter is updated.
        self.customer_rect = pygame.Rect(500,75,200,418)


    def setWaiting(self):
        """Sets the shared customerWaiting flag to True."""
        Register.customerWaiting = True

    def take_order(self, screen, currentCust=None):
        """
        Draws the register order-taking screen and UI elements.
        
        Args:
            screen (pygame.Surface): The display surface.
            currentCust (Customer): The customer being served.
        """

        # to do: learn to crop customer to rectangle
        screen.blit(self.order_screen, (0,0))
        screen.blit(self.customer_image, self.customer_rect)

        # Fonts for register UI text
        title_font = pygame.font.SysFont(None, 36)
        body_font = pygame.font.SysFont(None, 28)

        # Main Title
        title_text = title_font.render("Register - Accepting an order gives you an empty cup", True, WHITE)
        screen.blit(title_text, (80, 70))

        # Show current customer order if available
        order_name = "???"
        if currentCust is not None and currentCust.orderedItem is not None:
            order_name = currentCust.orderedItem.get_name()
        
        # Speech buubble position - to the left of the customer
        bubble_x, bubble_y = 60, 100
        bubble_w, bubble_h = 420, 120

        # Draw bubble background
        pygame.draw.rect(screen, WHITE, (bubble_x, bubble_y, bubble_w, bubble_h), border_radius=20)

        # Draw tail pointing toward customer
        tail_points = [(bubble_x + bubble_w - 60, bubble_y + bubble_h),
                    (bubble_x + bubble_w + 20, bubble_y + bubble_h + 60),
                    (bubble_x + bubble_w - 120, bubble_y + bubble_h)]
        pygame.draw.polygon(screen, WHITE, tail_points)

        # Order text inside the bubble
        order_text = title_font.render(f"I want an {order_name}!", True, BLACK)
        screen.blit(order_text, (bubble_x + 20, bubble_y + 20))

        hint_text = body_font.render("...please :)", True, (80, 80, 80))
        screen.blit(hint_text, (bubble_x + 20, bubble_y + 65))
        # Control hints
        hint_accept = body_font.render("[S] Accept Order", True, WHITE)
        hint_close = body_font.render("[ESC] Leave Register", True, WHITE)

        screen.blit(hint_accept, (80, 300))
        screen.blit(hint_close, (80, 340))


    def render(self, screen):
        """Renders the register icon in the game world."""
        if Register.customerWaiting == True:
            screen.blit(self.icon, self.icon_rect)


class Sink(Counter):
    """
    A specialized Counter that handles clearing the player's inventory cup.
    
    Attributes:
        interactionZone (pygame.Rect): Area where player can interact with the sink.
    """
    def __init__(self, x, y):
        super().__init__(x, y)
        self.placeable = False

        self.interactionZone = pygame.Rect(self.rect.x, self.rect.y + 100, self.rect.w, self.rect.h)

    def clear_cup(self, player):
        """
        Empties the cup in the player's active inventory slot.
        
        Args:
            player (Player): The player instance performing the action.
        """
        curr_slot = player.inventory[player.selectedSlot]
        if curr_slot and isinstance(curr_slot[0], Cup) and curr_slot[0].contents:
            cup_to_clear = curr_slot.pop()

            #cup_to_clear = copy.deepcopy(cup_to_clear)  # Creates a new instance to avoid mutating the original cup in the inventory
            cup_to_clear.contents.clear()
            cup_to_clear.update()
            print(f'{cup_to_clear}')
            added = player.addInventoryItem(cup_to_clear, Cup)
            if not added:
                player.inventory[player.selectedSlot].append(cup_to_clear)
            return True
        return False   
    
    def is_player_nearby(self, player):
        """Checks if the player is within range of the sink."""
        return player.get_foot_rect().colliderect(self.interactionZone)

    def render(self, screen, debugmode):
        """Renders the sink unit visuals."""
        if debugmode == True:
            pygame.draw.rect(screen, WHITE, self.rect) 
            pygame.draw.rect(screen, (0, 0, 255), self.interactionZone, 2)
