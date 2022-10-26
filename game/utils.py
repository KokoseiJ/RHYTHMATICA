import pygame

import time
import random


class SmoothMoveXY:
    def __init__(self, surface, orig, dest, duration):
        self.surface = surface
        self.orig = orig
        self.dest = dest
        self.duration = duration
        self.starttime = None

        self.distance_x = dest[0] - orig[0]
        self.start_speed_x = 2 * self.distance_x / duration
        self.acceleration_x = -self.start_speed_x / duration

        self.distance_y = dest[1] - orig[1]
        self.start_speed_y = 2 * self.distance_y / duration
        self.acceleration_y = -self.start_speed_y / duration

    @property
    def is_started(self):
        return self.starttime is not None

    @property
    def elapsed_time(self):
        if self.is_started:
            return time.perf_counter() - self.starttime
        else:
            return None

    @property
    def is_running(self):
        return self.is_started and not self.elapsed_time > self.duration

    def start(self):
        self.starttime = time.perf_counter()

    def reset(self):
        self.starttime = None

    def get_pos(self):
        return self._get_pos(self.elapsed_time)

    def draw(self, surface):
        return surface.blit(self.surface, self.get_pos())

    def _get_pos(self, time_):
        if not self.is_started:
            cur_pos = self.orig
        elif self.elapsed_time <= self.duration:
            # s = v0t + 1/2at^2
            cur_pos_x = (
                self.orig[0]
                + self.start_speed_x * time_
                + self.acceleration_x * time_**2 / 2
            )
            cur_pos_y = (
                self.orig[1]
                + self.start_speed_y * time_
                + self.acceleration_y * time_**2 / 2
            )
            cur_pos = (cur_pos_x, cur_pos_y)
        else:
            cur_pos = self.dest

        return cur_pos


def calc_size_rel(full_y, size, factor):
    if factor > 1:
        factor /= 100

    w, h = size
    newh = full_y * factor
    neww = full_y / h * w * factor

    return (neww, newh)


def calc_center(srcsize, loc, center_factor=(0.5, 0.5)):
    w, h = srcsize
    return (loc[0] - w * center_factor[0], loc[1] - h * center_factor[1])


def calc_loc_rel(srcsize, factors):
    return (srcsize[0] * factors[0], srcsize[1] * factors[1])


def scale_rel(surface, factor, maxsize=None, func=None):
    if maxsize is None:
        maxsize = pygame.display.get_window_size()
    if func is None:
        func = pygame.transform.smoothscale

    newsize = calc_size_rel(maxsize[1], surface.get_size(), factor)

    return func(surface, newsize)


def blit_center(dest, src, loc, center=(0.5, 0.5), *args, **kwargs):
    return dest.blit(
        src, calc_center(src.get_size(), loc, center), *args, **kwargs)


def blit_center_rel(dest, src, factors, center=(0.5, 0.5), *args, **kwargs):
    loc_rel = calc_loc_rel(dest.get_size(), factors)
    return blit_center(dest, src, loc_rel, center, *args, **kwargs)


def text_multiline(font, text, *args, background=None, bg_alpha=128,
                   centered=True, **kwargs):
    renders = [font.render(line.strip(), *args, **kwargs)
               for line in text.split("\n")]

    sizes = [render.get_size() for render in renders]
    total_w = max([size[0] for size in sizes])
    total_h = sum([size[1] for size in sizes])

    surface = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
    if background:
        if not isinstance(background, pygame.Color):
            background = pygame.Color(background)

        background.a = bg_alpha

        surface.fill(background)

    y = 0

    for i in range(len(renders)):
        w, h = sizes[i]
        x = (total_w - w) / 2 if centered else 0
        surface.blit(renders[i], (x, y))
        y += h

    return surface


def get_random_color():
    return tuple(random.choices(range(256), k=3))
