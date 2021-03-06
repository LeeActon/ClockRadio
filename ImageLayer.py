#!/usr/bin/env python3
import sys
import signal
import pygame

from Layer import Layer
import SurfaceHelper

class ImageLayer(Layer):
    image = None

    def __init__(self):
        super().__init__()
        self.imageFile = None
        self.centerImage = True

    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

    def __str__(self):
        return f"ImageLayer {{{self.imageFile}}}"

    def loadImage(self, imageFile):
        self.imageFile = imageFile
        self.image = pygame.image.load(imageFile)

    def paint(self, surface):
        if (not self.visible):
            return
        super().paint(surface)
        if self.image != None:
            offset = (0,0)
            if (self.centerImage):
                center = Layer.center
                image_width = self.image.get_width()
                image_height = self.image.get_height()
                offset = (center[0] - image_width/2, center[1] - image_height/2)
            surface.blit(self.image, offset)

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
