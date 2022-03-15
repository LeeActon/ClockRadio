
class Style:
    def __init__(self):
        self.parentStyle = None
        self._color = None
        self._backColor = None
        self._strokeColor = None
        self._fillColor = None
        self.width = 0
        self.length = 0
    
    @property
    def color(self):
        if (self._color != None):
            return self._color

        if (self.parentStyle != None):
            return self.parentStyle.color

        return (0, 0, 0)

    @color.setter
    def color(self, value):
        self._color = value

    @property
    def hasColor(self):
        return (self._color != None) or ((self.parentStyle != None) and self.parentStyle.hasColor)
    
    @property
    def backColor(self):
        if (self._backColor != None):
            return self._backColor

        if (self.parentStyle != None):
            return self.parentStyle.backColor

        return (0, 0, 0)

    @backColor.setter
    def backColor(self, value):
        self._backColor = value

    @property
    def hasBackColor(self):
        return (self._backColor != None) or ((self.parentStyle != None) and self.parentStyle.hasBackColor)

    @property
    def strokeColor(self):
        if (self._strokeColor != None):
            return self._strokeColor

        if (self.parentStyle != None):
            return self.parentStyle.strokeColor

        return self.color

    @strokeColor.setter
    def strokeColor(self, value):
        self._strokeColor = value

    @property
    def hasStrokeColor(self):
        return (self._strokeColor != None) or ((self.parentStyle != None) and self.parentStyle.hasStrokeColor)

    @property
    def fillColor(self):
        if (self._fillColor != None):
            return self._fillColor

        if (self.parentStyle != None) and self.parentStyle.hasFillColor:
            return self.parentStyle.fillColor

        return self.color

    @fillColor.setter
    def fillColor(self, value):
        self._fillColor = value

    @property
    def hasFillColor(self):
        return (self._fillColor != None) or ((self.parentStyle != None) and self.parentStyle.hasFillColor)
