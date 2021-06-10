import pygame

# This module contains elements used by the UI (buttons, etc.)


pygame.freetype.init()
regularfont = pygame.freetype.SysFont('Mono', 20)
titlefont = pygame.freetype.Font("schoolgirls.otf", 60)


# Class representing a clickable button
class Button:
    def __init__(self, rect, text, funcs, args):
        self.rect = rect
        self.text = text
        self.color = (0, 0, 0)
        self.bordercolor = (255, 255, 0)
        self.textcolor = (255, 255, 0)
        self.funcs = funcs
        self.args = args

    # Change color on hover
    def hover(self, mousepos):
        if self.rect.collidepoint(mousepos):
            # Become darker when mouse is hovering over button
            self.color = tuple([self.color[i] - 2 if self.color[i] > 0 else self.color[i] for i in range(3)])
        else:
            # Become lighter when no mouse is hovering over button
            self.color = tuple([self.color[i] + 2 if self.color[i] < 20 else self.color[i] for i in range(3)])

    # Draw the button
    def render(self):
        surface = pygame.Surface(self.rect.size)

        # Background and border
        pygame.draw.rect(surface, self.color, pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)
        pygame.draw.rect(surface, self.bordercolor, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        # Text
        text, rect = regularfont.render(self.text, self.textcolor)
        surface.blit(text, (surface.get_width() // 2 - rect.width // 2, 10))

        return surface


class TextBox:
    def __init__(self, rect):
        self.rect = rect
        self.text = ""
        self.active = False

    def render(self):
        surface = pygame.Surface(self.rect.size)

        # Background and border
        bordercolor = (180, 140, 255) if self.active else (20, 20, 20)
        pygame.draw.rect(surface, (220, 220, 220), pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)
        pygame.draw.rect(surface, bordercolor, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        # Text
        text, rect = regularfont.render(self.text, (0, 0, 0))
        surface.blit(text, (10, 10))

        return surface

    def handle_events(self, events):
        mousepos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.active =  self.rect.collidepoint(mousepos)

            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode