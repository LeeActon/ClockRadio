import time
from Layer import Layer

class Page(Layer):
    prevMenuRotaryValue = 0
    menuRotaryId = 13
    buttonDownTimes = {}
    buttonDownRepeats = {}
    buttonRepeatRate = {}

    def __init__(self):
        super().__init__()
        self.surface = None
        self.auxDevices = None
        self.pageUp = None
        self.pageDown = None
        self.pageLeft = None
        self.pageRight = None
        self.timeout = None

    def __delete__(self):
        pass

    currentPage = None
    prevPages = []

    @classmethod
    def getCurrentPage(cls):
        return cls.currentPage

    @classmethod
    def setCurrentPage(cls, page):
        cls.currentPage = page
        cls.currentPage.onActivate()

    @classmethod
    def updateCurrentPage(cls):
        if cls.currentPage != None:
            cls.currentPage.update()

    @classmethod
    def pushIfNotCurrent(cls, page):
        currentPage = cls.getCurrentPage()
        if page != currentPage:
            cls.prevPages.append(currentPage)
            cls.setCurrentPage(page)
            print(f"push - {page} - {cls.prevPages}")
            return False
        return True

    @classmethod
    def pop(cls):
        if (len(cls.prevPages) > 0):
            page = cls.prevPages.pop()
            cls.setCurrentPage(page)
            print(f"pop - {page} - {cls.prevPages}")
            return page
        
        return None

    def onActivate(self):
        pass

    def defaultTimeout(self):
        self.timeout = time.time() + 3

    def checkTimeout(self, now):
        if (self.timeout != None) and (now > self.timeout):
            page = Page.pop()
            if page != None:
                page.checkTimeout(now)

    def update(self):
        if (self.timeout != None):
            self.checkTimeout(time.time())

        time_ns = time.time_ns()
        for buttonId, ns in Page.buttonDownTimes.items():
            if ns != None:
                count = Page.buttonDownRepeats[buttonId] + 1
                rate = Page.buttonRepeatRate[buttonId]

                delta = time_ns - ns
                if delta > rate*count:
                    print(f"button repeat: {delta}, {count}, {rate}")
                    Page.buttonDownRepeats[buttonId] = count
                    self.handleButtonDownRepeat(buttonId, count)

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
        if rotaryId == Page.menuRotaryId:
            d = value - Page.prevMenuRotaryValue
            print(f"value = {value} prev = {Page.prevMenuRotaryValue} d = {d}")
            Page.prevMenuRotaryValue = value
            if d > 0:
                self.up()
            elif d < 0:
                self.down()
            return True

        return False

    @classmethod
    def setButtonRepeatRate(cls, buttonId, rate):
        Page.buttonRepeatRate[buttonId] = rate

    def handleButton(self, buttonId, state):
        self.defaultButtonHandler(buttonId, state)
        return True

    def defaultButtonHandler(self, buttonId, state):
        print(f"defaultButtonHandler({buttonId}, {state})")
        if (state != 0):
            if buttonId in Page.buttonRepeatRate:
                Page.buttonDownTimes[buttonId] = time.time_ns()
                Page.buttonDownRepeats[buttonId] = 0
            self.handleButtonDown(buttonId)
        else:
            ns = 0  # to handle any weird cases

            if buttonId in Page.buttonRepeatRate:
                print(f"    repeat rate: {Page.buttonRepeatRate[buttonId]}")
                if buttonId in Page.buttonDownTimes:
                    ns = time.time_ns() - Page.buttonDownTimes[buttonId];
                    print(f"    down time: {Page.buttonDownTimes[buttonId]} ns: {ns}")
                    del Page.buttonDownTimes[buttonId]

            self.handleButtonUp(buttonId, ns)

    def handleButtonDownRepeat(self, buttonId, count):
        pass

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

    def handleButtonUp(self, buttonId, ns):
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
        self.up()

    def up(self):
        if self.pageUp != None:
            print(self)
            print(self.pageUp)
            Page.setCurrentPage(self.pageUp)

    def handleDownButtonUp(self):
        print("Down Released")
        self.down()

    def down(self):
        if self.pageDown != None:
            Page.setCurrentPage(self.pageDown)

    def handleLeftButtonUp(self):
        print("Left Released")
        self.left()

    def left(self):
        if self.pageLeft != None:
            Page.setCurrentPage(self.pageLeft)

    def handleRightButtonUp(self):
        print("Right Released")
        self.right()

    def right(self):
        if self.pageRight != None:
            Page.setCurrentPage(self.pageRight)

    def sendAuxDevices(self, s):
        print(f"--> {s}")
        self.auxDevices.write(s.encode("utf-8"))
        self.auxDevices.write("\n".encode("utf-8"))
