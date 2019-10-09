from function import *
from objclass import *
from pygame.locals import *
from math import floor
import os
print("ligma")

def clear():
    os.system("cls")
#initialize screen
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

screen = pygame.display.set_mode(size = (1024, 768))
pygame.display.set_caption("RHYTHMATICA")

rolex = pygame.time.Clock()

noto = {}
noto['black'] = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 50)
noto['regular'] = pygame.font.Font("res/fonts/NotoSans-Regular.ttf", 50)

flamingo = songpack('Flamingo', noto)
notelist = get_note(flamingo.notelist)

#load logo and stuffs
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((255, 255, 255))

outline = pygame.image.load("res/image/ingame/outsidecover.png").convert_alpha()
outline = resize_height(outline, screen.get_height() * 0.25)

keylist = (K_t, K_y, K_g, K_h, K_b, K_n)
ispressed = [0, 0, 0, 0, 0, 0]
shownote = [0, 0, 0, 0, 0, 0]
judgenote = [0, 0, 0, 0, 0, 0]
notes = []
desiredfps = 99999
duration = 1

for x in range(1, 7):
    inside = pygame.image.load("res/image/ingame/inside"+str(x)+".png").convert_alpha()
    inside = resize_height(inside, screen.get_height() * 0.25)
    if not x % 2:
        xloc = 0.65
    else:
        xloc = 0.35
    if x <= 2:
        yloc = 0.2
    elif x <= 4:
        yloc = 0.5
    else:
        yloc = 0.8
    blit_center(background, inside, (xloc, yloc))

screen.blit(background, (0, 0))

pygame.display.update()

starttime = pygame.time.get_ticks()
pygame.time.wait(duration)
flamingo.music.play()

while True:
    curtime = get_times(starttime)
    screen.blit(background, (0, 0))
    for event in pygame.event.get(): #get all of the events in the queue.
        if event.type == KEYDOWN:
            for key, numb in zip(keylist, range(6)):
                if event.key == key:
                    ispressed[numb] = 1
                    judgeres = judge(starttime, notelist[numb][judgenote[numb]], duration)
                    if judgeres:
                        judgenote[numb] += 1
                        break
        elif event.type == KEYUP:
            for key, numb in zip(keylist, range(6)):
                if event.key == key:
                    ispressed[numb] = 0
                    break
        elif event.type == QUIT:#if user tried to close the window?
            exit() #kill the python. simple
    for pressed, numb in zip(ispressed, range(6)):
        if pressed:
            outline_mod = resize(outline, 1.11)
        else:
            outline_mod = resize(outline, 1)
        if numb % 2:
            xloc = 0.65
        else:
            xloc = 0.35
        if numb < 2:
            yloc = 0.2
        elif numb < 4:
            yloc = 0.5
        else:
            yloc = 0.8
        blit_center(screen, outline_mod, (xloc, yloc))
    for x in range(6):
        if (notelist[x][shownote[x]] - duration) * 1000 <= curtime:
            noteimg = pygame.image.load("res/image/ingame/outside"+str(x+1)+".png").convert_alpha()
            noteimg = resize_height(noteimg, screen.get_height() * 0.25)
            notes.append(note(x, shownote[x], noteimg))
            shownote[x] += 1
    minusnumb = 0
    for x in range(len(notes)):
        x -= minusnumb
        if notes[x].blit(screen, judgenote, rolex.get_fps(), duration):
            del(notes[x])
            minusnumb += 1
    pygame.display.flip()
    rolex.tick(desiredfps)