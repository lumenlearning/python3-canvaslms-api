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

from collections import OrderedDict

def getUniqueValues(valueList):
    """\
Produce a set of unique values from a set of values with possible duplicates.

Return: A list of unique values taken from valueList

Parameters:
  * valueList: A list of values to be de-duplicated.
"""

    # Using a dict as a filter for valueList.  Dictionary keys must be unique,
    #   and this will help us eliminate duplicates in valueList.
    valueDict = dict()

    # Doesn't matter what the values are.  Consequently, doesn't matter that
    #   they potentially are overwritten.
    for v in valueList:
        valueDict[v] = 1

    # Return the list of unique keys.
    return list(valueDict.keys())

def createDictFromAttr(objList, attr):
    """\
Group the objects in objList based on their value for a specific attribute.

Return: A dict where each key is one of the values attested for the attribute.  The value associated with each key is a list of objects whose value for attr was the same as the key.

Parameters:
  * objList: A list of objects, each having the attribute specified in attr.
  * attr: A string indicating the attribute of interest.
"""

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
    """\
Given a list of objects in objList, each having the attribute attr, return a list comprising the value of attr for each object in objList.

Return: A list of values.

Parameters:
  * objList: The list of objects
  * attr: The attribute had in common
"""

    values = []
    for o in objList:
        if type(o) == dict or type(o) == OrderedDict:
            values.append(o.get(attr, None))
        else:
            values.append(getattr(o, attr))
    return values

def createGetArray(varName, values):
    """\
Create a URL string to represent a named array of values for HTTP GET requests.

Example:
    urlArray = createGetArray('friends', ['Alice', 'Bob', 'Charlie', 'Drusilla'])
    print(urlArray)

Output:
    &friends[]=Alice&friends[]=Bob&friends[]=Charlie&friends[]=Drusilla

Return: The URL-encoded array string.

Parameters:
  * varName: The name of the array.
  * values: A list of string values.
"""

    output = ''
    for v in values:
        output = output + '&{}[]={}'.format(varName, v)
    return output
