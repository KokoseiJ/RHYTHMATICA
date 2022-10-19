import pygame

from base import Scene
from utils import get_random_color

import time
import random
import logging

logger = logging.getLogger("RHYTHMATICA")


class Intro(Scene):
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

    def start(self):
        # loc, color, size_factor
        w, h = self.game.screen.get_size()
        self.circles = [(
            (random.randrange(w), random.randrange(h)),
            get_random_color(),
            random.random())
            for _ in range(10)
        ]

        self.start_time = time.perf_counter()
        self.next_time = self.start_time + self.interval

    def task(self):
        if time.perf_counter() > self.next_time:
            self.big = not self.big
            self.next_time += self.interval

        self.game.screen.fill("white")
        for loc, color, size_factor in self.circles:
            factor = size_factor + (self.size_increment if self.big else 0)
            size = self.min_size + (self.max_size - self.min_size) * factor
            pygame.draw.circle(self.game.screen, color, loc, size)
