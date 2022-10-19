import pygame

from base import Scene
from utils import blit_center_rel

import time
import random
import logging

logger = logging.getLogger("RHYTHMATICA")


class Play(Scene):
    def __init__(self):
        super().__init__()

    def start(self):
        self.game.screen.fill("orange")

    def task(self):
        pass
