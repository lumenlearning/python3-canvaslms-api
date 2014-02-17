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

import json

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class InvalidJSONError(Error):
    """Raised when the JSON interpreter could not decode the file."""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return(repr(self.message))

class InvalidConfigurationError(Error):
    """Raised when the JSON in the file is not exactly one map object."""
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return(repr(self.message))

def readconfig(config_str):
    """Attempt to read a configuration dict from config_str.

    Arguments:
        config_str -- a string containing a map/dict object in JSON format.
    """
    # check if config_str contains properly formatted JSON
    try:
        config = json.loads(config_str)
    except ValueError as ve:
        raise InvalidJSONError("The following string does not contain properly formatted JSON:\n\t{}\n\t{}".format(config_str, ve.message))
    
    # check if JSON data contains exactly one map object
    if type(config) != dict:
        raise InvalidConfigurationError("The JSON object decoded from config_str must be a map (dict) object. Instead, the decoded object has a data type of {}.".format(repr(type(config))))

    # Otherwise, return the configuration object
    return config

def readconfigfile(path):
    """Attempt to read in a configuration dict object from the file at path.
    
    Arguments:
        path -- a string containing the path to a configuration file.
    """
    # Read in the contents of path
    f = open(path, 'r')
    config_str = f.read()
    f.close()

    # Get the configuration object
    return readconfig(config_str)
