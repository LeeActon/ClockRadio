
class Page:

    def handleEnterButtonDown(self):
        print("Enter Pressed");

    def handleUpButtonDown(self):
        print("Up Pressed");

    def handleDownButtonDown(self):
        print("Down Pressed");

    def handleLeftButtonDown(self):
        print("Left Pressed");

    def handleRightButtonDown(self):
        print("Right Pressed");


    def handleEnterButtonUp(self):
        print("Enter Released");

    def handleUpButtonUp(self):
        print("Up Released");

    def handleDownButtonUp(self):
        print("Down Released");

    def handleLeftButtonUp(self):
        print("Left Released");

    def handleRightButtonUp(self):
        print("Right Released");


    buttonDownHandlers = [handleEnterButtonDown, handleUpButtonDown, handleLeftButtonDown, handleDownButtonDown, handleRightButtonDown]
    buttonUpHandlers = [handleEnterButtonUp, handleUpButtonUp, handleLeftButtonUp, handleDownButtonUp, handleRightButtonUp]

    def __init__(self):
        pass

    def __delete__(self):
        pass

    def handleButtonDown(self, buttonId):
        if (buttonId >= 0 and buttonId < len(self.buttonDownHandlers)):
            self.buttonDownHandlers[buttonId](self)

    def handleButtonUp(self, buttonId):
        if (buttonId >= 0 and buttonId < len(self.buttonUpHandlers)):
            self.buttonUpHandlers[buttonId](self)
