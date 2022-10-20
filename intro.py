import pygame

from play import Play
from utils import get_random_color
from base import TransitionableScene

import os
import time
import random
import logging

logger = logging.getLogger("RHYTHMATICA")


class Intro(TransitionableScene):
    def __init__(self, interval=None):
        super().__init__()

        self.interval = interval if interval else 1 / 130 * 60
        self.min_size = 100
        self.max_size = 200
        self.size_increment = 0.1

        self.circles = None

        self.start_time = 0
        self.next_time = 0
        self.big = True

        self.fadeout_surface = None

    def start(self):
        w, h = self.game.screen.get_size()

        loadingpath = os.path.join("res", "image", "loading.png")
        self.fadeout_surface = pygame.transform.smoothscale(
            pygame.image.load(loadingpath), (w, h))

        # loc, color, size_factor
        self.circles = [(
            (random.randrange(w), random.randrange(h)),
            get_random_color(),
            random.random())
            for _ in range(10)
        ]

        self.start_time = time.perf_counter()
        self.next_time = self.start_time + self.interval

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            self.game.add_task(self.fade_task, (
                self.fadeout_surface, False, self.fadeout_callback))

    def fadeout_callback(self, _):
        logger.info("Intro fadeout finished, starting Play Scene")
        next_scene = Play(self.fadeout_surface)
        self.game.set_scene(next_scene)

    def task(self):
        if time.perf_counter() > self.next_time:
            self.big = not self.big
            self.next_time += self.interval

        self.game.screen.fill("white")
        for loc, color, size_factor in self.circles:
            factor = size_factor + (self.size_increment if self.big else 0)
            size = self.min_size + (self.max_size - self.min_size) * factor
            pygame.draw.circle(self.game.screen, color, loc, size)
