import pygame
import sys
from uielements import *
import data

# This module contains all of the scenes used by the Movie predictor


# Main Classes:

# Controls the scenes and handles transitions between them
class Director:
    def __init__(self):
        self.scene = None
        self.switch(MenuScene())

    # Takes the new scene as its current scene and adds itself to it
    def switch(self, scene):
        self.scene = scene
        self.scene.director = self


# Scene base class
class Scene:
    def __init__(self):
        # Scenes initially have no director
        self.director = None
        self.ui = {}

    def handle_events(self, events):
        for element in self.ui.values():
            element.handle_events(events)

    def update(self):
        pass

    def render(self, surface):
        # Clear screen
        surface.fill((40, 40, 40))

        # UI element rendering
        for element in self.ui.values():
            surface.blit(element.render(), element.rect.topleft)

    # Used for switching to another scene, can be called by buttons.
    def switch(self, scene, args=None):
        args = [] if args is None else args
        self.director.switch(Fader(self, scene(*args)))

    @staticmethod
    def execute(func, args):
        func(*args)


# The class representing the main menu
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.ui = {
            'return': Button(pygame.Rect(100, 300, 300, 30), "Predict Enjoyment", [self.switch], [PredictorScene], self),
            'pvalue': Button(pygame.Rect(100, 400, 300, 30), "P-Value", [self.switch], [PValueScene], self),
            'rate': Button(pygame.Rect(100, 500, 300, 30), "Rate People", [self.switch], [RateScene], self),
            'quit': Button(pygame.Rect(100, 600, 300, 30), "Quit", [pygame.quit, sys.exit], [], self)
        }

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        # Title text
        text(surface, "Movie Enjoyment Predictor", (40, 40), titlefont, (255, 255, 0))
        text(surface, "by Jonathan Williams", (50, 100), regularfont, (255, 255, 0))


class PredictorScene(Scene):
    def __init__(self):
        super().__init__()
        self.ui = {
            'return': Button(pygame.Rect(100, 650, 300, 30), "Return", [self.switch], [MenuScene], self),
            'search': SearchBox(pygame.Rect(100, 200, 1000, 400), "movie", self)
        }

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        text(surface, "Predict Enjoyment", (40, 40), titlefont, (255, 255, 0))


class PValueScene(Scene):
    def __init__(self):
        super().__init__()
        self.ui = {
            'return': Button(pygame.Rect(100, 650, 300, 30), "Return", [self.switch], [MenuScene], self),
            'table': Table(pygame.Rect(50, 200, 600, 400), self),
            'search': SearchBox(pygame.Rect(800, 200, 600, 400), "person", self),
            'take': Button(pygame.Rect(700, 385, 50, 30), "←", [self.take], [], self)
        }
        self.ui['table'].selectable = False

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        text(surface, "P-Value Mode", (40, 40), titlefont, (255, 255, 0))

    def take(self):
        entry = self.ui['search'].outputtable.get_selected()
        if entry is not None:
            self.ui['table'].add_entry(entry)


class RateScene(Scene):
    def __init__(self):
        super().__init__()
        self.ui = {
            'return': Button(pygame.Rect(225, 700, 300, 30), "Return", [self.switch], [MenuScene], self),
            'rate': Button(pygame.Rect(575, 700, 300, 30), "Rate", [self.rate], [], self),
            'search': SearchBox(pygame.Rect(225, 150, 1000, 500), "person", self)
        }

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        text(surface, "Rate People", (40, 40), titlefont, (255, 255, 0))

    def rate(self):
        entry = self.ui['search'].outputtable.get_selected()
        if entry is not None:
            self.director.switch(ApplyRateScene(entry, self))


