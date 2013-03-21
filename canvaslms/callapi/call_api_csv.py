#!/usr/bin/python3.2

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

import collections
import csv
import io
import sys

import canvaslms.api as api

def main():
    if len(sys.argv) == 1:
        printUsage()
        return
        
    tokenFilePath = sys.argv[1]
    server = sys.argv[2]
    apiEndpoint = sys.argv[3]

    csv = call_api_csv(tokenFilePath, server, apiEndpoint)

    print(csv)

def call_api_csv(tokenFilePath, server, apiEndpoint):
    token = api.getAuthTokenFromFile(tokenFilePath)
    apiObj = api.CanvasAPI(defaultServer=server, defaultAuthToken=token)

    result = apiObj.allPages(apiEndpoint)
    if len(result) > 0:
        # allKeys is acting simply as an ordered set here.  Not all
        #   of the results have the same set of data, which means that
        #   we need to look at the headers for ALL of the results instead
        #   of only the first one.
        allKeys = collections.OrderedDict()
        for r in result:
            ks = list(r.keys())
            for k in ks:
                allKeys[k] = 1

        headers = list(allKeys.keys())
    else:
        headers = []

    buf = io.StringIO()
    dw = csv.DictWriter(buf, headers)
    dw.writeheader()
    dw.writerows(result)

    result = buf.getvalue()
    buf.close()
    return result

def printUsage():
    print("Usage: api_call_csv.py 'path to OAuth token file' 'server' 'api endpoint'")

    
if __name__ == '__main__': main()
