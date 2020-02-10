import pygame

from module.const import *

def resize(surf, size):
    return pygame.transform.scale(surf, [int(x * size) for x in surf.get_size()])

def resize_height(surf, desheight):
    #height:width = desheight:x
    #desheight * width / height = x
    height = surf.get_height()
    width = surf.get_width()
    return pygame.transform.scale(surf, (int(desheight * width / height), int(desheight)))

def resize_width(surf, deswidth):
    #height:width = x:deswidth
    #height * deswidth / width = x
    height = surf.get_height()
    width = surf.get_width()
    return pygame.transform.scale(surf, (int(deswidth), int(height * deswidth / width)))

def blit_center(screen, surf, loc, anchor = (0.5, 0.5)):
    """
    This will help you set the anchor point of the surface and blit it to the screen.
    if the presented loc is larger than 1, it will be treated as absolute location.
    else, it will be treated as relative location.
    it multiplies the anchor size to the size of the surface and add it to the location.
    """
    surfsize = surf.get_size()
    scrsize = screen.get_size()
    newloc = []
    for _loc, _surfsize, _scrsize, _anchor in zip(loc, surfsize, scrsize, anchor):
        if _loc >= 1:
            newloc.append(_loc - _surfsize * _anchor)
        else:
            newloc.append(_scrsize * _loc - _surfsize * _anchor)
    return screen.blit(surf, newloc)

def font_render(font, text, antialias = 10, color = BLACK, background = None):
    text_list = [font.render(x, antialias, color) for x in text.split("\n")]
    width = max([x.get_width() for x in text_list])
    height = sum([x.get_height() for x in text_list])
    if background:
        rtnsurf = pygame.Surface((width, height))
        rtnsurf.fill(background)
    else:
        rtnsurf = pygame.Surface((width, height), flags = pygame.SRCALPHA)
    ypos = 0
    for x in text_list:
        blit_center(rtnsurf, x, (0.5, ypos), (0.5, 0))
        ypos += x.get_height()
    return rtnsurf