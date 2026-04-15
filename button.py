from constants import *

class Button:
    """
    A clickable UI element used for navigation or triggering game actions.
    
    This class handles rendering text on a rectangle and detecting mouse 
    interactions for state changes.
    """
    def __init__(self, x, y, width, height, text, target_state, action):
        """
        Initializes the button with its position, dimensions, and behavior.
        
        Args:
            x (int): Horizontal position of the button.
            y (int): Vertical position of the button.
            width (int): Width of the button rectangle.
            height (int): Height of the button rectangle.
            text (str): The label displayed on the button.
            target_state (str): The game state to transition to when clicked.
            action (function): A callback function to execute on click.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.target_state = target_state
        self.font = pygame.font.SysFont(None, 22)

        self.color = WHITE
        self.hover_color = (200, 200, 200)
        self.text_color = BLACK
        self.action = action

    def is_clicked(self, mouse_pos):
        """Checks if a given mouse position is within the button's boundaries."""
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        """
        Renders the button to the screen, changing color if the mouse is hovering.
        
        Args:
            screen (pygame.Surface): The display surface to draw on.
        """
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, current_state):
        """
        Processes mouse events to determine if the button was clicked.
        
        Returns the target_state if clicked, otherwise returns the current_state.
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.target_state

        return current_state