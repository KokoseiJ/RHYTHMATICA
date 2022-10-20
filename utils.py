import pygame

import random


def calc_size_rel(full_y, size, factor):
    if factor > 1:
        factor /= 100

    w, h = size
    newh = full_y * factor
    neww = full_y / h * w * factor

    return (neww, newh)


def scale_rel(surface, factor, maxsize=None, func=None):
    if maxsize is None:
        maxsize = pygame.display.get_window_size()
    if func is None:
        func = pygame.transform.smoothscale

    if factor > 1:
        factor /= 100

    newsize = calc_size_rel(maxsize[1], surface.get_size(), factor)

    return func(surface, newsize)


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


def text_multiline(font, text, *args, **kwargs):
    renders = [font.render(line.strip(), *args, **kwargs).convert_alpha()
               for line in text.split("\n")]

    sizes = [render.get_size() for render in renders]
    total_w = max([size[0] for size in sizes])
    total_h = sum([size[1] for size in sizes])

    surface = pygame.Surface((total_w, total_h), pygame.SRCALPHA)

    y = 0

    for i in range(len(renders)):
        w, h = sizes[i]
        x = (total_w - w) / 2
        surface.blit(renders[i], (x, y))
        y += h

    return surface


def get_random_color():
    return tuple(random.choices(range(256), k=3))
