import pygame

import random


def scale_rel(surface, factor, maxsize=None, func=None):
    if maxsize is None:
        maxsize = pygame.display.get_window_size()
    if func is None:
        func = pygame.transform.smoothscale

    if factor > 1:
        factor /= 100

    w, h = surface.get_size()
    newh = maxsize[1] * factor
    neww = maxsize[1] / h * w * factor

    return func(surface, (neww, newh))


def calc_size_rel(full_y, size, factor):
    if factor > 1:
        factor /= 100

    w, h = size
    newh = full_y * factor
    neww = full_y / h * w * factor

    return (neww, newh)


def blit_center(dest, src, loc, *args, **kwargs):
    w, h = src.get_size()
    x, y = loc

    newx = x - w / 2
    newy = y - h / 2

    return dest.blit(src, (newx, newy), *args, **kwargs)


def blit_center_rel(dest, src, factors, *args, **kwargs):
    srcw, srch = dest.get_size()
    w, h = src.get_size()
    fx, fy = factors

    x = srcw * fx
    y = srch * fy

    return blit_center(dest, src, (x, y), *args, **kwargs)


def get_random_color():
    return tuple(random.choices(range(256), k=3))
