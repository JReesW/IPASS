import pygame
import data
import scenes
from typing import Tuple, Callable, List, Union

# This module contains elements used by the UI (buttons, etc.)


pygame.freetype.init()
regularfont = pygame.freetype.SysFont('Mono', 20)
titlefont = pygame.freetype.Font("schoolgirls.otf", 60)
subtitlefont = pygame.freetype.Font("schoolgirls.otf", 30)


# Add text to a surface
def text(surface: pygame.Surface, message: str, pos: Tuple[int, int], font: pygame.freetype, color: Tuple[int, int, int]) -> None:
    """
    Draws text to a given surface

    :param surface: the surface to draw to
    :param message: the text to draw
    :param pos: the position of the drawing on the surface (topleft)
    :param font: the font to draw the text with
    :param color: the color of the text
    """
    t, _ = font.render(message, color)
    surface.blit(t, pos)


# Class representing a clickable button
class Button:
    """
    A button that can be pressed and then executes a function on the given scene
    """
    def __init__(self, rect: pygame.Rect, txt: str, funcs: Callable, args: List[any], scene: object) -> None:
        self.rect = rect
        self.text = txt
        self.color = (40, 40, 40)
        self.bordercolor = (255, 255, 0)
        self.textcolor = (255, 255, 0)
        self.funcs = funcs
        self.args = args
        self.scene = scene

    # Change color on hover
    def hover(self, mousepos: Tuple[int, int]) -> None:
        """
        Changes the color of the button when the mouse is positioned on top of it

        :param mousepos: the position of the mouse
        """
        if self.rect.collidepoint(mousepos):
            # Become darker when mouse is hovering over button
            self.color = tuple([self.color[i] - 2 if self.color[i] > 20 else self.color[i] for i in range(3)])
        else:
            # Become lighter when no mouse is hovering over button
            self.color = tuple([self.color[i] + 2 if self.color[i] < 40 else self.color[i] for i in range(3)])

    # Draw the button
    def render(self) -> None:
        """
        Return a surface containing the rendered button

        :return: the button surface
        """
        surface = pygame.Surface(self.rect.size)

        # Background and border
        pygame.draw.rect(surface, self.color, pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)
        pygame.draw.rect(surface, self.bordercolor, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        # Text
        txt, rect = regularfont.render(self.text, self.textcolor)
        surface.blit(txt, (surface.get_width() // 2 - rect.width // 2, 10))

        return surface

    def handle_events(self, events, overridemouse=None) -> None:
        mousepos = pygame.mouse.get_pos()
        if overridemouse is not None:
            mousepos = overridemouse

        self.hover(mousepos)

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if self.rect.collidepoint(mousepos):
                    for func in self.funcs:
                        self.scene.execute(func, self.args)


class TextBox:
    """
    A text box which can be activated by being clicked on, after which text can be written into it
    """
    def __init__(self, rect: pygame.Rect) -> None:
        self.rect = rect
        self.text = ""
        self.active = False
        self.buffer = 0

    def get_text(self) -> str:
        """
        Return the text written into this text box

        :return: the text
        """
        return self.text

    def render(self) -> pygame.Surface:
        """
        Return a surface containing the rendered text box

        :return: the text box surface
        """
        surface = pygame.Surface(self.rect.size)

        # Background and border
        bordercolor = (180, 140, 255) if self.active else (20, 20, 20)
        pygame.draw.rect(surface, (220, 220, 220), pygame.Rect(1, 1, self.rect.width - 2, self.rect.height - 2), 0)
        pygame.draw.rect(surface, bordercolor, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        # Text
        text(surface, self.text, (10, 10), regularfont, (0, 0, 0))

        return surface

    def handle_events(self, events: List[object], overridemouse=None) -> None:
        mousepos = pygame.mouse.get_pos()
        if overridemouse is not None:
            mousepos = overridemouse

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
    """
    A table which can store data entries and displays them.
    Has scrolling features and the ability to select entries and view more info.
    """
    def __init__(self, rect: pygame.Rect, scene: object) -> None:
        self.rect = rect
        self.entries = {}
        self.scroll = 0
        self.selected = None
        self.selectable = True
        self.scene = scene

    def add_entry(self, entry: data.Entry) -> None:
        """
        Add a given entry to the table

        :param entry: a new entry to add
        """
        self.entries[entry] = entry

    def remove_entry(self, entry: data.Entry) -> None:
        """
        Remove a given entry from the table

        :param entry: the entry to remove
        """
        del self.entries[entry]

    def clear(self) -> None:
        """
        Removes all entries from the table
        """
        self.entries = {}

    def get_selected(self) -> Union[data.Entry, None]:
        """
        Returns the selected entry

        :return: a data entry
        """
        if self.selected is None:
            return None
        return list(self.entries.values())[self.selected]

    def render(self) -> pygame.Surface:
        """
        Return a surface containing the rendered table

        :return: the table surface
        """
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
                text(surface, info['title'], (20, rect.top + 20), regularfont, yellow)
                text(surface, info['info'], (30, rect.top + 45), pygame.freetype.SysFont('Mono', 15), yellow)

                # radio selectors
                if self.selectable:
                    pygame.draw.rect(surface, yellow, pygame.Rect(self.rect.width - 100, (i * 100) - self.scroll + 25, 50, 50), 2)
                    if self.selected == i:
                        pygame.draw.circle(surface, yellow, (self.rect.width - 75, (i * 100) - self.scroll + 50), 15, 3)

                    # info button
                    pygame.draw.rect(surface, yellow, pygame.Rect(self.rect.width - 175, (i * 100) - self.scroll + 25, 50, 50), 2)
                    ifont = pygame.freetype.SysFont('Mono', 50)
                    text(surface, "i", (self.rect.width - 160, (i * 100) - self.scroll + 35), ifont, yellow)

        # Scroll bar
        barheight = min(1.0, (self.rect.height / 100) / max(1, len(self.entries)))  # height of the bar
        bartop = self.scroll / (max(1, len(self.entries)) * 100)  # distance from top
        scrollrect = pygame.Rect(self.rect.width - 20, 5 + (self.rect.height * bartop), 15, (self.rect.height - 10) * barheight - 3)
        pygame.draw.rect(surface, yellow, scrollrect, 0)

        pygame.draw.rect(surface, yellow, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)
        pygame.draw.line(surface, yellow, (self.rect.width - 25, 0), (self.rect.width - 25, self.rect.height), 2)

        return surface

    def handle_events(self, events, overridemouse=None):
        mousepos = pygame.mouse.get_pos()
        if overridemouse is not None:
            mousepos = overridemouse

        for event in events:
            # Check if the mouse is being used while positioned over the table
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(mousepos):
                # Scrolling upwards
                if event.button == 4 and self.scroll > 0:
                    self.scroll -= 6
                    self.scroll = max(self.scroll, 0)
                # Scrolling downwards
                elif event.button == 5 and self.scroll + self.rect.height < 100 * len(self.entries):
                    self.scroll += 6
                    self.scroll = min(self.scroll, 100 * len(self.entries) - self.rect.height)
                # Clicking with the rightmouse button
                elif event.button == 1:
                    # Check if the mouse is positioned over the scroll bar
                    if pygame.Rect(self.rect.right - 25, self.rect.top, 25, self.rect.height).collidepoint(mousepos):
                        # Calculate how far the list must scroll so that the middle of the scroll bar lands
                        # where the mouse was clicked. The scroll bar cannot exceed its boundaries.
                        barhalf = (min(1.0, 4 / max(1, len(self.entries))) * self.rect.height) / 2
                        relativemouse = min(max(0, mousepos[1] - self.rect.top - barhalf - 5), self.rect.height - (2 * barhalf))
                        span = abs((barhalf - 5) - (self.rect.height - barhalf - 5))
                        self.scroll = int((relativemouse / max(1, span)) * max(0, (len(self.entries) * 100) - self.rect.height))
                    elif self.selectable:
                        for c, e in enumerate(self.entries):
                            radiorect = pygame.Rect(self.rect.width - 100 + self.rect.left, (c * 100) - self.scroll + 25 + self.rect.top, 50, 50)
                            inforect = pygame.Rect(self.rect.width - 175 + self.rect.left, (c * 100) - self.scroll + 25 + self.rect.top, 50, 50)
                            if radiorect.collidepoint(mousepos):
                                if self.selected == c:
                                    self.selected = None
                                else:
                                    self.selected = c
                            elif inforect.collidepoint(mousepos):
                                self.scene.director.switch(scenes.InfoScene(e, self.scene))


class SearchBox:
    """
    A search box, combining a button, text box, and table into one
    """
    def __init__(self, rect: pygame.Rect, searchtype: str, scene: object) -> None:
        textrect = pygame.Rect(10, 10, rect.width - 105, 30)
        buttonrect = pygame.Rect(rect.width - 90, 10, 80, 30)
        tablerect = pygame.Rect(10, 45, rect.width - 20, rect.height - 55)
        self.rect = rect
        self.inputbar = TextBox(textrect)
        self.searchbutton = Button(buttonrect, "search", [self.search], [self.inputbar.get_text], self)
        self.outputtable = Table(tablerect, scene)
        # Searchtype dictates whether the searchbox searches for movies or people, defaulting to movies if unknown
        # modes are entered.
        self.searchtype = "person" if searchtype.lower() == "person" else "movie"

    def handle_events(self, events: List[object]) -> None:
        mousepos = pygame.mouse.get_pos()
        relativemouse = (mousepos[0] - self.rect.left, mousepos[1] - self.rect.top)

        self.inputbar.handle_events(events, relativemouse)
        self.searchbutton.handle_events(events, relativemouse)
        self.outputtable.handle_events(events, relativemouse)

    def render(self) -> pygame.Surface:
        """
        Return a surface containing the rendered search box

        :return: the search box surface
        """
        surface = pygame.Surface(self.rect.size)
        yellow = (255, 255, 0)
        pygame.draw.rect(surface, yellow, pygame.Rect(0, 0, self.rect.width - 1, self.rect.height - 1), 2)

        surface.blit(self.inputbar.render(), self.inputbar.rect.topleft)
        surface.blit(self.searchbutton.render(), self.searchbutton.rect.topleft)
        surface.blit(self.outputtable.render(), self.outputtable.rect.topleft)

        return surface

    @staticmethod
    def execute(func: Callable, args: List[any]) -> None:
        """
        Execute a given function and pass args as arguments
        Can be called by buttons to call class methods

        :param func: the function to execute
        :param args: the arguments to pass to the function
        """
        func(args[0]())

    def search(self, query: str) -> None:
        """
        Fill the table with search results from parsing the string into IMDbPy

        :param query: the queried string
        """
        results = data.search_person(query, 10) if self.searchtype == "person" else data.search_movie(query, 10)
        self.outputtable.clear()
        self.outputtable.selected = None
        self.outputtable.scroll = 0
        _ = [self.outputtable.add_entry(entry) for entry in results]
