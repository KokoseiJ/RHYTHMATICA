from function import *
from objclass import *
from pygame.locals import *
from math import floor
import os
print("ligma")

def clear():
    os.system("clear")

#initialize screen
pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

screen = pygame.display.set_mode(size = (640, 480))
pygame.display.set_caption("RHYTHMATICA")

rolex = pygame.time.Clock()

noto = {}
noto['black'] = pygame.font.Font("res/fonts/NotoSans-Black.ttf", 150)
noto['regular'] = pygame.font.Font("res/fonts/NotoSans-Regular.ttf", 150)



cursongpack = songpack('Himiko', noto)
notelist = get_note(cursongpack.notelist)
noteamount = sum(map(lambda x:  len(x), notelist))

#load logo and stuffs
whitebg = pygame.Surface(screen.get_size())
whitebg = whitebg.convert()
whitebg.fill((255, 255, 255))

outside = tuple(map(lambda x:  pygame.image.load("res/image/ingame/outside"+str(x+1)+".png").convert_alpha(), range(6)))

outline = pygame.image.load("res/image/ingame/outsidecover.png").convert_alpha()
outline = resize_height(outline, screen.get_height() * 0.25)

hitimg = pygame.image.load("res/image/ingame/hit.png").convert_alpha()
hitimg = resize_onload(screen, hitimg, 0.4)

missimg = pygame.image.load("res/image/ingame/miss.png").convert_alpha()
missimg = resize_onload(screen, missimg, 0.4)

keylist = (K_t, K_y, K_g, K_h, K_b, K_n)
loc = ((0.35, 0.2), (0.65, 0.2), (0.35, 0.5), (0.65, 0.5), (0.35, 0.8), (0.65, 0.8))
ispressed = [0, 0, 0, 0, 0, 0]
shownote = [0, 0, 0, 0, 0, 0]
judgenote = [0, 0, 0, 0, 0, 0]
notes = []
desiredfps = 60
duration = (60 / cursongpack.bpm) / 0.75

score = 0
maxcombo = 0
combo = 0
hit = 0
miss = 0
judge_count = [0, 0, True]
ishit = False
ismiss = False

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
    blit_center(whitebg, inside, (xloc, yloc))

screen.blit(whitebg, (0, 0))

pygame.display.update()

starttime = pygame.time.get_ticks()
cursongpack.music.play()

while pygame.mixer.get_busy():
    curtime = get_times(starttime)
    curfps = rolex.get_fps()
    screen.blit(whitebg, (0, 0))
    #####detecting keypress / exit signal, judgement when keydown, gets each key's status(pressed or not)#####
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_q:
                hit = 135
                miss = 246
                maxcombo = 256
                score = 8295
                cursongpack.music.stop()
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
                                if combo > maxcombo:
                                    maxcombo = combo
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
    if True:
        combotxt = noto['black'].render(str(combo), 1, (0, 0, 0), None)
        combotxt = resize_height(combotxt, screen.get_height() * 0.1)
        blit_center(screen, combotxt, (0.5, 0.65))
    screen.blit(noto['regular'].render(str(int(curfps)), 1, (0, 0, 0), None), (0, 0))
    pygame.display.flip()
    rolex.tick(desiredfps)

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
restxt = noto['black'].render("Result", 10, (0, 0, 0), None)
restxt = resize_onload(screen, restxt, 0.2)
blit_center(background, restxt, (0.5, 0), (0.5, 0))
nametxt = noto['black'].render(cursongpack.artist + " - " + cursongpack.name, 10, (255, 255, 255), None)
nametxt = resize_onload(screen, nametxt, 0.4)
nametxt_bg = pygame.Surface((screen.get_width(), nametxt.get_height()))
nametxt_bg.fill((0, 0, 0))
nametxt_bg.set_alpha(100)
blit_center(background, nametxt_bg, (0.5, 1), (0.5, 1))
blit_center(background, nametxt, (0.5, 1), (0.5, 1))

hitcount = 0
misscount = 0
combocount = 0
scorecount = 0

scoretxt = multilinerender(noto['regular'], 
'''HIT    0
MISS    0
MAXCOMBO    0
SCORE    0''', align = 1)
scoretxt = resize_height(scoretxt, screen.get_height() * 0.4)

tmpscreen = background
blit_center(tmpscreen, scoretxt, (0, 0.5), (0, 0.5))

fadein_screen(rolex, screen, tmpscreen, whitebg)

screen.blit(tmpscreen, (0, 0))
pygame.display.flip()

pygame.time.wait(1000)

while not scorecount >= score:
    if hitcount < hit:
        hitcount += 5
        if hitcount > hit:
            hitcount = hit
    elif misscount < miss:
        misscount += 5
        if misscount > miss:
            misscount = miss
    elif combocount < combo:
        combocount += 5
        if combocount > combo:
            combocount = combo
    elif scorecount < score:
        scorecount += 100
        if scorecount > score:
            scorecount = score

    scoretxt = multilinerender(noto['regular'],
    "HIT    " + hitcount + "\n" + 
    "MISS    " + misscount + "\n" +
    "COMBO    " + combocount + "\n" +
    "SCORE    " + scorecount,
    align = 1)
    scoretxt = resize_height(scoretxt, screen.get_height() * 0.4)

    screen.blit(background, (0, 0))
    blit_center(screen, scoretxt, (0, 0.5), (0, 0.5))
    pygame.display.flip()

    rolex.tick(20)