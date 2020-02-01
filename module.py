import pygame
from pydub import AudioSegment

def load_sound(filepath):
	return pygame.mixer.Sound(AudioSegment.from_file(filepath).raw_data)

	