import pygame

class FontRef:
    def __init__(self):
        self.filename = ""
        self.size = 0
        self._font = None

    @property
    def font(self):
        if self._font == None:
            self._font = pygame.font.Font(self.filename, self.size)

        return self._font
