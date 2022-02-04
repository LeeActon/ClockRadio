import os
import pygame

def OpenSurface():
    surface = None
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679
    DISPLAY = os.getenv("DISPLAY")
    if DISPLAY:
        print("Display: {0}".format(DISPLAY))

    if os.getenv('SDL_VIDEODRIVER'):
        print("Using driver specified by SDL_VIDEODRIVER: {}".format(os.getenv('SDL_VIDEODRIVER')))
        pygame.display.init()
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        if size == (480, 480): # Fix for 480x480 mode offset
            size = (640, 480)
        surface = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.HWSURFACE)
        return surface

    else:
        # Iterate through drivers and attempt to init/set_mode
        for driver in ['rpi', 'kmsdrm', 'fbcon', 'directfb', 'svgalib']:
            os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
                size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
                if size == (480, 480):  # Fix for 480x480 mode offset
                    size = (640, 480)
                surface = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.HWSURFACE)
                print("Using driver: {0}, Framebuffer size: {1:d} x {2:d}".format(driver, *size))
                return surface
            except pygame.error as e:
                print('Driver "{0}" failed: {1}'.format(driver, e))
                continue
            break

    return None
