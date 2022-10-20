import pygame

from .play import Circle
from .selectsong import SongSelect
from ..utils import get_random_color, scale_rel, blit_center_rel
from ..base import TransitionableScene

import os
import time
import random
import logging

logger = logging.getLogger("RHYTHMATICA")


class Intro(TransitionableScene):
    name = "Intro"

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

        self.logo = None
        self.version = None
        self.pressntostart = None
        self.fadeout_surface = None

    def start(self):
        w, h = maxsize = self.game.screen.get_size()

        logo_raw = pygame.image.load(os.path.join("res", "image", "logo.png"))
        self.logo = scale_rel(logo_raw, 0.25, maxsize).convert_alpha()

        self.version = scale_rel(
            self.game.fonts['bold'].render("Ver. A10P", True, "black"),
            0.05, maxsize)

        self.pressntostart = scale_rel(
            self.game.fonts['black'].render("Press N to start", True, "black"),
            0.075, maxsize)

        loadingpath = os.path.join("res", "image", "loading.png")
        self.fadeout_surface = pygame.transform.smoothscale(
            pygame.image.load(loadingpath), maxsize).convert_alpha()

        # loc, color, size_factor
        self.circles = [(
            (random.randrange(w), random.randrange(h)),
            random.choice(Circle.COLORS),
            random.random())
            for _ in range(10)
        ]

        self.start_time = time.perf_counter()
        self.next_time = self.start_time + self.interval

        pygame.mixer.music.load(os.path.join("res", "sound", "main.mp3"))
        pygame.mixer.music.play()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(os.path.join("res", "sound", "start.mp3"))
            pygame.mixer.music.play()
            self.game.add_task(self.fade_task, (
                self.fadeout_surface, False, self.fadeout_callback))

    def fadeout_callback(self, _):
        logger.info("Intro fadeout finished, starting SongSelect Scene")
        next_scene = SongSelect(self.fadeout_surface)
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

        blit_center_rel(self.game.screen, self.logo, (0.5, 0.45))
        blit_center_rel(self.game.screen, self.pressntostart, (0.5, 0.8))
        blit_center_rel(self.game.screen, self.version, (1, 1), (1, 1))
