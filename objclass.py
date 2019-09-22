#This code contains classes that can be used in RHYTHMATICA.
#Copyright (C) 2019, Wonjun Jung

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <https://www.gnu.org/licenses/>.
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
class songpack:
    def __init__(self, path):
        """
        0|Flamingo #name
        1|Kero Kero Bonito #artist
        2|89 #bpm
        3|1489 #note
        #difficulty: ~2 easy 3~5 medium 6~ hard
        """
        try:
            self.path = path
            self.image = pygame.image.load("note/" + path + "/img.png").convert()
            self.music = pygame.mixer.Sound("note/" + path + "/song.wav")
            self.pre = pygame.mixer.Sound("note/" + path + "/pre.wav")
            self.notelist = open("note/" + path + "/note.txt").read().split("\n")
            self.name, self.artist, bpm, notes = open("note/" + path + "/info.txt").read().split("\n")[0:4]
            self.bpm = float(bpm)
            notepersec = int(notes) / self.music.get_length()
            if notepersec < 3:
                self.difficulty = "EASY"
            elif 3 <= notepersec < 6:
                 self.difficulty = "MEDIUM"
            elif 6 <= notepersec < 10:
                self.difficulty = "HARD"
            elif 10 <= notepersec:
                self.difficulty = "EXTREME"
            self.errmsg = False
        except Exception as e:
            self.errmsg = (1, "0of, seems like your songpack is corrupted!", e)
        finally:
            return
    def get_surf(self, size, fonts):
        rtnsurf = pygame.Surface(size).convert()
        white = pygame.Surface(size).convert()
        white.fill((255, 255, 255))
        bg = pygame.transform.scale(self.image, size)
        bg.set_alpha(100)
        preview = resize_height(self.image, rtnsurf.get_height() / 2)
        txt = multilinerender(fonts['regular'], self.name+"\nArtist:"+self.artist+"\nBPM:"+str(self.bpm)+"\nDifficulty:"+self.difficulty, 5)
        txt = resize_height(txt, rtnsurf.get_height() / 3)
        guide = multilinerender(fonts['black'], "Press T, Y to change the speed\nPress G, H to change the song.\nPress N to start the game.", 5)
        guide = resize_height(guide, rtnsurf.get_height() / 6)
        rtnsurf.blit(white, (0, 0))
        rtnsurf.blit(bg, (0, 0))
        blit_center(rtnsurf, preview, (0.5, 0), (0.5, 0))
        blit_center(rtnsurf, txt, (0.5, 0.5), (0.5, 0))
        blit_center(rtnsurf, guide, (0.5, 1), (0.5, 1))
        return rtnsurf