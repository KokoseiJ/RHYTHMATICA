import os
import pygame
from pygame.locals import *
from pygame.image import load as load_image
from os import listdir
from os.path import abspath, dirname, join

from module import *

version = "A6P"

# TODO: load mixer buffer, screen size, etc from the config file.

### initialization process ###

# Little Buffer, Less Delay!
pygame.mixer.pre_init(44100, -16, 2, 1024) 
pygame.init()

# set it's size, flags, caption.
screen = pygame.display.set_mode(size = (1280, 720))#, flags = pygame.FULLSCREEN)
pygame.display.set_caption("RHYTHMATICA")

# get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()

print("\n###################")
print("# RHYTHMATICA " + version + " #")
print("###################\n")

##### Loading Sequence #####
basepath = dirname(abspath(__file__))
print("Program Path is:", basepath)

### Loading Images ###
print("\nLoading Images...\n")
imgpath = join(basepath, "res", "image")

print("Loading logo image... ", end = "")
logo = load_image(join(imgpath, "logo.png")).convert_alpha()
print("Done.")

print("Loading loading image... ", end = "")
loading = load_image(join(imgpath, "loading.png")).convert()
print("Done.")

print("Loading outside images... ", end = "")
outside = [load_image(join(imgpath, "outside", str(x) + ".png")).convert_alpha() for x in range(1, 7)]
print("Done.")

print("Loading inside images... ", end = "")
inside = [load_image(join(imgpath, "inside", str(x) + ".png")).convert_alpha() for x in range(1, 7)]
print("Done.")

print("Loading outline image... ", end = "")
outline = load_image(join(imgpath, "outline.png")).convert_alpha()
print("Done.")

print("Loading judge images... ", end = "")
judge = dict([[x.split(".")[0], load_image(join(imgpath, "judge", x)).convert_alpha()] for x in listdir(join(imgpath, "judge"))])
print("Done.")

print("Loading rating images... ", end = "")
rating = dict([[x.split(".")[0], load_image(join(imgpath, "rating", x)).convert_alpha()] for x in listdir(join(imgpath, "rating"))])
print("Done.")

### Loading sound ###
print("\nLoading Sound files...\n")
soundpath = join(basepath, "res", "sound")

sound = {}

for x in os.listdir(soundpath):
	print("Loading " + x.split('.')[0] + " sound... ", end = "")
	sound[x.split(".")[0]] = load_sound(join(soundpath, x))
	print("Done.")

### Loading fonts ###
print("\nLoading Fonts...", end = "")
fontpath = join(basepath, "res", "fonts")

font = dict([[x.split(".")[0], pygame.font.Font(join(fontpath, x), 10)] for x in os.listdir(fontpath) if x.split(".")[-1] == "ttf"])
print("Done.\n")

print("Finished loading.")
