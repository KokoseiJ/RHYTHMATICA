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
			self.size -= 0.2
		else:
			self.isbig = True
			self.size += 0.2
		self.img = pygame.transform.scale(self.img, resize(self.img.get_size(), self.size))
		screen.blit(self.img, get_center(screen.get_size(), self.img.get_size(), self.loc))