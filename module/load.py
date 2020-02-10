import pygame
from pydub import AudioSegment
from pygame.image import load as load_image
from os import listdir, scandir
from os.path import abspath, dirname, join

from module.transform import *

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

    for file in scandir(imgpath):
        # load it as a list/dict if it's a folder, else just load it as a single image
        filename = file.name.split(".")[0]
        print("Loading " + filename  + "... ", end = "")
        if file.is_dir():
            folderpath = file.path
            for name in [x.name.split(".")[0] for x in scandir(folderpath)]:
                # check if every file name is a number
                try:
                    int(name)
                except:
                    break
            else:
                img[filename] = [load_image(x.path).convert_alpha() for x in scandir(folderpath)]
                continue
            # if not, load it as a dict
            img[filename] = dict([(x.name.split(".")[0], load_image(x.path).convert_alpha()) for x in scandir(folderpath)])
        else:
            img[filename] = load_image(file.path).convert_alpha()
        print("Done.")
    img['logo'] = resize_width(img['logo'], scr_size[0])
    img['logo'] = resize(img['logo'], 0.8)
    img['loading'] = pygame.transform.scale(img['loading'], scr_size)

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
    font = dict([[x.split(".")[0], pygame.font.Font(join(fontpath, x), 70)] for x in listdir(fontpath) if x.split(".")[-1] == "ttf"])
    print("Done.\n")
    print("Finished loading.")

    return (img, sound, font)