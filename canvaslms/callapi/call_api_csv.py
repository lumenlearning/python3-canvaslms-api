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
import json
import sys

import canvaslms.api as api

def main():
    """\
This main function for this module allows it to be run from the command line with the following invocation:

  python3.2 -m canvaslms.callapi.call_api_csv {tokenFilePath} {server} {apiEndpoint}

The arguments are not named.  Order is important.
  1. The relative or absolute path of the file containing the authentication token.
  2. The server running the instance of Canvas.  (e.g., "myinstitution.instructure.com")
  3. The API endpoint to call.  (e.g., "courses/123456/assignments")

The program generates an absolute URL for the API call, calls it, converts the results to CSV format, and prints the CSV to standard output.
"""

    # If the user didn't provide any command line arguments, print usage.
    if len(sys.argv) == 1:
        printUsage()
        return
    
    # Pull the command line arguments into variables.
    tokenFilePath = sys.argv[1]
    server = sys.argv[2]
    apiEndpoint = sys.argv[3]

    # Make the call to the API and print the results in CSV format to standard output.
    csv = call_api_csv(tokenFilePath, server, apiEndpoint)
    print(csv)

def call_api_csv(tokenFilePath, server, apiEndpoint):
    """\
Call allPages with the appropriate parameters to get all results from the requested API call.  Convert these results to CSV format.  Return a string
"""

    token = api.getAuthTokenFromFile(tokenFilePath)
    apiObj = api.CanvasAPI(defaultServer=server, defaultAuthToken=token)
    
    result = apiObj.allPages(apiEndpoint)

    # Go through each dict object and look for arrays and dicts.
    #   These are complex data types that are not really compatible with CSV
    #   output format.  Change these types back into JSON strings so that if
    #   they contain data the user is interested in, they can process the JSON
    #   after the fact.
    for d in result:
        for k in d.keys():
            if type(d[k]) == dict or type(d[k]) == collections.OrderedDict or type(d[k]) == list:
                # Create an in-memory file for json.dump to work with.
                buf = io.StringIO()

                # Convert the object to a JSON string.
                json.dump(d[k], buf)

                # Replace the original object with the JSON string.
                d[k] = buf.getvalue()

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

        # The list of headers in the order that we first saw them.
        headers = list(allKeys.keys())
    else:
        headers = []

    # csv.DictWriter requires a file to write to.  Use an in-memory file.
    buf = io.StringIO()

    # Write out the objects in CSV format.
    dw = csv.DictWriter(buf, headers)
    dw.writeheader()
    dw.writerows(result)

    # Return the CSV data as a string
    result = buf.getvalue()
    buf.close()
    return result

def printUsage():
    print("Usage: api_call_csv.py 'path to OAuth token file' 'server' 'api endpoint'")

    
if __name__ == '__main__': main()
