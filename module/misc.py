import pygame

from module.const import *

def FPSrender(clock):
    fps = int(clock.get_fps())
    return pygame.font.Font(None, 100).render(str(fps), 0, BLACK)

def update(display, screen, FPS = None):
    #TODO: make a letterbox option. It will gonna look shitty on non 16:9 screen such as my 16:10 one
    """ 
    Scale the surface to fit the display size and blit it to the screen, and update the display.
    all of the pygame.display.update() function will be replaced with this one.
    """
    resize = pygame.transform.scale(screen, display.get_size())
    display.blit(resize, (0, 0))
    if FPS:
        display.blit(FPS, (0, 0))
    return pygame.display.update()