from function import *
from objclass import *
import pygame
from random import randint
print("ligma")
#initialize screen
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption("RHYTHMATICA")

#load logo and stuffs
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))

electron = pygame.image.load("res/image/ingame/inside.png").convert_alpha()
electrons = []
for x in range(10):
    electrons.append(intro_electron(electron, randint(1, 10)/10, randint(1, 10)/10, randint(3, 5)/10))

logo = pygame.image.load("res/image/ingame/Rhythmatica.png").convert_alpha()
logo = pygame.transform.scale(logo, resize(logo.get_size(), 0.3))

notoblack = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 50)
pressntostart = notoblack.render("Press N to start", 1, (0, 0, 0))

screen.blit(background, (0, 0)) 
for x in electrons:
    x.blit(screen)
screen.blit(logo, get_center(screen.get_size(), logo.get_size()))
screen.blit(pressntostart, get_center(screen.get_size(), pressntostart.get_size(), (0.5, 0.75)))
pygame.display.update()