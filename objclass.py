import pygame
from function import *
class intro_electron:
    def __init__(self, img, loc_x, loc_y, size):
        self.img = img
        self.loc = (loc_x, loc_y)
        self.size = size
        self.isbig = False
    def blit(self, screen):
        if self.isbig:
            self.isbig = False
            self.resizedimg = resize(self.img, self.size)
        else:
            self.isbig = True
            self.resizedimg = resize(self.img, self.size + 0.1)
        blit_center(screen, self.resizedimg, self.loc)