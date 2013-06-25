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

import collections
import json
import re

from urllib.request import Request, urlopen

# Some regexes for dealing with HTTP responses from API
JSON_PATTERN = re.compile(r'application/json', re.I)
CHARSET_PATTERN = re.compile(r'charset=(.+?)(;|$)')

def getAuthTokenFromFile(authTokenFilePath):
    """\
Read an authorization token from the file pointed to by authTokenFilePath.  The file MUST consist of only the authorization token.  It MAY contain leading or trailing whitespace.

Return: A string containing the authorization token (stripped of leading and trailing whitespace.)

Parameters:
  * authTokenFilePath: A string pointing to the filepath of the authorization token file.
"""
    
    # Read in the file containing the authorization token.
    f = open(authTokenFilePath)
    authToken = f.read()

    # Get rid of leading and trailing whitespace.
    authToken = authToken.strip()
    f.close()

    return authToken

def checkJSON(resp):
    """\
Check the 'Content-Type' header of a urllib.response object for the value 'application/json'.

Return: A boolean indicating whether the value of the Content-Type header is application/json.

Parameters:
  * resp: the urllib.response object to check.  (Probably obtained from the callAPI function.)
"""

    # Perform a regular expression search of the Content-Type header to
    #   check for application/json.
    contentType = resp.headers.get('Content-Type')
    return bool(JSON_PATTERN.search(contentType))

def getCharset(resp):
    """\
Determine the character set in use in a urllib.response object.

Return: A string taken from the Content-Type header indicating the character encoding of the response body.

Parameters:
  * resp: the urllib.response object to check.  (Probably obtained from the callAPI function.)
"""

    # Check the value of the Content-Type header for a charset identifier.
    contentType = resp.headers.get('Content-Type')
    return CHARSET_PATTERN.search(contentType).group(1)

def getResponseBody(resp):
    """\
Get the text of the response body.

Returns: Either a string containing the response body, or a dict object in the case of JSON data.

Parameters:
  * resp: A urllib.response object (probably returned from a call to callAPI).
"""

    # Read the response body and decode it according to the specified
    #   character set.
    charset = getCharset(resp)
    respBody = resp.readall()
    respBody = respBody.decode(charset)

    # If the content is JSON-encoded, then decode it into a dict object.
    isJSON = checkJSON(resp)
    if isJSON:
        respBody = json.loads(respBody, object_pairs_hook=collections.OrderedDict)
        
    return respBody


class CanvasAPI:
    """\
This class contains the core functionality of the canvaslms module.  Note the constructor, the pages generator, the allPages function, and the callAPI function.
"""

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
        """\
Create a new CanvasAPI object.

Parameters:
  * defaultServer: A string containing the name of the server on which the Canvas instance resides.  E.g., 'lumen.instructure.com'.
  * defaultAuthToken: A string containing the token to be used in authorizing API calls make to defaultServer.
  * defaultVersion: A string containing the version of the API.  Defaults to 'v1'.
  * defaultPerPage: An integer declaring the desired default number of API request results per page.  Default is 1000, but Canvas currently limits the maximum number of results to 50 per page.
"""
        
        self.defaultServer = defaultServer
        self.defaultAuthToken = defaultAuthToken
        self.defaultVersion = defaultVersion
        self.defaultPerPage = defaultPerPage

        # set API access clases to None
        self.courses = None

    def pages(self, url, absoluteUrl=False, verbose=False):
        """\
A generator function for use in for loops and any other context accepting a generator function.

Each subsequent call to the generator returns a urllib.response object corresponding to the next page of results from the original API call.

Parameters: See the parameter list for the callAPI function.
"""

        # Make the initial call to the API  to retrieve the first page
        #   of results.
        resp = self.callAPI(url, absoluteUrl, verbose)
        
        # Always send back the first page of results.
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
                # If we didn't find a 'Link' header, stop.
                checkMorePages = False
                raise StopIteration()

            # If we DID find a 'Link' header, then search for a 'next' link.
            #   All the links are separated by commas.
            links = linkHdr[1].split(',')
            for lnk in links:
                # Each link consists of two parts (the URL, and the 'rel'
                #   attribute), separated by a semi-colon.
                parts = lnk.split(';')
                if parts[1].find('next') >= 0:
                    nextPageUrl = parts[0]

                    # Remove the < and > characters that delineate the URL.
                    nextPageUrl = nextPageUrl.replace('<', '')
                    nextPageUrl = nextPageUrl.replace('>', '')
                    nextPageUrl = nextPageUrl.strip()

                    # Get the URL to retrieve the next page of results.
                    resp = self.callAPI(url=nextPageUrl, absoluteUrl=True)

                    # Wait until someone asks for the next page.
                    yield resp
                    break
            else:
                # If we went through all of the links and didn't find a 'next'
                #   link, then stop looking.
                checkMorePages = False
                raise StopIteration()

    def allPages(self, url, absoluteUrl=False, verbose=False):
        """\
Make the initial API request and then make subsequent calls to the API to retrieve any available pages beyond the initial page of results.

allPages makes use of the pages generator function in order to facilitate retrieving subsequent pages of results.

Return: A list of dicts, each dict representing one result from the API call.

Parameters: See the parameter list for the pages function.
"""

        # A place to accumulate all of the results from all of the pages.
        collector = []

        # Read all of the pages of results from this API call.
        for pg in self.pages(url, absoluteUrl, verbose):
            respBody = getResponseBody(pg)

            # If we were calling an API that returns single objects and not
            #   a list of objects, then wrap the object in a list so that we
            #   can append it to the collector list.
            if isinstance(respBody, collections.OrderedDict):
                respBody = [respBody]
            collector = collector + respBody
        return collector


    def callAPI(self, url, absoluteUrl=False, verbose=False):
        """\
Make a call to the API and return a urllib.response object.  See checkJSON, getCharset, and getResponseBody as useful functions for working with the response object.

Return: A urllib.response object obtained from calling the API.

Parameters:
  * url: The string containing the API endpoint to call.  E.g., 'courses/123456/assignments'.
  * absoluteUrl: A boolean indicating if url is an absolute URL.  Defaults to False.  If False, the url string is augmented with values from the defaultServer and defaultVersion variables in order to create an absolute URL (e.g., 'https://lumen.instructure.com/api/v1/courses/123456/assignments').
  * verbose: A boolean indicating if additional debug information should be printed to standard out.
"""

        # Gather connection/API information
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

        # If we're dealing with an absolute URL, then use it as it
        #   was provided.
        if absoluteUrl:
            urlstr = url
        # Otherwise, augment the URL with the default server, version, and
        #  per_page information.
        else:
            if url.find('?') < 0:
                urlstr = 'https://{}/api/{}/{}?per_page={}'.format(server, version, url, perPage)
            else:
                urlstr = 'https://{}/api/{}/{}&per_page={}'.format(server, version, url, perPage)

        # Print to standard out only if verbose == True.
        if verbose:
            print('Attempting to retrieve {} ...'.format(urlstr))

        # Create the request, adding in the oauth authorization token
        req = Request(url=urlstr, headers={'Authorization':' Bearer {}'.format(authToken)})

        # Make the call and return the urllib.response object.
        return urlopen(req)
