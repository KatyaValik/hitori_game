import pygame
import config as c


class Button:
    def __init__(self, x, y, width, height, color, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.font = self.font = pygame.font.Font(None, 21)
        self.txt_surface = self.font.render(text, True, (0, 0, 0))
        self.count = 0
        self.solve = False

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.text == 'increase the field size':
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.count += 1
            if self.text == 'solve':
                if self.rect.collidepoint(event.pos):
                    self.solve = True

    def update(self):
        pass