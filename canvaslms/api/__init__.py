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

import canvaslms.api.courses
from urllib.request import Request, urlopen
import json
import re

# Some regexes for dealing with HTTP responses from API
JSON_PATTERN = re.compile(r'application/json', re.I)
CHARSET_PATTERN = re.compile(r'charset=(.+?)(;|$)')

class CanvasAPI:
    @property
    def defaultServer(self):
        return self._defaultServer
    @defaultServer.setter
    def defaultServer(self, value):
        self._defaultServer = value

    @property
    def defaultAuthToken(self):
        return self._defaultAuthToken
    @defaultAuthToken.setter
    def defaultAuthToken(self, value):
        self._defaultAuthToken = value

    @property
    def defaultVersion(self):
        return self._defaultVersion
    @defaultVersion.setter
    def defaultVersion(self, value):
        self._defaultVersion = value

    # API access classes
    @property
    def courses(self):
        if self._courses == None:
            self.courses = courses.Courses(self)

        return self._courses
    @courses.setter
    def courses(self, value):
        self._courses = value

    def __init__(self, defaultServer=None, defaultAuthToken=None, defaultVersion='v1'):
        self.defaultServer = defaultServer
        self.defaultAuthToken = defaultAuthToken
        self.defaultVersion = defaultVersion

        # set API access clases to None
        self.courses = None

    def callAPI(self, url):
        # pull together connection/API information
        server = self.defaultServer
        if server == None:
            raise ValueError('Property \'defaultServer\' must be set prior to calling callAPI.')
        authToken = self.defaultAuthToken
        if authToken == None:
            raise ValueError('Property \'defaultAuthToken\' must be set prior to calling callAPI.')
        version = self.defaultVersion
        if version == None:
            raise ValueError('Property \'defaultVersion\' must be set prior to calling callAPI.')

        # put together the URL and make the request
        urlstr = 'https://{}/api/{}/{}'.format(server, version, url)
        req = Request(url=urlstr, headers={'Authorization':' Bearer {}'.format(authToken)})
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
