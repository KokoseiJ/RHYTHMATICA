'''
RHYTHMATICA is a simple rhythm game, desinged by Kokosei J a.k.a Wonjun Jung.
Copyright (C) 2019, Wonjun Jung

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
#####Import Modules#####
from function import *
from objclass import *
import pygame
from pygame.locals import *
from random import randint
import os
print("ligma")


#####initialization process#####
pygame.mixer.pre_init(44100, -16, 2, 1024) #Little Buffer, Less Delay!
pygame.init() #initialize pygame.

#set it's size, flags, caption.
screen = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption("RHYTHMATICA")

#get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()


#####set required variables#####
songnumb = 0 #songnumb should be set as 0.
desiredfps = 60 #set fps.
speed = 1.00
keylist = (K_t, K_y, K_g, K_h, K_b, K_n)
loc = ((0.35, 0.2), (0.65, 0.2), (0.35, 0.5), (0.65, 0.5), (0.35, 0.8), (0.65, 0.8))

#####make/load/process resources#####
#make a new Surface filled with color white, because black is not my favorite color xD
whitebg = pygame.Surface(screen.get_size()).convert()
whitebg.fill((255, 255, 255))

#load electron image, resize it and append 10 intro_electron class with randomly given arguments.
electron = pygame.image.load("res/image/ingame/inside1.png").convert_alpha()
electron = resize_height(electron, screen.get_height())
electrons = []
for x in range(10):
    electrons.append(intro_electron(electron, randint(1, 10)/10, randint(1, 10)/10, randint(1, 2)/10))

outside = tuple(map(lambda x:  pygame.image.load("res/image/ingame/outside"+str(x+1)+".png").convert_alpha(), range(6)))

outline = pygame.image.load("res/image/ingame/outsidecover.png").convert_alpha()
outline = resize_height(outline, screen.get_height() * 0.25)

hitimg = pygame.image.load("res/image/ingame/hit.png").convert_alpha()
hitimg = resize_onload(screen, hitimg, 0.4)

missimg = pygame.image.load("res/image/ingame/miss.png").convert_alpha()
missimg = resize_onload(screen, missimg, 0.4)

#load logo, resize it a bit because it's T 0 0  T H I C C
logo = pygame.image.load("res/image/ingame/Rhythmatica.png").convert_alpha()
logo = resize_onload(screen, logo, 0.7)

#load the loding screen, I won't resize it as long as it will be resized in fadeout/fadein functions. :accreate:
loadimg = pygame.image.load("res/image/ingame/loading_wide.png").convert()

#load font, render a text kindly. uhh, maybe not that kind... nevermind.
noto = {}
noto['black'] = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 100)
noto['regular'] = pygame.font.Font("res/fonts/NotoSans-Regular.ttf", 100)
pressntostart = noto['black'].render("Press N to start", 10, (0, 0, 0)).convert_alpha()
pressntostart = resize_onload(screen, pressntostart, 0.3)

#load my cool intro uwu
intromusic = pygame.mixer.Sound("res/audio/effect/Rhythmatica.wav")

#load the effect sounds.
startsound = pygame.mixer.Sound("res/audio/effect/start.wav")
changeeffect = pygame.mixer.Sound("res/audio/effect/nextsong.wav")

#####aaand, finally we draw all these shit to the screen! yay!#####

#at the start, we play the song.

intromusic.play()

#####This is the intro code!#####
while True: # Let's repeat this until python breaks something.
    #first, blit the background.
    screen.blit(whitebg, (0, 0))
    #intro_electron class have its own blit method, and will blit itself to the argument. so we call all of them.
    for x in electrons:
        x.blit(screen)
    #blit logo, kind(maybe not)text to the screen.
    blit_center(screen, logo)
    blit_center(screen, pressntostart, (0.5, 0.75))
    #and... flip! now you can see everything in the screen!
    pygame.display.flip()
    intro_beattime = pygame.time.get_ticks()
    #now it's time to handle some events.
    for event in pygame.event.get(): #get all of the events in the queue.
        if event.type == QUIT: #if user tried to close the window?
            exit() #kill the python. simple
        elif event.type == KEYDOWN: #if user pressed the key?
            if event.key == K_n: #if the key that user pressed is N?
                print("n pressed") #first, print it in the console for debug purpose.
                break #and, get outta here.
    else: #if nothing broke:
        #130 is the BPM of the song. BPM/60 makes BPM to beat per second, and I doubled it up to call these codes 2 times a beat.
        rolex.tick(130 / 60 * 2)
        continue #let's keep this loop.
    break #if something broke, it will break this loop too.
intromusic.stop() #stop the music.
startsound.play() #and start the start-effect sound.
fadeout_screen(rolex, screen, screen, loadimg) #call the fadeout thing


#####Selection Codes starts from here!#####
#flush the songpacks list.
songpacks = []
#load the note directory.
try:
    songlists = os.listdir("note")
except: #if there was no note folder?
    songlists = [] #set it to blank.
    os.mkdir("note")
if not songlists: #if the folder is empty:
    print("ur note folder is empty. gtfo") #heh
    exit()
#get all the folders, make instances with it
for x in songlists:
    #make instance with it's own fontset.
    song = songpack(x, noto)
    #if there was an error:
    if song.errmsg:
        #print error to the screen, for the troubleshoot.
        print(song.errmsg[1])
        print(str(song.errmsg[2].__class__.__name__)+":", song.errmsg[2])
        print("path:", song.path)
    else:
        #print infos to check if it's parsed
        print(song.name, song.artist, song.bpm, song.difficulty)
        songpacks.append(song)
    print()
songnumb_max = len(songpacks) #get the number of songs available.
if songnumb >= songnumb_max: #if somehow songnumb is higher than the songnumb_max:
    print("wot m8 u deleted music while playing? impressive job") #it doesn't usally happen so... that really is impressing job
    songnumb = 0 #to prevent errors, we restore songnumb to 0

#get the selection screen from the songpack instance.
tmpscreen = songpacks[songnumb].get_surf(screen.get_size())
screen.blit(songpacks[songnumb].get_surf(screen.get_size()), (0, 0))
speedstr = str(speed)
if len(speedstr) == 3:
    speedstr += '0'
speedtxt = noto['regular'].render("Speed: x" + speedstr, 10, (0, 0, 0), None)
speedtxt = resize_onload(tmpscreen, speedtxt, 0.15)
blit_center(tmpscreen, speedtxt, (1, 1), (1, 1))
#fadein.
fadein_screen(rolex, screen, tmpscreen, loadimg)
#play the preview song.
songpacks[songnumb].pre.play()

#flush the event queue, to prevent some troubles that will happen when players pressing their keyboard...
pygame.event.clear()

#Repeat this while python breaks something, again:
while True:
    for event in pygame.event.get(): #get all of the events in the queue.
        if event.type == QUIT: #if user tried to close the window?
            exit() #kill the python. simple
        elif event.type == KEYDOWN: #if user pressed the key?
            if event.key == keylist[0]:
                if speed > 0.25:
                    speed -= 0.25
                    screen.blit(songpacks[songnumb].get_surf(screen.get_size()), (0, 0))
                    speedstr = str(speed)
                    if len(speedstr) == 3:
                        speedstr += '0'
                    speedtxt = noto['regular'].render("Speed: x" + speedstr, 10, (0, 0, 0), None)
                    speedtxt = resize_onload(screen, speedtxt, 0.15)
                    blit_center(screen, speedtxt, (1, 1), (1, 1))
                    #flip!
                    pygame.display.update()

            elif event.key == keylist[1]:
                if speed < 5:
                    speed += 0.25
                    screen.blit(songpacks[songnumb].get_surf(screen.get_size()), (0, 0))
                    speedstr = str(speed)
                    if len(speedstr) == 3:
                        speedstr += '0'
                    speedtxt = noto['regular'].render("Speed: x" + speedstr, 10, (0, 0, 0), None)
                    speedtxt = resize_onload(screen, speedtxt, 0.15)
                    blit_center(screen, speedtxt, (1, 1), (1, 1))
                    #flip!
                    pygame.display.update()

            elif event.key == keylist[2]: #If the key that user pressed is G?
                songpacks[songnumb].pre.stop() #stops the preview song.
                changeeffect.play() #play the change effect sound.
                prevsongnumb = songnumb #back up the previous song number, to show the song-changing effect
                #Shift the songnumb.
                if songnumb == 0: 
                    songnumb = songnumb_max - 1
                else:
                    songnumb -= 1
                #move the images.
                move_right(rolex, screen, whitebg, songpacks[prevsongnumb], songpacks[songnumb], desiredfps)
                #get a information surface from songpack instance
                screen.blit(songpacks[songnumb].get_surf(screen.get_size()), (0, 0))
                speedstr = str(speed)
                if len(speedstr) == 3:
                    speedstr += '0'
                speedtxt = noto['regular'].render("Speed: x" + speedstr, 10, (0, 0, 0), None)
                speedtxt = resize_onload(screen, speedtxt, 0.15)
                blit_center(screen, speedtxt, (1, 1), (1, 1))
                #flip!
                pygame.display.update()
                pygame.time.wait(100) #wait a bit.
                songpacks[songnumb].pre.play() #play the song.

            elif event.key == keylist[3]: #Almost same as above.
                songpacks[songnumb].pre.stop()
                changeeffect.play()
                prevsongnumb = songnumb
                if songnumb == songnumb_max - 1:
                    songnumb = 0
                else:
                    songnumb += 1
                move_left(rolex, screen, whitebg, songpacks[prevsongnumb], songpacks[songnumb], desiredfps)
                screen.blit(songpacks[songnumb].get_surf(screen.get_size()), (0, 0))
                speedstr = str(speed)
                if len(speedstr) == 3:
                    speedstr += '0'
                speedtxt = noto['regular'].render("Speed: x" + speedstr, 10, (0, 0, 0), None)
                speedtxt = resize_onload(screen, speedtxt, 0.15)
                blit_center(screen, speedtxt, (1, 1), (1, 1))
                pygame.display.update()
                pygame.time.wait(100)
                songpacks[songnumb].pre.play()

            elif event.key == keylist[5]: #if the key that user pressed is N?
                print("n pressed") #first, print it in the console for debug purpose.
                break #proceed to the next step!
    else: #If nothing broke:
        continue #do it uinthill they break something
    break #boom
songpacks[songnumb].pre.stop()
startsound.play() #and start the start-effect sound.
fadeout_screen(rolex, screen, screen, loadimg)

#####Preparation Process#####
#load notes.
cursongpack = songpacks[songnumb]
notelist = get_note(cursongpack.notelist)
noteamount = sum(map(lambda x:  len(x), notelist))

#set some variables.
duration = (60 / cursongpack.bpm) / speed
notes = []

ispressed = [0, 0, 0, 0, 0, 0]
shownote = [0, 0, 0, 0, 0, 0]
judgenote = [0, 0, 0, 0, 0, 0]

score = 0
maxcombo = 0
combo = 0
hit = 0
miss = 0
judge_count = [0, 0, True]
ishit = False
ismiss = False

#draw circles.
background = pygame.Surface(screen.get_size()).convert()
musicbg = cursongpack.image
scrsize = screen.get_size()
imgsize = musicbg.get_size()
if imgsize[0] < imgsize[1]:
    musicbg = resize_width(musicbg, scrsize[0])
else:
    musicbg = resize_height(musicbg, scrsize[1])
musicbg.set_alpha(100)

background.blit(whitebg, (0, 0))
blit_center(background, musicbg)
nametxt = noto['black'].render(cursongpack.artist + " - " + cursongpack.name, 10, (255, 255, 255), None)
nametxt = resize_onload(screen, nametxt, 0.4)
nametxt_bg = pygame.Surface((screen.get_width(), nametxt.get_height()))
nametxt_bg.fill((0, 0, 0))
nametxt_bg.set_alpha(100)
blit_center(background, nametxt_bg, (0.5, 0), (0.5, 0))
blit_center(background, nametxt, (0.5, 0), (0.5, 0))

for x in range(6):
    inside = pygame.image.load("res/image/ingame/inside"+str(x+1)+".png").convert_alpha()
    inside = resize_height(inside, screen.get_height() * 0.25)
    blit_center(background, inside, loc[x])
tmpscreen = pygame.Surface(screen.get_size()).convert()
tmpscreen.blit(background, (0, 0))
for x in range(6):
    blit_center(tmpscreen, outline, loc[x])

fadein_screen(rolex, screen, tmpscreen, loadimg)

starttime = pygame.time.get_ticks()
cursongpack.music.play()

while pygame.mixer.get_busy():
    curtime = get_times(starttime)
    curfps = rolex.get_fps()
    screen.blit(background, (0, 0))
    scoreimg = noto['regular'].render(str(int(score)), 10, (0, 0, 0), None)
    scoreimg = resize_height(scoreimg, screen.get_height() * 0.1)
    blit_center(screen, scoreimg, (0.5, 1), (0.5, 1))
    #####detecting keypress / exit signal, judgement when keydown, gets each key's status(pressed or not)#####
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                songpacks[songnumb].music.stop()
            for key, numb in zip(keylist, range(6)):
                if event.key == key:
                    ispressed[numb] = 1
                    if not len(notelist[numb]) <= judgenote[numb]:
                        judgeres = judge(starttime, notelist[numb][judgenote[numb]], duration)
                        if judgeres:
                            #print(judgeres)
                            judgenote[numb] += 1
                            if judgeres == 1:
                                score += 10000 / noteamount
                                combo += 1
                                if combo > maxcombo:  maxcombo = combo
                                hit += 1
                                ishit = True
                                ismiss = False
                                judge_count = [0, 0, True]
                            else:
                                combo = 0
                                miss += 1
                                ishit = False
                                ismiss = True
                                judge_count = [0, 0, True]
                            break
        elif event.type == KEYUP:
            for key, numb in zip(keylist, range(6)):
                if event.key == key:
                    ispressed[numb] = 0
                    break
        elif event.type == QUIT:#if user tried to close the window?
            exit() #kill the python. simple
    #####Draw outlines#####
    for pressed, _loc in zip(ispressed, loc):
        if pressed:
            outline_mod = resize(outline, 1.1)
        else:
            outline_mod = resize(outline, 1)
        blit_center(screen, outline_mod, _loc)
    #####Spawn notes#####
    for x in range(6):
        if not len(notelist[x]) <= shownote[x]:
            if (notelist[x][shownote[x]] - duration) * 1000 <= curtime:
                noteimg = outside[x]
                noteimg = resize_height(noteimg, screen.get_height() * 0.25)
                notes.append(note(x, shownote[x], noteimg))
                shownote[x] += 1
        #####Judgement when player has press the key too lately, or even did not pressed the key#####
        if not len(notelist[x]) <= judgenote[x]:
            if curtime > (notelist[x][judgenote[x]] + 0.3) * 1000:
                judgenote[x] += 1
                combo = 0
                miss += 1
                ishit = False
                ismiss = True
                judge_count = [0, 0, True]
    #####Blit notes, Delete it from the list if it shouldn't be blited#####
    minusnumb = 0
    for x in range(len(notes)):
        x -= minusnumb
        if notes[x].blit(screen, judgenote, curfps, duration):
            del(notes[x])
            minusnumb += 1
    #####blit judgement text#####
    if ishit:
        judge_count[0] += 1
        if judge_count[2]:
            #hitimg = multilinerender(noto['black'], "HIT!! "+str(combo), color = (0, 255, 240))
            #hitimg = resize_height(hitimg, screen.get_height() * 0.4)
            blit_center(screen, hitimg)
        if judge_count[0] >= curfps * 0.05:
            judge_count[0] = 0
            judge_count[1] += 1
            judge_count[2] = not judge_count[2]
        if judge_count[1] == 10:
            ishit = False
    elif ismiss:
        judge_count[0] += 1
        if judge_count[2]:
            blit_center(screen, missimg)
        if judge_count[0] >= curfps * 0.05:
            judge_count[0] = 0
            judge_count[1] += 1
            judge_count[2] = not judge_count[2]
        if judge_count[1] == 10:
            ismiss = False
    if combo:
        combotxt = noto['black'].render(str(combo), 1, (0, 0, 0), None)
        combotxt = resize_height(combotxt, screen.get_height() * 0.1)
        blit_center(screen, combotxt, (0.5, 0.65))
    pygame.display.flip()
    rolex.tick(desiredfps)
startsound.play() #and start the start-effect sound.
fadeout_screen(rolex, screen, tmpscreen, loadimg, desopacity = 255)
60 * 0.05