from pygame.locals import *

from module import *

def intro(display, screen, rolex, res):
    # let's go to intro sequence
    img, sound, font = res
    electrons = [electron(img['inside'], screen.get_size()) for x in range(10)]

    sound["main"].play()

    while True:
        screen.fill((WHITE))
        for x in electrons:
            x.get(screen)

        blit_center(screen, img['logo'], (0.5, 0.5))
    
        starttext = font_render(font['bold'], "Press N to Start")
        blit_center(screen, starttext, (0.5, 0.75))

        vertext = font_render(font['bold'], "Ver: " + version)
        blit_center(screen, vertext, (1, 1), (1, 1))

        update(display, screen, FPSrender(rolex, font['regular']))
        rolex.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_n:
                    break
        else:  continue
        break