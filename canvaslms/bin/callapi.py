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

import getpass
import json
import optparse
import os
import sys

import canvaslms.api as api
import canvaslms.api.util as apiutil
import canvaslms.bin.configutil as configutil

def main():
    """\
    This script makes the specified call to the Canvas API, returning the result
    to standard output in CSV format.  The main function for this module allows
    it to be run from the command line with the following invocation:
    
        python3 -m canvaslms.bin.callapi -T TOKENFILE -H HOST APICALL

    where TOKENFILE, HOST, AND APICALL are the following:
     - TOKENFILE: path to the file containing the authentication token
       to be used for communicating with the API.
        - "/home/superdevel/some_project/tokenfile"
     - HOST: name of the server running Canvas
        - "canvas.instructure.com"
     - APICALL: the actuall call to make to the API
        - "courses/123456/users?enrollment_type=student"

    Of course, if an appropriate configuration file has been provided containing
    the authentication token file path and the Canvas host name, you can run the
    script simply as:

        python3 -m canvaslms.bin.callapi APICALL
    """

    # 0. Start out with an empty configuration dict
    config = {}

    # 1. Check CANVASLMS_API_CONFIG_PATH environment variable
    # If found, try to read a configuration dict from the path given.
    config_path = os.getenv("CANVASLMS_API_CONFIG_PATH")
    if config_path != None:
        # TODO: Instead of just dying here, print a warning to
        # standard error if the specified file doesn't exist.
        config = configutil.updatedict(config, configutil.readconfigfile(config_path))

    # 2. Check for CANVASLMS_API_CONFIG file in the current working directory
    if os.path.isfile("CANVASLMS_API_CONFIG"):
        config = configutil.updatedict(config, configutil.readconfigfile("CANVASLMS_API_CONFIG"))

    # Parse command line options
    parser = optparse.OptionParser()
    parser.add_option("-C", "--config-path", dest="ConfigPath")
    parser.add_option("-H", "--host", dest="CanvasHost")
    parser.add_option("-T", "--token-path", dest="TokenPath")
    parser.add_option('-A', "--get-auth-token", dest='GetAuthToken', default=False, action='store_true')
    parser.add_option('-V', '--csv-output', dest='CSVOutput', default=False, action='store_true')
    (options, args) = parser.parse_args()

    # 3. Check for a --config argument
    if options.ConfigPath != None:
        # TODO: We do actually want to die here.  If the user
        # explicitly specified a path to a config file and the file
        # doesn't exist, we should throw an exception.
        config = configutil.updatedict(config, configutil.readconfigfile(options.ConfigPath))

    # 4. Update config with command line options and arguments
    config = configutil.updatedict(config, options.__dict__)
    if len(args) == 1:
        config['APICall'] = args[0]

    # Get the required configuration values from the configuration object
    tokenFilePath = configutil.get_required_config_value(config, 'TokenPath')
    server = configutil.get_required_config_value(config, 'CanvasHost')
    apiCall = configutil.get_required_config_value(config, 'APICall')

    # Get our auth token, either from the terminal or from a file.
    if options.GetAuthToken == True:
        token = getpass.getpass('Auth Token: ')
    else:
        token = api.getAuthTokenFromFile(tokenFilePath)

    # Make the call to the API and print the results to stdout.
    # Default output format is JSON (same as the API), but CSV output
    # is available with the -V command line option.
    apiObj = api.CanvasAPI(defaultServer=server, defaultAuthToken=token)
    results = apiObj.allPages(apiCall)
    if options.CSVOutput == True:
        print(apiutil.toCSVString(results))
    else:
        print(json.dumps(results, indent=4, separators=(',', ': ')))

if __name__ == '__main__': main()
