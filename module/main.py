import pygame
from pygame.locals import *
from pygame.transform import scale

from module.transform import *
from module.classes import *
from module.misc import *

from module.const import *

def fadeout(display, screen, image, rolex, fps = 60, duration = 1.5):
    image = scale(image, screen.get_size()).convert()
    opacity = 0
    tmpscreen = screen.copy()
    for x in range(int(fps * duration)):
        screen.blit(tmpscreen, (0, 0))
        image.set_alpha(opacity)
        screen.blit(image, (0, 0))
        opacity += (255 / (fps * duration))
        update(display, screen, FPSrender(rolex))
        rolex.tick(fps)

def fadein(display, screen, tmpscreen, image, rolex, fps = 60, duration = 1.5):
    image = scale(image, screen.get_size()).convert()
    opacity = 255
    for x in range(int(fps * duration)):
        screen.blit(tmpscreen, (0, 0))
        tmpimage = image.copy()
        tmpimage.set_alpha(opacity)
        screen.blit(tmpimage, (0, 0))
        opacity -= (255 / (fps * duration))
        update(display, screen, FPSrender(rolex))
        rolex.tick(fps)

def intro(display, screen, rolex, res):
    # let's go to intro sequence
    img, sound, font = res
    electrons = [electron(img['inside'], screen.get_size()) for x in range(10)]

    sound["main"].play()

    while True:
        screen.fill((WHITE))
        for x in electrons:
            x.get(screen)

        blit_center(screen, img['logo'], (0.5, 0.5))
    
        starttext = font_render(font['bold'], "Press N to Start")
        blit_center(screen, starttext, (0.5, 0.75))

        vertext = font_render(font['bold'], "Ver: " + version)
        blit_center(screen, vertext, (1, 1), (1, 1))

        update(display, screen, FPSrender(rolex))
        rolex.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_n:
                    sound['main'].stop()
                    sound['start'].play()
                    tmpscreen = screen.copy()
                    fadeout(display, screen, img['loading'], rolex)
                    fadein(display, screen, tmpscreen, img['loading'], rolex)
                    return