from function import *
from objclass import *
import pygame
from pygame.locals import *
from random import randint
print("ligma")
#initialize screen
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption("RHYTHMATICA")

#get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()

#make a new Surface filled with color white, because black is not my favorite color xD
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))

#load electron image, and append 10 intro_electron class with randomly given arguments.
electron = pygame.image.load("res/image/ingame/inside.png").convert_alpha()
electrons = []
for x in range(10):
    electrons.append(intro_electron(electron, randint(1, 10)/10, randint(1, 10)/10, randint(3, 5)/10))

#load logo, resize it a bit because it's T 0 0  T H I C C
logo = pygame.image.load("res/image/ingame/Rhythmatica.png").convert_alpha()
logo = pygame.transform.scale(logo, resize(logo.get_size(), 0.3))

#load font, render a text kindly. uhh, maybe not that kind... nevermind.
notoblack = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 50)
pressntostart = notoblack.render("Press N to start", 1, (0, 0, 0))

#load my cool intro uwu
intromusic = pygame.mixer.Sound("res/audio/effect/Rhythmatica.wav")

#aaand, finally we draw these shit to the screen! yay!
#first, blit the background.
screen.blit(background, (0, 0))
#intro_electron class have its own blit method, and will blit itself to the argument. so we call all of them.
for x in electrons:
    x.blit(screen)
#blit logo, kind(maybe not)text to the screen.
screen.blit(logo, get_center(screen.get_size(), logo.get_size()))
screen.blit(pressntostart, get_center(screen.get_size(), pressntostart.get_size(), (0.5, 0.75)))
#and... flip! now you can see everything in the screen!
pygame.display.flip()
intromusic.play()
while True:
    screen.blit(background, (0, 0))
    for x in electrons:
        x.blit(screen)
    screen.blit(logo, get_center(screen.get_size(), logo.get_size()))
    screen.blit(pressntostart, get_center(screen.get_size(), pressntostart.get_size(), (0.5, 0.75)))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == QUIT:
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_n:
                print("n pressed")
                break
    else:
        rolex.tick(130/60)#130 is the BPM of the song. BPM/60 makes BPM to beat per second, and I doubled it up to call these codes 2 times a beat.
        continue
    break