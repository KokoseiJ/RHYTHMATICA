import pygame
from function import *
class intro_electron:
	def __init__(self, img, loc_x, loc_y, size):
		self.img = pygame.transform.scale(img, resize(img.get_size(), size))
		self.loc = (loc_x, loc_y)
		self.size = size
		self.isbig = False
	def blit(self, screen):
		if self.isbig:
			self.isbig = False
			self.resizedimg = pygame.transform.scale(self.img, resize(self.img.get_size(), self.size))
		else:
			self.isbig = True
			self.resizedimg = pygame.transform.scale(self.img, resize(self.img.get_size(), self.size + 0.2))
		screen.blit(self.resizedimg, get_center(screen.get_size(), self.resizedimg.get_size(), self.loc))