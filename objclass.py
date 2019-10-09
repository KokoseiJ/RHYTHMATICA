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
        return
    def blit(self, screen):
        if self.isbig:
            self.isbig = False
            self.resizedimg = resize(self.img, self.size)
        else:
            self.isbig = True
            self.resizedimg = resize(self.img, self.size + 0.05)
        blit_center(screen, self.resizedimg, self.loc)
        return
class songpack:
    def __init__(self, path, fonts):
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
            self.font = fonts
            self.name, self.artist, bpm, notes = open("note/" + path + "/info.txt").read().split("\n")[0:4]
            if '.' in bpm:
                self.bpm = float(bpm)
            else:
                self.bpm = int(bpm)
            self.blit_size = 0
            self.blit_xloc = 0
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
    def get_surf(self, size):
        rtnsurf = pygame.Surface(size).convert()
        white = pygame.Surface(size).convert()
        white.fill((255, 255, 255))
        bg = pygame.transform.scale(self.image, size)
        bg.set_alpha(100)
        preview = resize_height(self.image, rtnsurf.get_height() / 2)
        txt = multilinerender(self.font['regular'], self.name+"\nArtist:"+self.artist+"\nBPM:"+str(self.bpm)+"\nDifficulty:"+self.difficulty, 10)
        txt = resize_height(txt, rtnsurf.get_height() / 3)
        guide = multilinerender(self.font['black'], "Press T, Y to change the speed.\nPress G, H to change the song.\nPress N to start the game.", 10)
        guide = resize_height(guide, rtnsurf.get_height() / 6)
        rtnsurf.blit(white, (0, 0))
        rtnsurf.blit(bg, (0, 0))
        blit_center(rtnsurf, preview, (0.5, 0), (0.5, 0))
        blit_center(rtnsurf, txt, (0.5, 0.5), (0.5, 0))
        blit_center(rtnsurf, guide, (0.5, 1), (0.5, 1))
        return rtnsurf
    def move_left(self, screen, mode, times): #0: main 1: slave
        resizedimg = resize(resize_height(self.image, screen.get_height() / 2), self.blit_size)
        blit_center(screen, resizedimg, (self.blit_xloc, 0.25))
        self.blit_xloc -= 0.5 / times
        if mode == 0:
            self.blit_size -= 1 / times
        if mode == 1:
            self.blit_size += 1 / times
        return
    def move_right(self, screen, mode, times): #0: main 1: slave
        resizedimg = resize(resize_height(self.image, screen.get_height() / 2), self.blit_size)
        blit_center(screen, resizedimg, (self.blit_xloc, 0.25))
        self.blit_xloc += 0.5 / times
        if mode == 0:
            self.blit_size -= 1 / times
        if mode == 1:
            self.blit_size += 1 / times
        return
class note:
    def __init__(self, keynumb, judgenumb, img):
        self.keynumb = keynumb
        self.img = img
        self.judgenumb = judgenumb
        if keynumb % 2:
            self.xloc = 0.65
        else:
            self.xloc = 0.35
        if keynumb < 2:
            self.yloc = 0.2
        elif keynumb < 4:
            self.yloc = 0.5
        else:
            self.yloc = 0.8
        self.orig_size = 2.5
        self.size = self.orig_size
        self.des_size = 1
        self.delete = False
        return
    def blit(self, screen, curjudge, fps, duration):
        if curjudge[self.keynumb] > self.judgenumb:
            return 1
        img = resize(self.img, self.size)
        blit_center(screen, img, (self.xloc, self.yloc))
        if self.size <= self.des_size:
            return 1
        else:
            self.size -= (self.orig_size - self.des_size) / (fps * duration)
            return 0