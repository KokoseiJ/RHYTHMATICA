import pygame

import os
import time
import logging
from queue import Queue
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


class Game:
    def __init__(self, size=None, name="RHYTHMATICA", fullscreen=False, fps=60,
                 show_fps=False):
        self.size = size if size is not None else (1280, 720)
        self.name = name
        self.fps = fps
        self.show_fps = show_fps
        self.flags = 0
        if fullscreen:
            self.flags = self.flags | pygame.FULLSCREEN

        logger.debug("size: %dx%d name: %s fps: %d", *size, name, fps)

        self.screen = None
        self.clock = None

        self.fonts = {}
        self.font_size_ratio = 1 / 12

        self.tasks = Queue()
        self.stop_flag = Event()

        self.scene = None

        logger.info("Hello, World!")

    def init_pygame(self):
        logger.info("Initializing %s...", self.name)
        pygame.init()

        self.screen = pygame.display.set_mode(self.size, self.flags)
        pygame.display.set_caption(self.name)
        logger.info("Display Spawned!")

        self.clock = pygame.time.Clock()
        logger.debug("Clock is up and running!")

        self.load_fonts()

    def load_fonts(self, folder=None, target_height=None):
        if folder is None:
            folder = os.path.join("res", "fonts")

        if target_height is None:
            target_height = self.screen.get_size()[1] * self.font_size_ratio

        logger.info("Loading fonts from %s, target height: %f",
                    folder, target_height)

        files = [x for x in os.listdir(folder) if x.endswith(".ttf")]

        font = pygame.font.Font(os.path.join(folder, files[0]), 100)
        ratio = 100 / font.get_height()
        size = round(ratio * target_height)
        logger.debug("calculated ratio: %f size: %d", ratio, size)

        for filename in files:
            file = os.path.join(folder, filename)
            name = filename.rsplit(".", 1)[0]

            logger.info("Loading font %s...", name)
            self.fonts[name] = font = pygame.font.Font(file, size)

            h = font.get_height()
            logger.debug("%s size: %d h: %f", name, size, h)

    def set_scene(self, scene):
        if not isinstance(scene, Scene):
            if issubclass(scene, Scene):
                logger.debug(
                    "Subclass %s detected, creating instance", scene.name)
                scene = scene()

            else:
                raise TypeError(f"scene {scene.__code__.c_name} is not Scene!")

        if self.scene is not None:
            logger.debug("Calling cleanup on Scene %s", self.scene)
            self.scene.cleanup()

        logger.debug("Registering %s as a scene", scene.name)
        self.scene = scene
        self.scene.set_game(self)

        logger.debug("Scene registered, Calling start")
        self.scene.start()

        logger.debug("Scene started")

    def add_task(self, task, args=None, kwargs=None):
        """
        Task should be a callable with one argument, or (func, args, kwargs)
        """
        self.tasks.put((task, args, kwargs))

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            logger.warning("pygame.QUIT triggered. Stopping the loop..")
            self.stop()

    def task(self):
        if self.show_fps:
            fps = round(self.clock.get_fps())
            fps_text = self.fonts['regular'].render(str(fps), True, 'black')
            self.screen.blit(fps_text, (0, 0))

    def run(self):
        """
        Task execution order:
        1. handle_event <- so that tasks can be added according to events
        2. Scene task <- Lets the scene prepare the surface beforehand
        3. task queue
        4. Global task <- Global overlay, has to be the last
        """
        if self.scene is None:
            logger.error("I refuse to run the game without a scene!")
            raise RuntimeError("Scene should be set before running the game")

        logger.info("Running the game!")
        while not self.stop_flag.is_set():
            for event in pygame.event.get():
                self.handle_event(event)
                self.scene.handle_event(event)

            self.scene.task()

            tasks = []
            while not self.tasks.empty():
                tasks.append(self.tasks.get())

            for func, args, kwargs in tasks:
                func(self, *(args if args else []),
                     **(kwargs if kwargs else {}))

            self.task()

            pygame.display.flip()

            self.clock.tick(self.fps)

        logger.warning("Broken out of the loop, exiting run()")

    def stop(self):
        logger.warning(".stop() called")
        self.stop_flag.set()
