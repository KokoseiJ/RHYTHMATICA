import pygame

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
    def __init__(self, size=None, name="RHYTHMATICA", fps=60, scene=None):
        self.size = size if size is not None else (1280, 720)
        self.name = name
        self.fps = fps

        logger.debug("size: %dx%d name: %s fps: %d", *size, name, fps)

        self.screen = None
        self.clock = None

        self.tasks = Queue()
        self.stop_flag = Event()

        self.scene = None
        
        if scene is not None:
            self.set_scene(scene)

        logger.info("Hello, World!")

    def init_pygame(self):
        logger.info("Initializing %s...", self.name)
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.name)
        logger.debug("Display Spawned!")

        self.clock = pygame.time.Clock()
        logger.debug("Clock is up and running!")

    def set_scene(self, scene):
        if not isinstance(scene, Scene):
            scene = scene()
        elif not issubclass(scene, Scene):
            raise TypeError(f"scene {scene.__code__.c_name} is not Scene!")

        if self.scene is not None:
            logger.debug("Calling cleanup on Scene %s", self.scene)
            self.scene.cleanup()

        name = scene.name
        logger.debug("Registering %s as a scene", name)
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
        pass

    def run(self):
        if self.scene is None:
            logger.error("I refuse to run the game without a scene!")
            raise RuntimeError("Scene should be set before running the game")

        logger.info("Running the game!")
        while not self.stop_flag.is_set():
            for event in pygame.event.get():
                self.handle_event(event)
                self.scene.handle_event(event)

            self.task()
            self.scene.task()

            tasks = []
            while not self.tasks.empty():
                tasks.append(self.tasks.get())

            for func, args, kwargs in tasks:
                func(self, *(args if args else []),
                     **(kwargs if kwargs else {}))

            pygame.display.flip()
            self.clock.tick(self.fps)

    def stop(self):
        self.stop_flag.set()
