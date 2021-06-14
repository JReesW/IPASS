import pygame

# This module contains elements used by the UI (buttons, etc.)


pygame.freetype.init()
regularfont = pygame.freetype.SysFont('Mono', 20)
titlefont = pygame.freetype.Font("schoolgirls.otf", 60)


# Class representing a clickable button
class Button:
    def __init__(self, rect, text, funcs, args, scene):
        self.rect = rect
        self.text = text
        self.color = (40, 40, 40)
        self.bordercolor = (255, 255, 0)
        self.textcolor = (255, 255, 0)
        self.funcs = funcs
        self.args = args
        self.scene = scene

    # Change color on hover
    def hover(self, mousepos):
        if self.rect.collidepoint(mousepos):
            # Become darker when mouse is hovering over button
            self.color = tuple([self.color[i] - 2 if self.color[i] > 20 else self.color[i] for i in range(3)])
        else:
            # Become lighter when no mouse is hovering over button
            self.color = tuple([self.color[i] + 2 if self.color[i] < 40 else self.color[i] for i in range(3)])

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

    def handle_events(self, events):
        mousepos = pygame.mouse.get_pos()

        self.hover(mousepos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mousepos):
                    for func in self.funcs:
                        self.scene.execute(func, self.args)


class TextBox:
    def __init__(self, rect):
        self.rect = rect
        self.text = ""
        self.active = False
        self.buffer = 0

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
                    elif event.key != pygame.K_BACKSPACE:
                        self.text += event.unicode

        if pygame.key.get_pressed()[pygame.K_BACKSPACE] and self.active:
            if self.buffer == 0:
                self.text = self.text[:-1]
                self.buffer = 1
            else:
                self.buffer += 1
                if self.buffer > 40 and self.buffer % 3 == 0:
                    self.text = self.text[:-1]
        else:
            self.buffer = 0


class Table:
    def __init__(self, rect):
        self.rect = rect
        self.entries = {}

    def add_entry(self, entry):
        self.entries[entry] = entry

    def remove_entry(self, entry):
        del self.entries[entry]

    def render(self):
        surface = pygame.Surface(self.rect.size)

        pygame.draw.rect(surface, (40, 40, 40), pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)
        pygame.draw.rect(surface, (255, 255, 0), pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        return surface

    def handle_events(self, events):
        pass
