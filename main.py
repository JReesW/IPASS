import pygame
import pygame.freetype
import sys
import os

import scenes


os.environ['SDL_VIDEO_WINDOW_POS'] = '%d,%d' % (0, 20)


if __name__ == "__main__":
    pygame.init()
    pygame.freetype.init()
    surface = pygame.display.set_mode((1450, 800))
    pygame.display.set_caption("Movie Enjoyment Predictor")
    FPS = pygame.time.Clock()

    director = scenes.Director()

    while True:
        FPS.tick(60)

        if pygame.event.get(pygame.QUIT):
            pygame.quit()
            sys.exit()

        director.scene.handle_events(pygame.event.get())
        director.scene.update()
        director.scene.render(surface)

        pygame.display.flip()
