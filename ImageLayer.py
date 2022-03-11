#!/usr/bin/env python3
import sys
import signal
import pygame

from Layer import Layer
import SurfaceHelper

class ImageLayer(Layer):
    image = None

    def __init__(self, surface):
        super().__init__(surface)

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def loadImage(self, imageFile):
        self.image = pygame.image.load(imageFile)

    def update(self):
        super().update()
        if self.image != None:
            self.surface.blit(self.image, (0,0))

    _running = False

    def _exit(self, sig, frame):
        self._running = False
        print("\nExiting!...\n")

    def run(self):
        self._running = True
        signal.signal(signal.SIGINT, self._exit)
        _clock = pygame.time.Clock()
        while self._running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._running = False
                    break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self._running = False
                        break
            self.update()

            pygame.display.flip()
            _clock.tick(30)  # Aim for 30fps

        pygame.quit()
        sys.exit(0)


if __name__ == "__main__":
    surface = SurfaceHelper.OpenSurface()
    imageLayer = ImageLayer(surface)
    imageLayer.run()
