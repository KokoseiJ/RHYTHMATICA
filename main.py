from game.base.game import Game
from game.scenes.intro import Intro

import logging

logger = logging.getLogger("RHYTHMATICA")
logger.setLevel("DEBUG")

handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(module)s::%(funcName)s | %(message)s",
    "%Y/%m/%d %H:%M:%S"
)

handler.setFormatter(formatter)
logger.addHandler(handler)

game = Game((1920, 1080), fullscreen=True, fps=0, show_fps=True)
game.init_pygame()
game.set_scene(Intro)
game.run()
