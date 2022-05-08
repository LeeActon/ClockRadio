
from Layer import Layer
from FontRef import FontRef

class TextLayer(Layer):
    def __init__(self):
        super().__init__()
        self._color = (255,0,0)
        self._font = None
        self._text = None

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, value):
        if isinstance(value, FontRef):
            value = value.font
        self._font = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    def paint(self, surface):
        if (not self.visible):
            return
        super().paint(surface)
        w, h = self.font.size(self.text)
        img = self.font.render(self.text,True,self.color)
        x, y = self.position
        surface.blit(img,(x-w/2,y-h/2))