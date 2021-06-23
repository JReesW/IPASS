import pygame
import pygame.freetype
import sys
import os

import scenes


os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0, 20)


if __name__ == "__main__":
    # Initialize pygame and its settings
    pygame.init()
    pygame.freetype.init()
    surface = pygame.display.set_mode((1450, 800))
    pygame.display.set_caption("Movie Enjoyment Predictor")
    FPS = pygame.time.Clock()

    # The director controlling the scenes
    director = scenes.Director()

    # The main loop
    while True:
        FPS.tick(60)

        # Handle exiting
        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()

        # Call the necessary scene functions of the active scene
        director.scene.handle_events(pygame.event.get())
        director.scene.update()
        director.scene.render(surface)

        # Draw the surface to the screen
        pygame.display.flip()
