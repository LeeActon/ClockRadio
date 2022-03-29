import json
from ClockPage import ClockPage
from Style import Style

class Settings:
    styles_loader = lambda settings, values : settings.loadDict(Style, values)
    clockPages_loader = lambda settings, values : settings.loadDict(ClockPage, values)

    @classmethod
    def loadSettings(cls, fileName):
        settings = Settings()
        with open(fileName) as f:
            settings.loadAttrs(settings, json.load(f))

        return settings;

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
            try:
                if objType is None or objType is type(None) or objType is property:
                    newObj = eval(value)
                else:
                    newObj = objType(eval(value))
            except:
                newObj = value

        return newObj

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
                        setattr(obj, attrName, newObj)
        
    def loadDict(self, itemType, values):
        results = dict()
        for key, value in values.items():
            results[key] = self.createObject(itemType, value)

        return results
