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


class TransitionableScene(Scene):
    def __init__(self):
        self.fade_bg = None
        self.fade_ongoing = Event()
        self.fade_duration = 1

    def fade_task(self, game, surface, fadein=True, callback=None,
                  start_time=None, duration=None):
        self.fade_ongoing.set()
        if start_time is None:
            start_time = time.perf_counter()
        if duration is None:
            duration = self.fade_duration

        elapsed_time = time.perf_counter() - start_time

        target = 255 * (-1 if fadein else 1)

        opacity = 255 if fadein else 0
        opacity += round(target / duration * elapsed_time)

        logger.debug("t: %f, a: %d", elapsed_time, opacity)

        surface_copy = surface.copy()
        surface_copy.set_alpha(opacity)

        if self.fade_bg is not None:
            game.screen.blit(self.fade_bg, (0, 0))
        game.screen.blit(surface_copy, (0, 0))

        if elapsed_time > duration:
            logger.debug("Fade task ended")
            self.fade_ongoing.clear()
            logger.debug(callback)
            if callable(callback):
                logger.debug("Callback found, calling")
                callback(self)
            return

        game.add_task(self.fade_task, (
            surface, fadein, callback, start_time, duration))
