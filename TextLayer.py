import Layer

class TextLayer(Layer.Layer):
    def __init__(self, surface):
        super().__init__(surface)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        self._font = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def update(self):
        super().update()
        w, h = self.font.size(self.text)
        img = self.font.render(self.text,True,(255,0,0))
        x, y = self.position
        self.surface.blit(img,(x-w/2,y-h/2))