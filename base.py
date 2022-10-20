import pygame

import os
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


class Game:
    def __init__(self, size=None, name="RHYTHMATICA", fps=60, show_fps=False):
        self.size = size if size is not None else (1280, 720)
        self.name = name
        self.fps = fps
        self.show_fps = show_fps

        logger.debug("size: %dx%d name: %s fps: %d", *size, name, fps)

        self.screen = None
        self.clock = None

        self.fonts = {}

        self.tasks = Queue()
        self.stop_flag = Event()

        self.scene = None

        logger.info("Hello, World!")

    def init_pygame(self):
        logger.info("Initializing %s...", self.name)
        pygame.init()

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)
        logger.info("Display Spawned!")

        self.clock = pygame.time.Clock()
        logger.debug("Clock is up and running!")

        self.load_fonts()

    def load_fonts(self, folder=None):
        if folder is None:
            folder = os.path.join("res", "fonts")
        logger.info("Loading fonts from %s", folder)

        for filename in [x for x in os.listdir(folder) if x.endswith(".ttf")]:
            file = os.path.join(folder, filename)
            name = filename.rsplit(".", 1)[0]
            logger.info("Loading font %s...", name)
            self.fonts[name] = font = pygame.font.Font(file, 75)
            h = font.get_height()
            logger.debug("%s size: %d h: %f, ratio %f",
                         name, 75, h, 75/h)

    def set_scene(self, scene):
        if issubclass(scene, Scene):
            logger.debug("Subclass %s detected, creating instance", scene.name)
            scene = scene()

        elif not isinstance(scene, Scene):
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
