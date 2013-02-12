def getUniqueValues(valueList):
    valueDict = dict()
    for v in valueList:
        valueDict[v] = 1

    return list(valueDict.keys())

def createDictFromAttr(objList, attr):
    dct = dict()
    for o in objList:
        key = getattr(o, attr)
        lst = dct.get(key)

        if lst:
            lst.append(o)
        else:
            dct[key] = [o]
    return dct

def getAttrFromList(objList, attr):
    values = []
    for o in objList:
        if type(o) == dict:
            values.append(o.get(attr, None))
        else:
            values.append(getattr(o, attr))
    return values

def createGetArray(varName, values):
    output = ''
    for v in values:
        output = output + '&{}[]={}'.format(varName, v)
    return output
