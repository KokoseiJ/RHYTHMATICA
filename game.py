from function import *
from objclass import *
import pygame
from pygame.locals import *
from random import randint
import os
print("ligma")

#####initialization process#####
pygame.mixer.pre_init(44100, -16, 2, 1024) #Little Buffer, Less Delay!
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720))
pygame.display.set_caption("RHYTHMATICA")
#get a new clock. is it a real Rolex? damn, that's cool.
rolex = pygame.time.Clock()


#####set required variables#####
songnumb = 0 #songnumb should be set as 0.


#####make/load/process resources#####
#make a new Surface filled with color white, because black is not my favorite color xD
background = pygame.Surface(screen.get_size()).convert()
background.fill((255, 255, 255))

#load electron image, and append 10 intro_electron class with randomly given arguments.
electron = pygame.image.load("res/image/ingame/inside.png").convert_alpha()
electrons = []
for x in range(10):
    electrons.append(intro_electron(electron, randint(1, 10)/10, randint(1, 10)/10, randint(2, 4)/10))

#load logo, resize it a bit because it's T 0 0  T H I C C
logo = pygame.image.load("res/image/ingame/Rhythmatica.png").convert_alpha()
logo = resize(logo, 0.3)

#load the loding screen, I won't resize it as long as it will be resized in fadeout/fadein functions. :accreate:
loadimg = pygame.image.load("res/image/ingame/loading_wide.png").convert()

#load font, render a text kindly. uhh, maybe not that kind... nevermind.
notoblack = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 50)
pressntostart = notoblack.render("Press N to start", 1, (0, 0, 0)).convert_alpha()

#load my cool intro uwu
intromusic = pygame.mixer.Sound("res/audio/effect/Rhythmatica.wav")

#load the start effect sound.
startsound = pygame.mixer.Sound("res/audio/effect/start.wav")


#####aaand, finally we draw all these shit to the screen! yay!#####
#at the start, we play the song.
intromusic.play()


#####This is the intro code!#####
while True: # Let's repeat this until python breaks something.
    #first, blit the background.
    screen.blit(background, (0, 0))
    #intro_electron class have its own blit method, and will blit itself to the argument. so we call all of them.
    for x in electrons:
        x.blit(screen)
    #blit logo, kind(maybe not)text to the screen.
    blit_center(screen, logo)
    blit_center(screen, pressntostart, (0.5, 0.75))
    #and... flip! now you can see everything in the screen!
    pygame.display.flip()
    #now it's time to handle some events.
    for event in pygame.event.get(): #get all of the events in the queue.
        if event.type == QUIT: #if user tried to close the window?
            exit() #kill the python. simple
        elif event.type == KEYDOWN: #if user pressed the key?
            if event.key == K_n: #if the key that user pressed is N?
                print("n pressed") #first, print it in the console for debug purpose.
                break #and, get outta here.
    else: #if nothing broke:
        rolex.tick(130/60*2)#130 is the BPM of the song. BPM/60 makes BPM to beat per second, and I doubled it up to call these codes 2 times a beat.
        continue #let's keep this loop.
    break #if something broke, it will break this loop too.
intromusic.stop() #stop the music.
startsound.play() #and start the start-effect sound.
fadeout_screen(rolex, screen, loadimg) #call the fadeout thing


#####Selection Codes starts from here!#####
songlists = os.listdir("note") #load the songs.
songnumb_max = len(songlists) #get the number of songs available.
if len(songlists) == 0: #if there is no song:
    print("pfffft u didnt even put songs n00b gtfo") #lul, get rekt
    exit() #and exit the game.
elif songnumb >= songnumb_max: #if somehow songnumb is higher than the songnumb_max:
    print("wot m8 u deleted music while playing? impressive job") #it doesn't usally happen so... that really is impressing job
    songnumb = 0 #to prevent errors, we restore songnumb to 0
#and get some infos from the info.txt file.
songname, artist, bpm, notes, preview = get_info(open("note/" + songlists[songnumb]+"/info.txt"))
tmpsurf = pygame.Surface(screen.get_size()).convert()