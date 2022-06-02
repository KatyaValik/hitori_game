import pygame
import config as c


class InputBox:
    def __init__(self, x, y, w, h, field_size, text=''):
        self.font = pygame.font.Font(None, 40)
        self.rect = pygame.Rect(x, y, w, h)
        self.color = c.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.font.render(text, True, self.color)
        self.active = False
        self.field_size = field_size
        self.mark = None
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = c.COLOR_ACTIVE if self.active else c.COLOR_INACTIVE
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    x = int(self.text + event.unicode)
                    if x <= self.field_size:
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        pass

    def draw(self, surface):
        if self.mark is None:
            # Blit the text.
            surface.blit(self.txt_surface, (self.rect.x+10, self.rect.y+10))
            # Blit the rect.
            pygame.draw.rect(surface, self.color, self.rect, 2)
        else:
            if self.mark == 'dark':
                rect = pygame.Rect(self.x, self.y, self.w, self.h)
                pygame.draw.rect(surface, (0, 0, 0), rect)
            elif self.mark == 'circle':
                surface.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
                pygame.draw.rect(surface, self.color, self.rect, 2)
            elif self.mark == 'blank':
                rect = pygame.Rect(self.x, self.y, self.w, self.h)
                pygame.draw.rect(surface, (255, 255, 255), rect)

                