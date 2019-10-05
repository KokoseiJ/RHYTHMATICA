#This code contains additional functions that can be used with Pygame, desinged for RHYTHMATICA.
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

########################
#####Screen Effects#####
########################

def fadeout_screen(clock, screen, tmpscreen, image, duration = 1.5, fps = 60):
    print("fadeout started")
    image = pygame.transform.scale(image, screen.get_size()) #resize the image as the size of the screen, so the image will fill the screen completely.
    opacity = 0 #set opacity to 0
    for x in range(int(fps * duration)): #so this code will be executed [fps] times per seconds, and you want it to be run for [duration] seconds. so you multiply it. easy work.
        screen.blit(tmpscreen, (0, 0)) #blit the backed up screen.
        image.set_alpha(opacity) #set the image's alpha to [opacity]
        screen.blit(image, (0, 0)) #blit the image.
        opacity += (50 / (fps * duration)) #increase opacity a bit.
        pygame.display.update() #flip!
        clock.tick(fps) #now wait for 1/60 secs. wait, is it sec or secs? dunno lol
    print("fadeout finished")
    return

def fadein_screen(clock, screen, tmpscreen, image, duration = 1.5, fps = 60):
    print("fadein started")
    image = pygame.transform.scale(image, screen.get_size()) #resize the image as the size of the screen, so the image will fill the screen completely.
    opacity = 255 #set opacity to 0
    for x in range(int(fps * duration)): #so this code will be executed [fps] times per seconds, and you want it to be run for [duration] seconds. so you multiply it. easy work.
        screen.blit(tmpscreen, (0, 0)) #blit the backed up screen.
        image.set_alpha(opacity) #set the image's alpha to [opacity]
        screen.blit(image, (0, 0)) #blit the image.
        opacity -= (255 / (fps * duration)) #increase opacity a bit.
        pygame.display.update() #flip!
        clock.tick(fps) #now wait for 1/60 secs. wait, is it sec or secs? dunno lol
    print("fadein finished")
    return

def move_left(clock, screen, bg, cur, _next, fps = 60, duration = 2):
    cur.blit_xloc = 0.5 #set the current instance's location.
    cur.blit_size = 1 #set the current instance's size.
    _next.blit_xloc = 1 #set the next instance's location.
    _next.blit_size = 0 #set the next instance's size.
    #repeat at specified FPS, duration second:
    for x in range(int(fps * duration)):
        screen.blit(bg, (0, 0)) #blit the background.
        #call the move_left method.
        cur.move_left(screen, 0, fps*duration) 
        _next.move_left(screen, 1, fps*duration)
        #whoop! flip!
        pygame.display.flip()
        clock.tick(fps)
    return

def move_right(clock, screen, bg, cur, _next, fps = 60, duration = 2):
    cur.blit_xloc = 0.5 #set the current instance's location.
    cur.blit_size = 1 #set the current instance's size.
    _next.blit_xloc = 0 #set the next instance's location.
    _next.blit_size = 0 #set the next instance's size.
    #repeat at specified FPS, duration second:
    for x in range(int(fps * duration)):
        screen.blit(bg, (0, 0)) #blit the background.
        #call the move_right method.
        cur.move_right(screen, 0, fps*duration)
        _next.move_right(screen, 1, fps*duration)
        #whoop! flip!
        pygame.display.flip()
        clock.tick(fps)
    return

###########################
#####Custom Transforms#####
###########################

#commented codes are left for reference.
#Previously, these functinos are returning the locations or sizes so you still have to call another functions such as pygame.transform.scale() or blit()
#but that makes the code longer, so I refined it to get all the things done in one function.
#for TL:DR - I changed it because it sucks. done.
"""
def get_center(screen, surf, loc = (0.5, 0.5), anchor = (0.5, 0.5)): #put screen's sizes and surface's sizes, desired location and anchor(both between 0 and 1)
    return ((screen[0] * loc[0]) - (surf[0] * anchor[0]), (screen[1] * loc[1]) - (surf[1] * anchor[1])) #returns calculated answer. ez but kinda complicated to do with lambda
"""

def blit_center(screen, surf, location = (0.5, 0.5), anchorloc = (0.5, 0.5)): #This function allows you to blit the image at relative location, based on relative anchor point.
    refinedloc = [] #This list will contain the modified location.
    for scrsize, surfsize, loc, anchor in zip(screen.get_size(), surf.get_size(), location, anchorloc):
        #It multiplies location argument to the screen size. and it multiplies anchor argument to surface size. and subtract it from the first result.
        refinedloc.append((scrsize * loc) - (surfsize * anchor))
    #and, blit it! done.
    screen.blit(surf, refinedloc)
    return

