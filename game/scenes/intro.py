import pygame

from ..base.scene import TransitionableScene
from .play import Circle
from .selectsong import SongSelect
from ..utils import scale_rel, blit_center_rel

import os
import time
import random
import logging

logger = logging.getLogger("RHYTHMATICA")


class Intro(TransitionableScene):
    name = "Intro"

    def __init__(self, interval=None):
        super().__init__()

        self.interval = interval if interval else 1 / 130 * 60 / 2
        self.min_size = 100
        self.max_size = 200
        self.size_increment = 0.1

        self.circles = None
        self.logo = None
        self.pressntostart = None
        self.version = None
        self.fade_bg = None

        self.start_time = 0
        self.next_time = 0
        self.big = True

    def prepare_res(self):
        logger.info("Intro: Preparing resources...")
        maxsize = self.game.screen.get_size()

        logger.info("Loading RHYTHMATICA logo...")
        logo_raw = pygame.image.load(os.path.join("res", "image", "logo.png"))
        self.logo = scale_rel(logo_raw, 0.25, maxsize).convert_alpha()

        logger.info("Rendering Text...")
        self.pressntostart = scale_rel(
            self.game.fonts['black'].render("Press N to start", True, "black"),
            self.game.font_size_ratio, maxsize)

        self.version = scale_rel(
            self.game.fonts['bold'].render("Ver. A10P", True, "black"),
            self.game.font_size_ratio * 0.75, maxsize)

        logger.info("Loading loading screen...")
        loadingpath = os.path.join("res", "image", "loading.png")
        self.fade_bg = pygame.transform.smoothscale(
            pygame.image.load(loadingpath), maxsize).convert()

        logger.info("Finished!")

    def start(self):
        self.prepare_res()

        w, h = self.game.screen.get_size()

        # loc, color, size_factor
        self.circles = [
            (
                (random.randrange(w), random.randrange(h)),
                random.choice(Circle.COLORS),
                random.random()
            ) for _ in range(10)
        ]

        self.start_time = time.perf_counter()
        self.next_time = self.start_time + self.interval

        pygame.mixer.music.load(os.path.join("res", "sound", "main.mp3"))
        pygame.mixer.music.play()

    def handle_event(self, event):
        if self.fade_ongoing.is_set():
            logger.warning("Event during fadeout, ignoring")
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(os.path.join("res", "sound", "start.mp3"))
            pygame.mixer.music.play()
            self.start_fade(fadein=False, callback=self.fadeout_callback)

    def fadeout_callback(self, game):
        logger.info("Intro fadeout finished, starting SongSelect Scene")
        next_scene = SongSelect(self.fade_bg)
        game.set_scene(next_scene)

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
