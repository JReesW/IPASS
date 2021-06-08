import pygame
import sys
import random
from uielements import *

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

    def handle_events(self, events):
        # Get the position of the mouse on the game
        mousepos = pygame.mouse.get_pos()

        # Each scene is dealing with buttons, so the button handling is done here
        # Handle mouse hover over buttons
        for button in self.buttons:
            button.hover(mousepos)

        # Handle button click
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                for button in self.buttons:
                    if button.rect.collidepoint(mousepos):
                        for func in button.funcs:
                            func(*button.args)

    def update(self):
        pass

    def render(self, surface):
        # Clear screen
        surface.fill((0, 0, 0))

        # Button rendering
        for button in self.buttons:
            surface.blit(button.render(), button.rect.topleft)

    # Used for switching to another scene, can be called by buttons.
    def switch(self, scene, args=None):
        args = [] if args is None else args
        self.director.switch(Fader(self, scene(*args)))


# The class representing the main menu
class MenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = [
            Button(pygame.Rect(100, 400, 300, 30), "Test", [self.switch], [TestScene]),
            Button(pygame.Rect(100, 600, 300, 30), "Quit", [pygame.quit, sys.exit], [])
        ]

    def handle_events(self, events):
        super().handle_events(events)

    def render(self, surface):
        super().render(surface)

        # Title text
        text, rect = titlefont.render("Movie Enjoyment Predictor", (255, 255, 0))
        surface.blit(text, (40, 40))
        text, rect = regularfont.render("by Jonathan Williams", (255, 255, 0))
        surface.blit(text, (50, 100))


class TestScene(Scene):
    def __init__(self):
        super().__init__()
        self.buttons = [
            Button(pygame.Rect(100, 400, 300, 30), "Return", [self.switch], [MenuScene])
        ]


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
        pygame.draw.rect(self.veil, (0, 0, 0), surface.get_rect())
        self.veil.set_alpha(self.fade)
        surface.blit(self.veil, (0, 0))