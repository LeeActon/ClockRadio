import json
from ClockPage import ClockPage

class Settings:
    clockPage_type = ClockPage

    @classmethod
    def loadSettings(cls, fileName):
        settings = Settings()
        with open(fileName) as f:
            Settings.loadAttrs(settings, json.load(f))

        return settings;

    @classmethod
    def createObject(cls, objType, value):
        print(f"createObject({objType}, {value})")
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
                    print("newObj = eval(value)")
                else:
                    newObj = objType(eval(value))
                    print("newObj = objType(eval(value))")
            except:
                newObj = value
                print("newObj = value")

        print(f"{objType} = {newObj} ({type(newObj)})")

        return newObj

    @classmethod
    def loadAttrs(cls, obj, settings):
        print(f"loadAttrs({obj}, {settings}")
        attrs = type(obj).__dict__
        attrNames = attrs.keys()
        if type(settings) is not dict:
            print(f"{settings} is not dict")
        else:
            for attrName, value in settings.items():
                if (attrName[0] != '-'):
                    attrType = None
                    attrName_type = f"{attrName}_type"
                    if attrName_type in attrNames:
                        attrType = attrs[attrName_type]
                    elif attrName in attrNames:
                        attrType = type(attrs[attrName])
                    else:
                        print(f"{attrName} not in {attrNames}")

                    Settings.loadAttr(obj, attrName, attrType, value)
        
    @classmethod
    def loadAttr(cls, obj, attrName, attrType, value):
        print(f"loadAttr({obj}, {attrName}, {attrType}, {value})")
        newObj = Settings.createObject(attrType, value)
        print(f"setattr({obj}, {attrName}, {newObj} )")
        setattr(obj, attrName, newObj)
