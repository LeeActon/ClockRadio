import time
from Layer import Layer

class Page(Layer):
    def __init__(self, surface):
        self.surface = surface
        self.pageUp = None
        self.pageDown = None
        self.pageLeft = None
        self.pageRight = None
        self.timeout = None

    def __delete__(self):
        pass
 
    traceCount = 0
    @classmethod
    def trace(cls, message):
        if (cls.traceCount > 0):
            cls.traceCount = cls.traceCount - 1
            print(message)

    currentPage = None
    prevPages = []

    @classmethod
    def getCurrentPage(cls):
        return cls.currentPage

    @classmethod
    def setCurrentPage(cls, page):
        cls.currentPage = page

    @classmethod
    def updateCurrentPage(cls):
        if cls.currentPage != None:
            cls.currentPage.update()

    @classmethod
    def push(cls, page):
        cls.prevPages.append(cls.getCurrentPage())
        cls.setCurrentPage(page)

    @classmethod
    def pop(cls):
        if (len(cls.prevPages) > 0):
            cls.setCurrentPage(cls.prevPages.pop())

    def update(self):
        Page.trace(f"{self}.update()")

        if (self.timeout != None):
            now = time.time()
            if (now > self.timeout):
                self.timeout = None
                Page.pop()

        self.paint(self.surface)

    def linkUp(self, buttons):
        curButton = self
        for nextButton in buttons:
            curButton.pageUp = nextButton
            nextButton.pageDown = curButton
            curButton = nextButton

    def linkRight(self, buttons):
        curButton = self
        for nextButton in buttons:
            curButton.pageRight = nextButton
            nextButton.pageLeft = curButton
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
