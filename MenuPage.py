
from Page import Page
from MenuItem import MenuItem
from TextLayer import TextLayer
from Layer import Layer
import Points
from Style import Style

class MenuPage(Page):
    def __init__(self):
        super().__init__()
        self.menuItems = []
        self.font = None
        self.style = Style()
        self.style.backColor = (0,0,0)

    def update(self):
        if len(self.layers) == 0:
            position = Points.translatePoint(Layer.center, (0, -180))
            for menuItem in self.menuItems:
                textLayer = TextLayer()
                textLayer.text = menuItem.text
                textLayer.font = self.font
                textLayer.position = position
                position = Points.translatePoint(position, (0, 80))
                self.addLayer(textLayer)

        super().update()
                