import pygame

from base import TransitionableScene

import logging
from math import floor

logger = logging.getLogger("RHYTHMATICA")


class Circle:
    SIZE = 0.225
    LOCX = ((3/8), (5/8))
    LOCY = ((3/16), (8/16), (13/16))
    COLORS = (
        pygame.Color("firebrick"), pygame.Color("gold"),
        pygame.Color("forestgreen"), pygame.Color("darkturquoise"),
        pygame.Color("blue"), pygame.Color("darkviolet")
    )

    def __init__(self, num, maxsize=None):
        if maxsize is None:
            maxsize = pygame.display.get_window_size()
        self.maxw, self.maxh = maxsize

        rw, rh = (self.LOCX[num % 2], self.LOCY[floor(num / 2)])

        self.loc = (self.maxw * rw, self.maxh * rh)
        self.radius = self.maxh * self.SIZE / 2
        self.color = self.COLORS[num]

        logger.debug((self.loc, self.radius))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.loc, self.radius)


class CircleEdge(Circle):
    EDGELEN = 1/10
    RADIUS_INCREMENT = 1.1

    def __init__(self, num, maxsize=None):
        super().__init__(num, maxsize)
        self.color = pygame.Color("gray50")
        self.edge = round(self.radius * self.EDGELEN)
        self.radius_big = self.radius * self.RADIUS_INCREMENT

    def draw(self, surface, big=False):
        radius = self.radius_big if big else self.radius
        pygame.draw.circle(
            surface, self.color, self.loc, radius, self.edge)


class Play(TransitionableScene):
    name = "Play"
    KEYS = ["t", "y", "g", "h", "b", "n"]

    def __init__(self, fadein_surface=None):
        super().__init__()

        self.surface = None
        self.edges = None
        self.key_status = [
            False, False,
            False, False,
            False, False
        ]

        self.fadein_surface = fadein_surface

    def start(self):
        screen_size = self.game.screen.get_size()

        self.surface = pygame.Surface(screen_size)
        self.surface.fill("orange")
        for n in range(6):
            Circle(n, screen_size).draw(self.surface)

        self.edges = [CircleEdge(n, screen_size) for n in range(6)]

        if self.fadein_surface is not None:
            self.game.add_task(self.fade_task, (self.fadein_surface, True))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                logger.info("q pressed, exiting the game")
                self.game.stop()

            keyname = pygame.key.name(event.key)
            if keyname in self.KEYS:
                keystatus = event.type == pygame.KEYDOWN
                self.key_status[self.KEYS.index(keyname)] = keystatus
                # logger.debug(self.key_status)

    def task(self):
        self.game.screen.blit(self.surface, (0, 0))
        [edge.draw(self.game.screen, self.key_status[n])
         for n, edge in enumerate(self.edges)]
