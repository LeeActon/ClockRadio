import json
from ClockPage import ClockPage
from Style import Style
from Polygon import Polygon
from Circle import Circle
from FMStation import FMStation
from AlarmPage import AlarmPage
from FontRef import FontRef
from MenuItem import MenuItem
from MenuPage import MenuPage

class ForwardRef:
    def __init__(self, target, attrName, attrType, value):
        self.target = target
        self.attrName = attrName
        self.attrType = attrType
        self.value = value

class Settings:
    fonts_loader = lambda settings, values : settings.loadDict(FontRef, values)
    styles_loader = lambda settings, values : settings.loadDict(Style, values)
    polygons_loader = lambda settings, values : settings.loadDict(Polygon, values)
    circles_loader = lambda settings, values : settings.loadDict(Circle, values)
    clockPages_loader = lambda settings, values : settings.loadDict(ClockPage, values)
    alarmPages_loader = lambda settings, values : settings.loadDict(AlarmPage, values)
    menuItems_loader = lambda settings, values : settings.loadDict(MenuItem, values)
    menuPages_loader = lambda settings, values : settings.loadDict(MenuPage, values)
    fmStations_type = FMStation

    def __init__(self):
        self.forwardRefs = []

        self.fonts = None
        self.styles = None
        self.polygons = None
        self.circles = None
        self.clockPages = None
        self.alarmPages = None
        self.menuItems = None
        self.menuPages = None
        self.fmStations = None
    
    @classmethod
    def loadSettings(cls, fileName):
        settings = Settings()
        with open(fileName) as f:
            settings.loadAttrs(settings, json.load(f))

        settings.bindForwardRefs()

        return settings

    def createObject(self, objType, value):
        newObj = None
        if type(value) is dict:
            newObj = objType()
            self.loadAttrs(newObj, value)
        elif (type(value) is list):
            newObj= []
            for itemValue in value:
                newItem = self.createObject(objType, itemValue)
                newObj.append(newItem)
        else:
            if (type(value) is str) and (len(value) > 0) and (value[0] == "#"):
                newObj = self.findObject(value[1:])
            else:
                try:
                    if objType is None or objType is type(None) or objType is property:
                        newObj = eval(value)
                    else:
                        newObj = objType(eval(value))
                except:
                    newObj = value

        return newObj

    def findObject(self, reference):
        t, i = reference.split('.')
        d = None
        obj = None
        if t in self.__dict__:
            d = getattr(self, t)
        else:
            print(f"{t} not found")

        if (d is not None) and (i in d):
            obj = d[i]

        if obj is None:
            print(f"{i} not found")

        return obj

    def loadAttrs(self, obj, settings):
        obj_type = type(obj)
        attrNames = dir(obj) # gets all attributes including from base classes
        if type(settings) is not dict:
            print(f"{settings} is not dict")
        else:
            for attrName, value in settings.items():
                if (attrName[0] != '-'):
                    attrType = None
                    attrName_loader = f"{attrName}_loader"
                    if attrName_loader in attrNames:
                        loader = getattr(obj_type, attrName_loader)
                        attrValue = loader(self, value)
                        setattr(obj, attrName, attrValue)
                    else:
                        attrName_type = f"{attrName}_type"
                        if attrName_type in attrNames:
                            attrType = getattr(obj_type, attrName_type)
                        elif attrName in attrNames:
                            attrType = type(getattr(obj, attrName))
                        else:
                            print(f"{attrName} not in {attrNames}")

                        newObj = self.createObject(attrType, value)
                        if newObj != None:
                            setattr(obj, attrName, newObj)
                        elif (type(value) is str) and (len(value) > 0) and (value[0] == "#"):
                            self.forwardRefs.append(ForwardRef(obj, attrName, attrType, value))
        
    def bindForwardRefs(self):
        for ref in self.forwardRefs:
            newObj = self.createObject(ref.attrType, ref.value)
            setattr(ref.target, ref.attrName, newObj)

    def loadDict(self, itemType, values):
        results = dict()
        for key, value in values.items():
            results[key] = self.createObject(itemType, value)

        return results
