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

from urllib.request import Request, urlopen
import json
import re

# Some regexes for dealing with HTTP responses from API
JSON_PATTERN = re.compile(r'application/json', re.I)
CHARSET_PATTERN = re.compile(r'charset=(.+?)(;|$)')

class CanvasAPI:
    # static variable to reference a default instance of this class
    INSTANCE = None

    def __init__(self, defaultServer=None, defaultAuthToken=None, defaultVersion='v1'):
        self._defaultServer = defaultServer
        self._defaultAuthToken = defaultAuthToken
        self._defaultVersion = defaultVersion

    def callAPI(self, url, server=None, authToken=None, version=None):
        if server == None:
            if self._defaultServer == None:
                raise ValueError('Argument \'server\' must be specified if \'defaultServer\' was not specified during CanvasAPI object initialization.')
            else:
                server = self._defaultServer

        if authToken == None:
            if self._defaultAuthToken == None:
                raise ValueError('Argument \'authToken\' must be specified if \'defaultAuthToken\' was not specified during CanvasAPI object initialization.')
            else:
                authToken = self._defaultAuthToken

        if version  == None:
            if self._defaultVersion == None:
                raise ValueError('Argument \'version\' must not be None.')
            else:
                version = self._defaultVersion


        req = Request(url='https://{}/api/{}/{}'.format(server, version, url), headers={'Authorization':' Bearer {}'.format(authToken)})
        return urlopen(req)

def checkJSON(resp):
    contentType = resp.headers.get('Content-Type')
    return bool(JSON_PATTERN.search(contentType))

def getCharset(resp):
    contentType = resp.headers.get('Content-Type')
    return CHARSET_PATTERN.search(contentType).group(1)

def getResponseBody(resp):
    charset = getCharset(resp)
    isJSON = checkJSON(resp)
    
    respBody = resp.readall()
    respBody = respBody.decode(charset)
    
    if isJSON:
        respBody = json.loads(respBody)
        
    return respBody

def setInstance(server, authToken):
    CanvasAPI.INSTANCE = CanvasAPI(server, authToken)