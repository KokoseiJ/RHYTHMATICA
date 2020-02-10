import random

from module.transform import *

class electron:
    def __init__(self, img, scrsize):
        self.scrsize = scrsize
        self.img = random.choice(img)
        self.orig_img = self.img.copy()
        self.loc = [random.randrange(0, x) for x in scrsize]
        self.speed = [random.randrange(-20, 20) / 10 for x in range(2)]
        #self.speed = (0, 0)
        self.status = True
        self.count = 0

    def get(self, screen):
        """
        blit the image to the screen, move it with the speed variable, increase its size
        """
        blit_center(screen, self.img, [int(x) for x in self.loc])
        temploc = [x + y for x, y in zip(self.loc, self.speed)]
        for x in range(2):
            if not 0 <= temploc[x] <= self.scrsize[x]:
                if temploc[x] < 0:
                    temploc[x] = 0
                elif temploc[x] > self.scrsize[x]:
                    temploc[x] = self.scrsize[x]
                self.speed[x] *= -1
        self.loc = temploc
        # Song's BPM is 130
        if self.count >= 60 / (130) * 60:
            if self.status:
                size = 0.7
            else:
                size = 0.8
            self.status = not self.status
            self.img = resize(self.orig_img, size)
            self.count = 0
        else:
            self.count += 1