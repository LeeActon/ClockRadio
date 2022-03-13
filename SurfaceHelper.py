import os
import pygame

def OpenSurface():
    surface = None
    # Based on "Python GUI in Linux frame buffer"
    # http://www.karoltomala.com/blog/?p=679
    DISPLAY = os.getenv("DISPLAY")
    if DISPLAY:
        print(f"Display: {DISPLAY}")

    if os.getenv("SDL_VIDEODRIVER"):
        print(f"Using driver specified by SDL_VIDEODRIVER: {SDL_VIDEODRIVER}")
        pygame.display.init()
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        if size == (480, 480): # Fix for 480x480 mode offset
            size = (640, 480)
        surface = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.HWSURFACE)
        return surface

    else:
        # Iterate through drivers and attempt to init/set_mode
        for driver in ["rpi", "kmsdrm", "fbcon", "directfb", "svgalib"]:
            os.putenv("SDL_VIDEODRIVER", driver)
            try:
                pygame.display.init()
                size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
                if size == (480, 480):  # Fix for 480x480 mode offset
                    size = (640, 480)
                surface = pygame.display.set_mode(size, pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.NOFRAME | pygame.HWSURFACE)
                print(f"Using driver: {driver}, Framebuffer size: {size[0]:d} x {size[1]:d}")
                return surface
            except pygame.error as e:
                print("Driver '{driver}' failed: {e}")
                continue
            break

    return None
