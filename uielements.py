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
        self.scroll = 0

    def add_entry(self, entry):
        self.entries[entry] = entry

    def remove_entry(self, entry):
        del self.entries[entry]

    def render(self):
        surface = pygame.Surface(self.rect.size)
        yellow = (255, 255, 0)
        pygame.draw.rect(surface, (40, 40, 40), pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)

        # Entries
        for i in range(max(4, len(self.entries))):
            color = (40, 40, 40) if i % 2 == 0 else (30, 30, 30)
            rect = pygame.Rect(0, (i * 100) - self.scroll, self.rect.width - 25, 100)
            pygame.draw.rect(surface, color, rect, 0)

            if i < len(self.entries):
                info = list(self.entries.values())[i].basic_info()
                text, trect = regularfont.render(info['title'], yellow)
                surface.blit(text, (20, rect.top + 20))

        # scroll bar
        barheight = min(1, 4 / len(self.entries))  # height of the bar
        bartop = self.scroll / (len(self.entries) * 100)  # distance from top
        scrollrect = pygame.Rect(self.rect.width - 20, 5 + (self.rect.height * bartop), 15, (self.rect.height - 10) * barheight - 3)
        pygame.draw.rect(surface, yellow, scrollrect, 0)

        pygame.draw.rect(surface, yellow, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)
        pygame.draw.line(surface, yellow, (self.rect.width - 25, 0), (self.rect.width - 25, self.rect.height), 2)

        return surface

    def handle_events(self, events):
        mousepos = pygame.mouse.get_pos()

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mousepos):
                if event.button == 4 and self.scroll > 0:
                    self.scroll -= 3
                    self.scroll = max(self.scroll, 0)
                elif event.button == 5 and self.scroll + 400 < 100 * len(self.entries):
                    self.scroll += 3
                    self.scroll = min(self.scroll, 100 * len(self.entries) - 400)
                elif event.button == 1:
                    if pygame.Rect(self.rect.right - 25, self.rect.top, 25, self.rect.height).collidepoint(mousepos):
                        barhalf = (min(1, 4 / len(self.entries)) * self.rect.height) / 2
                        relativemouse = min(max(0, mousepos[1] - self.rect.top - barhalf - 5), self.rect.height - (2 * barhalf))
                        span = abs((barhalf - 5) - (self.rect.height - barhalf - 5))
                        self.scroll = (relativemouse / max(1, span)) * max(0, (len(self.entries) * 100) - 400)
