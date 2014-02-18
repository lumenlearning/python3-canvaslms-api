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
    """
    Base class for exceptions in this module.
    """
    pass

class InvalidJSONError(Error):
    """
    Raised when the JSON interpreter could not decode the file.
    """

    def __init__(self, message):
        self.message = message
    def __str__(self):
        return(repr(self.message))

class InvalidConfigurationError(Error):
    """
    Raised when the JSON in the file is not exactly one map object.
    """

    def __init__(self, message):
        self.message = message
    def __str__(self):
        return(repr(self.message))

class MissingConfigurationValueError(Error):
    """
    Raised when a mandatory configuration value is not specified in the
    configuration object.

    Attributes:
     - key: A string indicating the case-sensitive name of the required value
        that was not found.
     - message: A string giving the exception message.
    """
    
    def __init__(self, key):
        self.key = key
        self.message = "Could not find a value for {} in the given configuration object.".format(key)

    def __str__(self):
        return(repr([self.key, self.message]))


def readconfig(config_str):
    """
    Attempt to read a configuration dict from config_str. The function
    either returns a dict object on success, or throws an exception on failure.

    Arguments:
     - config_str: a string containing a map/dict object in JSON format.
    """

    # check if config_str contains properly formatted JSON
    try:
        config = json.loads(config_str)
    except ValueError as ve:
        raise InvalidJSONError("The following string does not contain properly formatted JSON:\n\t{}\n\t{}".format(config_str, ve))
    
    # check if JSON data contains exactly one map object
    if type(config) != dict:
        raise InvalidConfigurationError("The JSON object decoded from config_str must be a map (dict) object. Instead, the decoded object has a data type of {}.".format(repr(type(config))))

    # Otherwise, return the configuration object
    return config

def readconfigfile(path):
    """
    Attempt to read in a configuration dict object from the file at path.
    The function either returns a dict object on success, or throws an exception
    on failure.

    Arguments:
     - path: a string containing the path to a configuration file.
    """

    # Read in the contents of path
    f = open(path, 'r')
    config_str = f.read()
    f.close()

    # Get the configuration object
    return readconfig(config_str)

def updatedict(current_dict, new_dict):
    """
    Update the contents of current_dict with the contents of new_dict using the
    following rules:
     - For keys that exist only in current_dict, current_dict retains the
       current values.
     - For keys that exist only in new_dict, current_dict receives the values
       from new_dict.
     - For keys that exist in both current_dict and new_dict, current_dict
       receives the values from new_dict.

    However, values from new_dict are used to update current_dict ONLY when the
    new_dict value is not None.  This allows us to use an optparse.Values class
    to update current_dict.

    Arguments:
     - current_dict: the dictionary to be updated
     - new_dict: the dictionary containing the new values
    """
    
    for key in new_dict:
        if new_dict[key] != None:
            current_dict[key] = new_dict[key]

    return current_dict

def get_required_config_value(config, key):
    """
    Retrieve key from config.  If key does not exist in config, throw
    an exception.

    Arguments:
     - config: a dict containing the configuration values.
     - key: a string giving the key for the desired configuration value.
    """

    value = get_config_value(config, key)
    if value == None:
        raise MissingConfigurationValueError(key)

    return value

def get_config_value(config, key):
    """
    Retrieve key from config.  If key does not exist in config, return None.

    Arguments:
     - config: A dict containing the configuration values.
     - key: A string giving the key for the desired configuration value.
    """

    return config.get(key, None)
