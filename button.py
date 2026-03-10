import pygame


class Button:
    def __init__(self, x, y, width, height, text, target_state, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.target_state = target_state
        self.font = pygame.font.SysFont(None, 22)



        self.color = (180, 180, 180)
        self.hover_color = (220, 220, 220)
        self.text_color = (0, 0, 0)
        self.action = action

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event, current_state):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return self.target_state

        return current_state
