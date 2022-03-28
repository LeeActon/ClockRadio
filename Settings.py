import debugpy
import json
from ClockPage import ClockPage

class Settings:
    clockPages_loader = lambda values : Settings.loadDict(ClockPage, values)

    @classmethod
    def loadSettings(cls, fileName):
        settings = Settings()
        with open(fileName) as f:
            Settings.loadAttrs(settings, json.load(f))

        return settings;

    @classmethod
    def createObject(cls, objType, value):
        newObj = None
        if type(value) is dict:
            newObj = objType()
            Settings.loadAttrs(newObj, value)
        elif (type(value) is list):
            newObj= []
            for itemValue in value:
                newItem = Settings.createObject(objType, itemValue)
                newObj.append(newItem)
        else:
            try:
                if objType is None or objType is property:
                    newObj = eval(value)
                else:
                    newObj = objType(eval(value))
            except:
                newObj = value

        return newObj

    @classmethod
    def loadAttrs(cls, obj, settings):
        attrs = type(obj).__dict__
        attrNames = attrs.keys()
        if type(settings) is not dict:
            print(f"{settings} is not dict")
        else:
            for attrName, value in settings.items():
                if (attrName[0] != '-'):
                    attrType = None
                    attrName_loader = f"{attrName}_loader"
                    if attrName_loader in attrNames:
                        attrValue = attrs[attrName_loader](value)
                        setattr(obj, attrName, attrValue)
                    else:
                        attrName_type = f"{attrName}_type"
                        if attrName_type in attrNames:
                            attrType = attrs[attrName_type]
                        elif attrName in attrNames:
                            attrType = type(attrs[attrName])
                        else:
                            print(f"{attrName} not in {attrNames}")

                        newObj = Settings.createObject(attrType, value)
                        setattr(obj, attrName, newObj)
        
    @classmethod
    def loadDict(cls, itemType, values):
        results = dict()
        for key, value in values.items():
            results[key] = Settings.createObject(itemType, value)

        return results
