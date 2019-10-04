from function import *
from objclass import *
from pygame.locals import *
print("ligma")
#initialize screen
pygame.init()
screen = pygame.display.set_mode(size = (1280, 720))
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
shownote = [1, 1, 1, 1, 1, 1]
judgenote = [1, 1, 1, 1, 1, 1]
starttime = pygame.time.get_ticks()
while True:
    screen.blit(background, (0, 0))
    currentinput = tuple(map(lambda x:  pygame.key.get_pressed()[x], (K_t, K_y, K_g, K_h, K_b, K_n)))
    for ispressed, numb in zip(currentinput, range(6)):
        if ispressed:
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
        print(numb, xloc, yloc)
        blit_center(screen, outline_mod, (xloc, yloc))
    pygame.display.flip()
    for event in pygame.event.get(): #get all of the events in the queue.
        if event.type == QUIT:#if user tried to close the window?
            exit() #kill the python. simple
    rolex.tick(60)