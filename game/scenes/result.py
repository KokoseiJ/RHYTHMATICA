import pygame

from ..base.task import Task, WaitForTask
from ..utils import blit_center_rel, scale_rel, text_multiline
from ..base.scene import TransitionableScene

import os
import time
import logging

logger = logging.getLogger("RHYTHMATICA")


class ResultField:
    def __init__(self, name, value, steps=60):
        self.name = name
        self.target_value = value
        self.value = 0
        self.increment = value / steps

    @property
    def is_finished(self):
        return self.value >= self.target_value

    def stepup(self):
        if self.value < self.target_value:
            self.value += self.increment

    def get(self):
        if self.value < self.target_value:
            return round(self.value)
            self.value += self.increment
        else:
            return self.target_value


class ResultTask(Task):
    def __init__(self, fields, sound, fontsize=1):
        super().__init__(self.func, name="Result")
        self.fields = fields
        self.sound = sound
        self.fontsize = 1
        self.next_update = None
        self.update_interval = 0.05

    def set_starttime(self, interval=1):
        self.next_update = time.perf_counter() + interval

    def draw_current_fields(self, game):
        text = "\n".join([
            f"{field.name}: {field.get()}" for field in self.fields
        ])

        render = text_multiline(
            game.fonts['regular'], text, 1, "black", centered=False)

        if self.fontsize != 1:
            render = scale_rel(render, game.font_size_ratio * self.fontsize)

        return render

    def func(self, self_, game):
        render = self.draw_current_fields(game)
        blit_center_rel(game.screen, render, (0, 0.5), (0, 0.5))

        if (not self.fields[-1].is_finished) and \
                time.perf_counter() > self.next_update:
            [field.stepup() for field in self.fields if not field.is_finished]
            self.sound.play()
            self.next_update += self.update_interval
        
        self.runagain(game)


class Result(TransitionableScene):
    def __init__(self, songdata, hits, misses, maxcombo, score,
                 prev_scene=None, fade_bg=None):
        super().__init__()
        self.songdata = songdata

        self.fields = [
            ResultField(name, value)
            for name, value in (
                ("Hits", hits),
                ("Misses", misses),
                ("Max Combo", maxcombo),
                ("Score", round(score))
            )
        ]

        self.fade_bg = fade_bg

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

        fade_task = self.start_fade()

        sound = pygame.mixer.Sound(os.path.join("res", "sound", "coin.ogg"))
        result_task = ResultTask(self.fields, sound)

        task = WaitForTask(self.fadein_callback, fade_task, result_task)

        self.game.add_task(task)

    def fadein_callback(self, task, game, result_task):
        game.add_task(result_task)
        result_task.set_starttime()
        pygame.mixer.music.load(os.path.join("res", "sound", "result.mp3"))
        pygame.mixer.music.play()

    def task(self):
        self.game.screen.blit(self.bg_surface, (0, 0))