class ApplyRateScene(Scene):
    def __init__(self, entry, background):
        super().__init__()
        self.entry = entry
        self.background = background
        self.error = [""]
        self.ui = {
            'return': Button(pygame.Rect(485, 500, 215, 30), "Return", [None], [self.background], self),
            'apply': Button(pygame.Rect(750, 500, 215, 30), "Apply", [self.apply], [], self),
            'text': TextBox(pygame.Rect(850, 400, 100, 30))
        }

    def update(self):
        if self.ui['return'].funcs[0] is None:
            self.ui['return'].funcs = [self.director.switch]

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        self.background.render(surface)
        sr = pygame.display.get_surface().get_rect()
        veil = pygame.Surface(sr.size)
        pygame.draw.rect(veil, (20, 20, 20), surface.get_rect())
        veil.set_alpha(150)
        surface.blit(veil, (0, 0))
        yellow = (255, 255, 0)

        pygame.draw.rect(surface, (40, 40, 40), pygame.Rect(475, 250, 500, 300))
        pygame.draw.rect(surface, yellow, pygame.Rect(475, 250, 500, 300), 2)

        text(surface, "Rate", (510, 285), subtitlefont, yellow)
        savedata = data.load_person_ratings()
        if self.entry.id in savedata:
            text(surface, f"{self.entry.name} (currently: {savedata[self.entry.id][0]})", (520, 315), regularfont, yellow)
        else:
            text(surface, self.entry.name, (520, 315), regularfont, yellow)
        text(surface, "Enter a rating (1.0 - 10.0):", (485, 410), regularfont, yellow)

        for e in range(len(self.error)):
            text(surface, self.error[e], (500, 440 + (e * 20)), regularfont, yellow)

        for element in self.ui.values():
            surface.blit(element.render(), element.rect.topleft)

    def apply(self):
        score = self.ui['text'].get_text()
        try:
            rating = float(score)
            if rating < 1.0 or rating > 10.0:
                raise ValueError
            savedata = data.load_person_ratings()
            if self.entry.id in savedata:
                data.save_person_rating(self.entry.id, rating, savedata[self.entry.id][1])
            else:
                data.save_person_rating(self.entry.id, rating, [])
            self.error = ["Rating saved succesfully"]
        except ValueError:
            self.error = ["Error: Input is not a number", "       between 1.0 and 10.0"]


class InfoScene(Scene):
    def __init__(self, entry, background):
        super().__init__()
        self.entry = data.update_movie(entry.id, ['main']) if isinstance(entry, data.Movie) else data.update_person(entry.id, ['main'])
        self.background = background
        self.ui = {
            'return': Button(pygame.Rect(150, 670, 300, 30), "Return", [None], [self.background], self)
        }

    def update(self):
        if self.ui['return'].funcs[0] is None:
            self.ui['return'].funcs = [self.director.switch]

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        self.background.render(surface)
        sr = pygame.display.get_surface().get_rect()
        veil = pygame.Surface(sr.size)
        pygame.draw.rect(veil, (20, 20, 20), surface.get_rect())
        veil.set_alpha(150)
        surface.blit(veil, (0, 0))
        yellow = (255, 255, 0)

        pygame.draw.rect(surface, (40, 40, 40), pygame.Rect(150, 150, 1150, 500))
        pygame.draw.rect(surface, yellow, pygame.Rect(150, 150, 1150, 500), 2)

        text(surface, "Info", (190, 190), titlefont, yellow)

        if isinstance(self.entry, data.Movie):
            text(surface, "Title", (205, 270), subtitlefont, yellow)
            text(surface, self.entry.title, (220, 310), regularfont, yellow)
            text(surface, "Director", (555, 360), subtitlefont, yellow)
            for i in range(min(2, len(self.entry.directors))):
                text(surface, self.entry.directors[i].name, (570, 400 + (30 * i)), regularfont, yellow)
            text(surface, "Cast", (205, 360), subtitlefont, yellow)
            for i in range(min(8, len(self.entry.cast))):
                text(surface, self.entry.cast[i].name, (220, 400 + (30 * i)), regularfont, yellow)
            if self.entry.poster is not None:
                surface.blit(self.entry.poster, (972, 175))
        else:
            text(surface, "Name", (255, 270), subtitlefont, yellow)
            text(surface, self.entry.name, (270, 310), regularfont, yellow)
            text(surface, "Birth date", (255, 360), subtitlefont, yellow)
            text(surface, self.entry.birthdate, (270, 400), regularfont, yellow)
            text(surface, "Birth place", (255, 450), subtitlefont, yellow)
            text(surface, self.entry.birthplace, (270, 490), regularfont, yellow)
            if self.entry.headshot is not None:
                surface.blit(self.entry.headshot, (972, 175))

        for element in self.ui.values():
            surface.blit(element.render(), element.rect.topleft)


class Fader(Scene):                         # Handles fading in and out between scenes
    def __init__(self, previous, next):
        super().__init__()
        self.current = previous     # The previous scene
        self.next = next            # The next scene
        self.fadein = True
        self.fade = 0
        sr = pygame.display.get_surface().get_rect()
        self.veil = pygame.Surface(sr.size)

    def handle_events(self, events):
        # The fader is meant to go uninterrupted, so event handling is disabled.
        pass

    def update(self):
        self.fade = self.fade + 15 if self.fadein else self.fade - 15
        if self.fade >= 255:
            self.fadein = False
            self.current = self.next
        if self.fade <= 0:
            self.director.switch(self.next)

    def render(self, surface):
        self.current.render(surface)
        pygame.draw.rect(self.veil, (20, 20, 20), surface.get_rect())
        self.veil.set_alpha(self.fade)
        surface.blit(self.veil, (0, 0))
