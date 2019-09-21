import pygame
#####Screen Effects#####
def fadeout_screen(clock, screen, image, duration = 1.5, fps = 60):
    print("fadeout started")
    tmpscreen = screen #back up the current screen, because we need to blit a low-opacity loading image to the screen for like 100 times.
    image = pygame.transform.scale(image, screen.get_size()) #resize the image as the size of the screen, so the image will fill the screen completely.
    opacity = 0 #set opacity to 0
    for x in range(int(fps * duration)): #so this code will be executed [fps] times per seconds, and you want it to be run for [duration] seconds. so you multiply it. easy work.
        screen.blit(tmpscreen, (0, 0)) #blit the backed up screen.
        image.set_alpha(opacity) #set the image's alpha to [opacity]
        screen.blit(image, (0, 0)) #blit the image.
        opacity += 100 / (fps * duration) #increase opacity a bit.
        pygame.display.update() #flip!
        clock.tick(fps) #now wait for 1/60 secs. wait, is it sec or secs? dunno lol
    print("fadeout finished")
    return

def fadein_screen(clock, screen, image, duration = 1.5, fps = 60):
    print("fadein started")
    tmpscreen = screen #back up the current screen, because we need to blit a low-opacity loading image to the screen for like 100 times.
    image = pygame.transform.scale(image, screen.get_size()) #resize the image as the size of the screen, so the image will fill the screen completely.
    opacity = 100 #set opacity to 0
    for x in range(int(fps * duration)): #so this code will be executed [fps] times per seconds, and you want it to be run for [duration] seconds. so you multiply it. easy work.
        screen.blit(tmpscreen, (0, 0)) #blit the backed up screen.
        image.set_alpha(opacity) #set the image's alpha to [opacity]
        screen.blit(image, (0, 0)) #blit the image.
        opacity -= 100 / (fps * duration) #increase opacity a bit.
        pygame.display.update() #flip!
        clock.tick(fps) #now wait for 1/60 secs. wait, is it sec or secs? dunno lol
    print("fadein finished")
    return


#####Custom Transforms#####
#commented codes are left for reference.
#Previously, these functinos are returning the locations or sizes so you still have to call another functions.
#but that makes code longer, so I refined it to do all the required things in these functions.
#for TL:DR - I changed it because it sucks. done.
"""
def get_center(screen, surf, loc = (0.5, 0.5), anchor = (0.5, 0.5)): #put screen's sizes and surface's sizes, desired location and anchor(both between 0 and 1)
    return ((screen[0] * loc[0]) - (surf[0] * anchor[0]), (screen[1] * loc[1]) - (surf[1] * anchor[1])) #returns calculated answer. ez but kinda complicated to do with lambda
"""

def blit_center(screen, surf, location = (0.5, 0.5), anchorloc = (0.5, 0.5)):
    refinedloc = []
    for scrsize, surfsize, loc, anchor in zip(screen.get_size(), surf.get_size(), location, anchorloc):
        refinedloc.append((scrsize * loc) - (surfsize * anchor))
    screen.blit(surf, refinedloc)
    return

"""
def get_resizedsize(surf, size): #put surface's size and desired size. default size is 1. 2 will double up the size.
    return (int(surf[0] * size), int(surf[1] * size)) #why did I define this fuction? This could be done with lambda xD
"""

def resize(surf, size): #put surface and desired size. default size is 1. 2 will double up the size.
    return pygame.transform.scale(surf, tuple(map(lambda x: int(x*size), surf.get_size())))

##TODO: Make another resizing method that depends on the height - done uwu
def resize_height(surf, desheight):
    #height:width = desheight:x
    #desheight * width / height = x
    height = surf.get_height()
    width = surf.get_width()
    return pygame.transform.scale(surf, (int(desheight * width / height), int(desheight)))

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

#####Parsing Scripts#####
"""
def get_info(file, songlength):
    #0|Flamingo #name
    #1|Kero Kero Bonito #artist
    #2|89 #bpm
    #3|1489 #note
    #difficulty: ~2 easy 3~5 medium 6~ hard
    pass
"""
def get_note(file):
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
    try:
        notelist =  file.read().split("\n")
        rtnlist = [[], [], [], [], [], []]
        ver = notelist[0][4:]
        if ver == "A3":
            tmp = 0
            for x in notelist[2:]:
                if x == "/":
                    tmp += 1
                else:
                    rtnlist[tmp].append(x)
        elif ver == "A4":
            bpm = 0
            div = 0
            time = 0
            for x in notelist[1:]:
                if x[0] == "b":
                    bpm = int(x[1:])
                elif x[0] == "d":
                    div = int(x[1:])
                elif x[0] == "w":
                    time = int(x[1:])
                elif x[0] == "/":
                    time += ((60 / bpm) / div) * int(x[1:])
                else:
                    for y in x:
                        rtnlist[int(y)].append(time)
                    time += (60 / bpm) / div
        return rtnlist
    except Exception as e:
        return (1, "Yeouch! There is a wild exception in the note file!\nError Message: "+e)
