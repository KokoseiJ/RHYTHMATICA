from base import Game
from intro import Intro
from play import Play

import logging

logger = logging.getLogger("RHYTHMATICA")
logger.setLevel("DEBUG")
handler = logging.StreamHandler()
logger.addHandler(handler)

game = Game((1600, 900))
game.init_pygame()
game.set_scene(Play)
game.run()
