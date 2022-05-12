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
        self.activeMenuIndex = -1
        self.font = None
        self.style = Style()
        self.style.backColor = (0,0,0)
        self.activeMenuStyle = None

    def onActivate(self):
        self.sendAuxDevices(f"R {self.rotaryId} : {self.activeMenuIndex}, 0, {len(self.menuItems) - 1}, 0, 0")
        self.createMenuItemLayers()
        if self.activeMenuIndex == -1:
            self.setActiveMenuItemIndex(0)

    def createMenuItemLayers(self):
        if len(self.layers) == 0:
            position = Points.translatePoint(Layer.center, (0, -180))
            for menuItem in self.menuItems:
                textLayer = TextLayer()
                textLayer.text = menuItem.text
                textLayer.font = self.font
                textLayer.position = position
                position = Points.translatePoint(position, (0, 80))
                self.addLayer(textLayer)

    def setActiveMenuItemIndex(self, index):
        if index != self.activeMenuIndex:
            # deactivate the current
            if self.activeMenuIndex != -1:
                self.layers[self.activeMenuIndex].removeStyle(self.activeMenuStyle)

            self.activeMenuIndex = index

            if self.activeMenuIndex != -1:
                self.layers[self.activeMenuIndex].addStyle(self.activeMenuStyle)

    def handleRotary(self, rotaryId, value):
        if rotaryId == self.rotaryId:
            self.defaultTimeout()
            if Page.pushIfNotCurrent(self):
                self.setActiveMenuItemIndex(value)
            return True

        return False
    
    def handleButtonUp(self, buttonId, ns):
        if buttonId == self.rotaryId:
            if self.activeMenuIndex != -1:
                page = self.menuItems[self.activeMenuIndex].page
                if page != None:
                    Page.setCurrentPage(page)