"""
def get_resizedsize(surf, size): #put surface's size and desired size. default size is 1. 2 will double up the size.
    return (int(surf[0] * size), int(surf[1] * size)) #why did I define this fuction? This could be done with lambda xD
"""

def resize(surf, size): #put surface and desired size. default size is 1. 2 will double up the size.
    return pygame.transform.scale(surf, tuple(map(lambda x: int(x*size), surf.get_size())))

#This will resize the image's size to the max, so as a result you can set your image's size relatively.
#Which will remove the dependency of fixed window size, and make the program more adaptive.
def resize_onload(screen, surf, size = 1): 
    #set the variables.
    scrx = screen.get_width()
    scry = screen.get_height()
    imgx = surf.get_width()
    imgy = surf.get_height()
    #if image's width is bigger than it's height:
    if imgx > imgy:
        #imgx : imgy = scrx : height
        #imgy * scrx / imgx = height
        width = scrx
        height = imgy * scrx / imgx
    else:
        #imgx : imgy = width : scry
        #imgx * scry / imgy = width
        width = imgx * scry / imgy
        height = scry
    return pygame.transform.scale(surf, tuple(map(lambda x: int(x*size), (width, height))))

##TODO: Make another resizing method that depends on the height - done uwu
def resize_height(surf, desheight):
    #height:width = desheight:x
    #desheight * width / height = x
    height = surf.get_height()
    width = surf.get_width()
    return pygame.transform.scale(surf, (int(desheight * width / height), int(desheight)))

def resize_width(surf, deswidth):
    #height:width = x:deswidth
    #height * deswidth / width = x
    height = surf.get_height()
    width = surf.get_width()
    return pygame.transform.scale(surf, (int(deswidth), int(height * deswidth / width)))

def multilinerender(font, text, antialias = 1, color = (0, 0, 0), background = None):
    renderedlist = []
    for x in text.split("\n"):
        renderedlist.append(font.render(x, antialias, color, background))
    return combinesurfs(renderedlist)

def combinesurfs(surf):
    width = max(tuple(map(lambda x:  x.get_width(), surf)))
    height = sum(tuple(map(lambda x:  x.get_height(), surf)))
    rtnsurf = pygame.Surface((width, height), pygame.SRCALPHA).convert_alpha()
    prevyloc = 0
    for x in surf:
        rtnsurf.blit(x,((width / 2) - (x.get_width() / 2), prevyloc))
        prevyloc += x.get_height()
    return rtnsurf

#########################
#####Parsing Scripts#####
#########################

"""
def get_info(file, songlength):
    #0|Flamingo #name
    #1|Kero Kero Bonito #artist
    #2|89 #bpm
    #3|1489 #note
    #difficulty: ~2 easy 3~5 medium 6~ hard
    pass
"""
def get_note(notelist):
    """
    1|ver:A3
    2|/
    3|specific second and repeat
    and repeats for 6 times
    """
    """
    1|ver:A4
    2|b180
    3|d4
    4|w18.9
    5|2
    6|6
    7|/4
    """
    #try:
    if True:
        rtnlist = [[], [], [], [], [], []]
        ver = notelist[0][4:]
        if ver == "A3":
            tmp = 0
            for x in notelist[2:]:
                if x == "/":
                    tmp += 1
                else:
                    rtnlist[tmp].append(float(x))
        elif ver == "A4":
            bpm = 0
            div = 0
            time = 0
            for x in notelist[1:]:
                print(x)
                if not x:
                    continue
                elif x[0] == "b":
                    bpm = float(x[1:])
                elif x[0] == "d":
                    div = float(x[1:])
                elif x[0] == "w":
                    time = float(x[1:])
                elif x[0] == "/":
                    time += ((60 / bpm) / div) * float(x[1:])
                else:
                    for y in x:
                        rtnlist[int(y)-1].append(time)
                    time += (60 / bpm) / div
        return rtnlist
    #except Exception as e:
    #    return (1, "Yeouch! There is a wild exception in the note file!\nError Message: " + str(e))

##############
#####Misc#####
##############
def get_times(starttime, curtime):
    return (curtime - starttime)

def breakpoint():
    global breaknumb
    print("b", breaknumb)