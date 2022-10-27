from .task import Task
from ..utils import blit_center_rel

import time
import logging
from threading import Event

logger = logging.getLogger("RHYTHMATICA")


class Scene:
    """
    Class for determining each scenes in game and how the game should act.
    """
    name = "Scene"

    def set_game(self, game):
        self.game = game

    def start(self):
        raise NotImplementedError()

    def handle_event(self, event):
        pass

    def task(self):
        pass

    def cleanup(self):
        pass


class FadeTask(Task):
    def __init__(self, surface, duration, fadein=True, callback=None):
        super().__init__(self.func, name="FadeTask")
        self.surface = surface
        self.duration = duration
        self.fadein = fadein
        self.callback = callback

        self.orig_opacity = 255 if fadein else 0
        target_delta = -255 if fadein else 255
        self.increment = target_delta / duration

        self.start_time = None

    def func(self, task, game):
        if self.start_time is None:
            self.start_time = time.perf_counter()

        elapsed_time = time.perf_counter() - self.start_time

        alpha = self.orig_opacity + self.increment * elapsed_time
        alpha = alpha if 0 <= alpha <= 255 else 0 if self.fadein else 255

        surf_alpha = self.surface.copy()
        surf_alpha.set_alpha(alpha)

        blit_center_rel(game.screen, surf_alpha, (0.5, 0.5))

        if elapsed_time < self.duration:
            self.runagain(game)
        else:
            logger.debug("Fade finished")
            if callable(self.callback):
                logger.debug("Callback found, calling...")
                self.callback(game)


class TransitionableScene(Scene):
    def __init__(self):
        self.fade_bg = None
        self.fade_duration = 1
        self.fade_task = None

    def start_fade(
            self, surface=None, duration=None, fadein=True, callback=None):
        if surface is None:
            surface = self.fade_bg

        if duration is None:
            duration = self.fade_duration

        self.fade_task = FadeTask(surface, duration, fadein, callback)
        self.game.add_task(self.fade_task)
