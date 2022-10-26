import time
import logging
from threading import Event

logger = logging.getLogger("RHYTHMATICA")


class Task:
    def __init__(self, func, *args, name=None, **kwargs):
        self.name = name if name is not None else func.__code__.co_name
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.finish_flag = Event()

        if not callable(func):
            raise TypeError(f"{func.__code__.co_name} is not callable!")

    @property
    def is_finished(self):
        return self.finish_flag.is_set()

    def runagain(self, game):
        game.add_task(self)

    def run(self, game):
        self._run(game)

    def _run(self, game):
        logger.debug("Running func")
        self.func(game, *self.args, **self.kwargs)
        self.finish_flag.set()


class WaitTimeTask(Task):
    def __init__(self, func, after=0, *args, name=None, **kwargs):
        super().__init__(func, *args, name=name, **kwargs)
        self.target_time = 0
        self.wait_for(after)

    def wait_for(self, after):
        self.target_time = time.perf_counter() + after

    def run(self, game):
        now = time.perf_counter()
        logger.debug("now: %f target: %f", now, self.target_time)
        if now < self.target_time:
            self.runagain(game)
        else:
            logger.debug("Target hit, running func")
            self._run(game)


class WaitForTask(Task):
    def __init__(self, func, after_task, *args, name=None, **kwargs):
        super().__init__(func, *args, name=name, **kwargs)
        self.after_task = after_task

    def run(self, game):
        if not self.after_task.is_finished:
            self.runagain(game)
        else:
            self._run(game)
