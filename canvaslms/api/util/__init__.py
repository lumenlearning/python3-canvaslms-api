###############################################################################
# python3-canvaslms-api Source Code
# Copyright (C) 2013 Lumen LLC. 
# 
# This file is part of the python3-canvaslms-api module Source Code.
# 
# python3-canvaslms-api is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# python3-canvaslms-api is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
# 
# You should have received a copy of the GNU Affero General Public License
# along with python3-canvaslms-api. If not, see <http://www.gnu.org/licenses/>.
###############################################################################

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
