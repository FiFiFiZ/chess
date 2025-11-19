import pygame
from math import*
import sys
sys.path.append("./bin")

from assets import Assets #type: ignore

class Game:
    def __init__(self):
        pygame.init()

        self.run = True
        self.clock = pygame.time.Clock()
        self.SCREEN_WIDTH = pygame.display.Info().current_w /2
        self.SCREEN_HEIGHT = pygame.display.Info().current_h /2
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.fill((20,50,150))
        self.fps_cap = 60
        self.grid = [4, 2, 3, 5, 6, 3, 2, 4,
                     1, 1, 1, 1, 1, 1, 1, 1,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     1, 1, 1, 1, 1, 1, 1, 1,
                     4, 2, 3, 5, 6, 3, 2, 4]

        self.assets = Assets()
        self.sprites = self.assets.sprites

    def game_run(self):
        while self.run:
            self.clock.tick(self.fps_cap)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    pygame.quit()
            pygame.display.update()

Game().game_run()
