import pygame
import random
from pydub import AudioSegment
from pygame.image import load as load_image
from os import listdir
from os.path import abspath, dirname, join

### Static variables ###
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

### classes ###
class electron:
    def __init__(self, img, scrsize):
        self.scrsize = scrsize
        self.img = random.choice(img)
        self.orig_img = self.img.copy()
        self.loc = [random.randrange(0, x) for x in scrsize]
        self.speed = [random.randint(10, 20) / 10 for x in range(2)]
        #self.speed = (0, 0)
        self.status = True
        self.count = 0

    def get(self, screen):
        """
        blit the image to the screen, move it with the speed variable, increase its size
        """
        blit_center(screen, self.img, self.loc)
        temploc = [x + y for x, y in zip(self.loc, self.speed)]
        for x in range(2):
            if not 0 <= temploc[x] <= self.scrsize[x]:
                if temploc[x] < 0:
                    temploc[x] = 0
                elif temploc[x] > self.scrsize[x]:
                    temploc[x] = self.scrsize[x]
                self.speed[x] *= -1
        self.loc = temploc
        if self.count >= 60 / (130) * 60:
            if self.status:
                size = 0.5
            else:
                size = 0.6
            self.img = resize(self.orig_img, size)
            self.status = not self.status
            self.count = 0
        else:
            self.count += 1

### Custom Transforms ###

def resize(surf, size):
    return pygame.transform.scale(surf, [int(x * size) for x in surf.get_size()])

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

def blit_center(screen, surf, loc, anchor = (0.5, 0.5)):
    """
    This will help you set the anchor point of the surface and blit it to the screen.
    if the presented loc is larger than 1, it will be treated as absolute location.
    else, it will be treated as relative location.
    it multiplies the anchor size to the size of the surface and add it to the location.
    """
    surfsize = surf.get_size()
    scrsize = screen.get_size()
    newloc = []
    for _loc, _surfsize, _scrsize, _anchor in zip(loc, surfsize, scrsize, anchor):
        if _loc > 1:
            newloc.append(_loc - _surfsize * _anchor)
        else:
            newloc.append(_scrsize * _loc - _surfsize * _anchor)
    return screen.blit(surf, newloc)

def font_render(font, text, antialias = 10, color = BLACK, background = None):
    text_list = [font.render(x, antialias, color) for x in text.split("\n")]
    width = max([x.get_width() for x in text_list])
    height = sum([x.get_height() for x in text_list])
    if background:
        rtnsurf = pygame.Surface((width, height))
        rtnsurf.fill(background)
    else:
        rtnsurf = pygame.Surface((width, height), flags = pygame.SRCALPHA)
    ypos = 0
    for x in text_list:
        blit_center(rtnsurf, x, (0.5, ypos), (0.5, 0))
        ypos += x.get_height()
    return rtnsurf

### Loading Thingy ###

def load_sound(filepath):
    """
    Load a sound file using pydub, get raw data of it, load it using pygame.
    It's a hack to load mp3 file in pygame
    """
    return pygame.mixer.Sound(AudioSegment.from_file(filepath).raw_data)

def load_resource(basepath, scr_size):
    # TODO: all the resizing functions are just for testing. remaster all the imgs with photoshop.
    """
    Load the files from the given path.
    Maybe can be used for loading a custom theme
    """

    ### Loading Images ###
    print("\nLoading Images...\n")
    imgpath = join(basepath, "res", "image")
    img = {}

    print("Loading logo image... ", end = "")
    img['logo'] = load_image(join(imgpath, "logo.png")).convert_alpha()
    img['logo'] = resize_width(img['logo'], scr_size[0])
    img['logo'] = resize(img['logo'], 0.8)
    print("Done.")
    
    print("Loading loading image... ", end = "")
    img['loading'] = load_image(join(imgpath, "loading.png")).convert()
    img['loading'] = pygame.transform.scale(img['loading'], scr_size)
    print("Done.")
    
    # loading files as a list
    print("Loading outside images... ", end = "")
    img['outside'] = [load_image(join(imgpath, "outside", str(x) + ".png")).convert_alpha() for x in range(1, 7)]
    print("Done.")
    
    # loading files as a list
    print("Loading inside images... ", end = "")
    img['inside'] = [load_image(join(imgpath, "inside", str(x) + ".png")).convert_alpha() for x in range(1, 7)]
    print("Done.")
    
    print("Loading outline image... ", end = "")
    img['outline'] = load_image(join(imgpath, "outline.png")).convert_alpha()
    print("Done.")
    
    # Loading files as a dict based on its filename
    print("Loading judge images... ", end = "")
    img['judge'] = dict([[x.split(".")[0], load_image(join(imgpath, "judge", x)).convert_alpha()] for x in listdir(join(imgpath, "judge"))])
    print("Done.")
    
    # Loading files as a dict based on its filename
    print("Loading rating images... ", end = "")
    img['rating'] = dict([[x.split(".")[0], load_image(join(imgpath, "rating", x)).convert_alpha()] for x in listdir(join(imgpath, "rating"))])
    print("Done.")
    
    ### Loading sound ###
    print("\nLoading Sound files...\n")
    soundpath = join(basepath, "res", "sound")
    
    sound = {}
    
    # Loading files as a dict based on its filename, but also printing all the files that are loaded
    for x in listdir(soundpath):
        print("Loading " + x.split('.')[0] + " sound... ", end = "")
        sound[x.split(".")[0]] = load_sound(join(soundpath, x))
        print("Done.")
    
    ### Loading fonts ###
    print("\nLoading Fonts...", end = "")
    fontpath = join(basepath, "res", "fonts")
    
    # Loading files as a dict based on its filename
    font = dict([[x.split(".")[0], pygame.font.Font(join(fontpath, x), 50)] for x in listdir(fontpath) if x.split(".")[-1] == "ttf"])
    print("Done.\n")
    print("Finished loading.")

    return (img, sound, font)

### Misc ###

def FPSrender(clock, font):
    fps = int(clock.get_fps())
    return font_render(font, str(fps))

def update(display, screen, FPS = None):
    #TODO: make a letterbox option. It will gonna look shitty on non 16:9 screen such as my 16:10 one
    """ 
    Scale the surface to fit the display size and blit it to the screen, and update the display.
    all of the pygame.display.update() function will be replaced with this one.
    """
    resize = pygame.transform.scale(screen, display.get_size())
    display.blit(resize, (0, 0))
    if FPS:
        display.blit(FPS, (0, 0))
    return pygame.display.update()
