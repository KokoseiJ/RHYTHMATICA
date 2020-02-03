import os
import pygame
from pygame.locals import *

from module import *

version = "A6P"

# TODO: load mixer buffer, screen size, etc from the config file.

### initialization process ###

# Little Buffer, Less Delay!
pygame.mixer.pre_init(44100, -16, 2, 1024) 
pygame.init()

# set it's size, flags, caption.
display = pygame.display.set_mode(size = (1280, 720))#, flags = pygame.FULLSCREEN)
screen = pygame.Surface(display.get_size())
pygame.display.set_caption("RHYTHMATICA")

# get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()

print("\n###################")
print("# RHYTHMATICA " + version + " #")
print("###################\n")

basepath = dirname(abspath(__file__))
print("Program Path is:", basepath)

# Load the resources.

img, sound, font = load_resource(basepath, screen.get_size())

# let's go to intro sequence

electrons = [electron(img['inside'], screen.get_size()) for x in range(10)]

sound["main"].play()

while True:
    screen.fill((WHITE))
    for x in electrons:
        x.get(screen)

    blit_center(screen, img['logo'], (0.5, 0.5))
    
    text = font_render(font['bold'], "Press N to Start")
    blit_center(screen, text, (0.5, 0.75))

    update(display, screen, FPSrender(rolex, font['black']))
    rolex.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_n:
                break
    else:  continue
    break