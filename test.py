def get_center(screen, surf, loc = (0.5, 0.5)):
    return ((screen[0] * loc[0]) - (surf[0] / 2), (screen[1] * loc[1]) - (surf[1] / 2))
def resize(surf, size):
    rtnlist = []
    for x in surf:
        rtnlist.append(int(x*size))
    return rtnlist
import pygame
print("ligma")
#initialize screen
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption("RHYTHMATICA")

#load logo and stuffs
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))
logo = pygame.image.load("res/ingame/Rhythmatica.png").convert()
logo = pygame.transform.scale(logo, resize(logo.get_size(), 0.4))
logo.set_colorkey((0, 0, 0))
notoblack = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 60)
pressntostart = notoblack.render("Press N to start", 1, (0, 0, 0))

screen.blit(background, (0, 0)) 
screen.blit(logo, get_center(screen.get_size(), logo.get_size()))
screen.blit(pressntostart, get_center(screen.get_size(), pressntostart.get_size(), (0.5, 0.75)))

pygame.display.update()