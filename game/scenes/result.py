import pygame

from ..utils import blit_center_rel, scale_rel
from ..base.scene import TransitionableScene


class ResultField:
    def __init__(self, name, value, steps=10):
        self.name = name
        self.target_value = value
        self.show_value = 0
        self.increment = value / steps


class Result(TransitionableScene):
    def __init__(self, songdata, hits, misses, maxcombo, score,
                 prev_scene=None, fade_surface=None):
        self.songdata = songdata

        self.fields = [
            ResultField(name, value)
            for name, value in (
                ("hits", hits),
                ("misses", misses),
                ("maxcombo", maxcombo),
                ("score", score)
            )
        ]

        self.fade_surface = None

    def start(self):
        result = self.game.fonts['bold'].render("Result", True, "white")
        result = scale_rel(result, self.game.font_size_ratio * 1.5)
        bg_size = (self.game.screen.get_width(), result.get_height())
        result_bg = pygame.Surface(bg_size)
        result_bg.set_alpha(100)

        self.bg_surface = pygame.Surface(self.game.screen.get_size())
        self.bg_surface.fill("white")

        blit_center_rel(self.bg_surface, self.songdata.img_big, (0.5, 0.5))
        blit_center_rel(self.bg_surface, result_bg, (0.5, 0), (0.5, 0))
        blit_center_rel(self.bg_surface, result, (0.5, 0), (0.5, 0))

    def task(self):
        self.game.screen.blit(self.bg_surface, (0, 0))
