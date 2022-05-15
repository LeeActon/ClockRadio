from Layer import Layer
from FontRef import FontRef
import Points

class TextLayer(Layer):
    def __init__(self):
        super().__init__()
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
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @classmethod
    def centerHorizontal(cls, textLayers, center):
        # Layout the textLayers horizontaly centered on center

        # Need the total width to center the whole group horizontally
        totalWidth = 0
        for textLayer in textLayers:
            w, h = textLayer.size
            totalWidth += w

        # Start out half the total width to the left of center
        p = Points.translatePoint(center,  (-int(totalWidth/2), 0))

        # Lay out each textLayer from left to right
        for textLayer in textLayers:
            w, h = textLayer.size
            # textLayer.position indicates the where the center of the text should be.
            # We want the left side to line up with the current position,
            # so we need to move the point half the width of the current layer.
            p = Points.translatePoint(p, (int(w/2),0))
            textLayer.position = p
            # Want the next layer's left side to line up with the current layer's right side
            p = Points.translatePoint(p, (int(w/2),0))

    @property
    def size(self):
        return self.font.size(self.text)

    def paint(self, surface):
        if (not self.visible):
            return
        super().paint(surface)
        if self.text != None:
            w, h = self.size
            color = self.color
            if self.hasFocus and (self.focusColor != None):
                color = self.focusColor
            img = self.font.render(self.text,True,color)
            x, y = self.position
            surface.blit(img,(x-w/2,y-h/2))