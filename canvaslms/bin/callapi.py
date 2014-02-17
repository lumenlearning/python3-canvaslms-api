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

import os
import sys

import canvaslms.api as api
import canvaslms.api.util as apiutil
import canvaslms.bin.configutil as configutil

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

    # Start out with a blank configuration dict
    config = {}

    # Check for CANVASLMS_API_CONFIG_PATH environment variable
    # If found, try to read a configuration dict from the path given.
    config_path = os.getenv("CANVASLMS_API_CONFIG_PATH")
    if config_path != None:
        config = configutil.updatedict(config, configutil.readconfigfile(config_path))

    # If the user didn't provide any command line arguments, print usage.
    if len(sys.argv) == 1:
        printUsage()
        return
    
    # Pull the command line arguments into variables.
    tokenFilePath = sys.argv[1]
    server = sys.argv[2]
    apiEndpoint = sys.argv[3]

    # Make the call to the API and print the results in CSV format to
    # standard output.
    token = api.getAuthTokenFromFile(tokenFilePath)
    apiObj = api.CanvasAPI(defaultServer=server, defaultAuthToken=token)
    print(apiutil.toCSVString(apiObj.allPages(apiEndpoint)))

def printUsage():
    print("Usage: api_call_csv.py 'path to OAuth token file' 'server' 'api endpoint'")
    
if __name__ == '__main__': main()
