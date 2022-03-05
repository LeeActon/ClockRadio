currentPage = None

def getCurrentPage():
    return Page.currentPage

def setCurrentPage(page):
    Page.currentPage = page

def updateCurrentPage():
    if Page.currentPage != None:
        Page.currentPage.update()

class Page:
    pageUp = None
    pageDown = None
    pageLeft = None
    pageRight = None
    layers = None

    def __init__(self):
        self.layers = []

    def __delete__(self):
        pass

    def addLayer(self, layer):
        self.layers.append(layer)

    def update(self):
        if self.layers != None:
            for layer in self.layers:
                layer.update()

    def linkUp(self, buttons):
        curButton = self
        for nextButton in buttons:
            curButton.pageUp = nextButton
            nextButton.pageDown = curButton
            curButton = nextButton

    def handleRotary(self, rotaryId, value):
        print(f"Rotary {rotaryId} = {value}")

    def handleButton(self, buttonId, state):
        if (state != 0):
            self.handleButtonDown(buttonId)
        else:
            self.handleButtonUp(buttonId)

    def handleButtonDown(self, buttonId):
        if buttonId == 0:
            self.handleEnterButtonDown()
        elif buttonId == 1:
            self.handleUpButtonDown()
        elif buttonId == 2:
            self.handleLeftButtonDown()
        elif buttonId == 3:
            self.handleDownButtonDown()
        elif buttonId == 4:
            self.handleRightButtonDown()

    def handleButtonUp(self, buttonId):
        if buttonId == 0:
            self.handleEnterButtonUp()
        elif buttonId == 1:
            self.handleUpButtonUp()
        elif buttonId == 2:
            self.handleLeftButtonUp()
        elif buttonId == 3:
            self.handleDownButtonUp()
        elif buttonId == 4:
            self.handleRightButtonUp()

    def handleEnterButtonDown(self):
        print("Enter Pressed")

    def handleUpButtonDown(self):
        print("Up Pressed")

    def handleDownButtonDown(self):
        print("Down Pressed")

    def handleLeftButtonDown(self):
        print("Left Pressed")

    def handleRightButtonDown(self):
        print("Right Pressed")

    def handleEnterButtonUp(self):
        print("Enter Released")

    def handleUpButtonUp(self):
        print("Up Released")
        if self.pageUp != None:
            print(self)
            print(self.pageUp)
            Page.currentPage = self.pageUp

    def handleDownButtonUp(self):
        print("Down Released")
        if self.pageDown != None:
            Page.currentPage = self.pageDown

    def handleLeftButtonUp(self):
        print("Left Released")
        if self.pageLeft != None:
            Page.currentPage = self.pageLeft

    def handleRightButtonUp(self):
        print("Right Released")
        if self.pageRight != None:
            Page.currentPage = self.pageRight
