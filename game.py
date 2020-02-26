import os
import pygame
from pygame.locals import *
from os import listdir, scandir
from os.path import abspath, dirname, join

from module.load import *
from module import main

from module.const import *

# TODO: load mixer buffer, screen size, etc from the config file.

### initialization process ###

# Little Buffer, Less Delay!
pygame.mixer.pre_init(44100, -16, 2, 1024) 
pygame.init()

# set it's size, flags, caption.
display = pygame.display.set_mode(size = (1280, 720))#, flags = pygame.FULLSCREEN)
screen = pygame.Surface((1920, 1080))
pygame.display.set_caption("RHYTHMATICA")

# get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()

# All is well
print("ligma")

print("\n###################")
print("# RHYTHMATICA " + version + " #")
print("###################\n")

basepath = os.path.dirname(os.path.abspath(__file__))
print("Program Path is:", basepath)

# Load the resources.

res = load_resource(basepath)

main.intro(display, screen, rolex, res, basepath)