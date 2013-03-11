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
import collections

# Some regexes for dealing with HTTP responses from API
JSON_PATTERN = re.compile(r'application/json', re.I)
CHARSET_PATTERN = re.compile(r'charset=(.+?)(;|$)')

def getAuthTokenFromFile(authTokenFilePath):
    # get the authorization token for connecting to the API
    f = open(authTokenFilePath)
    authToken = f.read()
    authToken = authToken.strip()
    f.close()

    return authToken

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
    
    @property
    def defaultPerPage(self):
        return self._defaultPerPage

    @defaultPerPage.setter
    def defaultPerPage(self, value):
        self._defaultPerPage = value

    # API access classes
    @property
    def courses(self):
        if self._courses == None:
            self.courses = courses.Courses(self)

        return self._courses
    @courses.setter
    def courses(self, value):
        self._courses = value

    def __init__(self, defaultServer=None, defaultAuthToken=None, defaultVersion='v1', defaultPerPage=1000):
        self.defaultServer = defaultServer
        self.defaultAuthToken = defaultAuthToken
        self.defaultVersion = defaultVersion
        self.defaultPerPage = defaultPerPage

        # set API access clases to None
        self.courses = None

    def pages(self, url, absoluteUrl=False):
        resp = self.callAPI(url, absoluteUrl)
        
        # always send back the first page of results
        yield resp

        checkMorePages = True
        while checkMorePages:
            # check for 'Link' header
            linkHdr = None
            for h in resp.headers.items():
                if h[0] == 'Link':
                    linkHdr = h
                    break
            else:
                # if we didn't find one, stop
                checkMorePages = False
                raise StopIteration()

            # if we DID find one ...
            # search for a 'next' link
            links = linkHdr[1].split(',')
            for lnk in links:
                parts = lnk.split(';')
                if parts[1].find('next') >= 0:
                    nextPageUrl = parts[0]
                    nextPageUrl = nextPageUrl.replace('<', '')
                    nextPageUrl = nextPageUrl.replace('>', '')
                    nextPageUrl = nextPageUrl.strip()
                    resp = self.callAPI(url=nextPageUrl, absoluteUrl=True)
                    yield resp
                    break
            else:
                # if we went through all of the links and didn't find a 'next' link ...
                # stop looking
                checkMorePages = False
                raise StopIteration()

    def allPages(self, url, absoluteUrl=False):
        collector = []
        for pg in self.pages(url, absoluteUrl):
            collector = collector + getResponseBody(pg)
        return collector


    def callAPI(self, url, absoluteUrl=False):
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
        perPage = self.defaultPerPage

        # put together the URL and make the request
        if absoluteUrl:
            urlstr = url
        else:
            if url.find('?') < 0:
                urlstr = 'https://{}/api/{}/{}?per_page={}'.format(server, version, url, perPage)
            else:
                urlstr = 'https://{}/api/{}/{}&per_page={}'.format(server, version, url, perPage)

        print('Attempting to retrieve {} ...'.format(urlstr))
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
        respBody = json.loads(respBody, object_pairs_hook=collections.OrderedDict)
        
    return respBody
