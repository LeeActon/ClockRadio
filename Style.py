
class Style:
    def __init__(self):
        self.parent = None
        self.color = None
        self.focusColor = None
        self.backColor = None
        self.strokeColor = None
        self.fillColor = None
        self.width = None
        self.length = None
        self.shape = None
        self.radius = None
        self.font = None

    def getProperty(self, propertyName):
        return getattr(self, propertyName)

    def setProperty(self, propertyName, value):
        return setattr(self, propertyName, value)
