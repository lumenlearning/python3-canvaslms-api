canvaslms
=========

canvaslms is released under the GNU AGPL version 3.  The full text of this license can be found [here](http://www.gnu.org/licenses/agpl.html) and in the `LICENSE` file in the project's root directory.

In its present state, canvaslms is a Python module that handles the low-level details of calling the [Canvas LMS API](https://canvas.instructure.com/doc/api/), including HTTP GET requests, OAuth authentication, and result pagination.  Its primary purpose is to provide a convenient means of pulling data from the API via GET requests.  Users can import this module into existing Python projects or they can run a standalone Python script from the command line and direct the output to a file.

This module was written in Python 3.  It would require fairly minimal effort to port it to Python 2.

**Table of Contents**

1. [Examples](#examples)
2. [Vision](#vision)
3. [History](#history)
4. [Contributions](#contributions)
5. [Active Development Disclaimer](#active-development)

<a id="examples">Examples</a>
---------------------------

These examples assume that you have copied the canvaslms folder to a location that is covered by the [PYTHONPATH](http://docs.python.org/3/tutorial/modules.html#the-module-search-path) variable.

### Import into existing project

    import canvaslms.api

    # Get the authorization token from a file (Or from any other source.
    #   We just need a string containing the authorization token.
    authToken = api.getAuthTokenFromFile('path/to/auth/token/file.txt')

    # Create our API object, giving the name of the server running the
    #   instance of Canvas and the authorization token that we'll use to
    #   authenticate our requests.
    apiObj = api.CanvasLMS('some.server.com', authToken)

    # Call the API and get the results.
    results = apiObj.allPages('accounts/123/courses')

    print(results)
    
    
### Call from the command line

Substitute "python3.2" with "python" or "python3" or whatever your Python 3 interpreter is called.  Run the following from the command line:

`python3.2 -m canvaslms.callapi.call\_api\_csv "path/to/authentication/file.txt" "some.server.com" "courses/123456/assignments" > results.csv`

This will make an authenticated call to the following URL:

`http://some.server.com/api/v1/courses/123456/assignments`

The result of the `-m` command line argument is that the Python interpreter loads the module in the `\_\_main\_\_` context.  This module is designed to run the `main()` function when in the `\_\_main\_
\_` context.

<a id="vision">Vision</a>
---------------------------------------------

canvaslms is a Python module with the ultimate goal of becoming a complete binding for [Instructure's Canvas LMS API](https://canvas.instructure.com/doc/api/).  The ideal implementation of this binding would be a module that allows the average Python developer to perform all actions and requests supported by the Canvas API while hiding some of the more arcane details from the user (such as [authentication](https://canvas.instructure.com/doc/api/file.oauth.html) and [pagination](https://canvas.instructure.com/doc/api/file.pagination.html).)

<a id="history">History</a>
---------------------------

This project began initially with the intent to create a counterpart Python class for everything in the Canvas API.  The module would include the following classes, for example:

* Account
* User
* Course
* Assignment
* Submission
* etc.

These classes would define a variety of methods to expose the functionality of the API.  It is easy to imagine examples such as the following:

* `myAcct = Account(123)` would instantiate a new `Account` object corresponding to account ID 123 and assign it to the `myAcct` variable.
* `myCourses = myAcct.getCourses()` would return a list of newly instantiated `Course` objects corresponding to courses in the 123 account and assign it to the `myCourses` variable.
* `myCourses[2].getAssignments()` would return a list of newly instantiated `Assignment` objects that are part of the course represented by the third `Course` object in the `myCourses` list.

The earlier commits in the repository attest to this vision.  However, starting with the `af85d0b30e` commit, we made a decision to temporarily put on hold the idea of a complete binding for all API functionality.  Instead, we pressed onward to develop code that would handle the low-level details of authentication and pagination, as well as returning the API results in a simple, human-readable, well supported format ([CSV](http://en.wikipedia.org/wiki/Comma-separated_values).)

By automating this basic functionality and wrapping the module in a standalone application (call\_api\_csv.py), we were able to call the module from any other program to retrieve data from the API.

This met our purposes for the time, and this remains the current state of the module.  We hope, however, to move forward in developing a complete binding for the Canvas API.

<a id="contributions">Contributions</a>
---------------------------------------

We welcome input from any interested parties!  If you would like to take part in discussion and development activities, contact `aaron@lumenlearning.com`.

<a id="active-development">Active Development Disclaimer</a>
------------------------------------------------------------

The canvaslms module is currently in nascent stages and is undergoing active development.  It should not at this time be considered "stable".  As we navigate through this exploratory development stage, we may choose to introduce changes into the code base that are not backwards compatible and will break existing interfaces.

As the COPYRIGHT document in the root of the repo states, this code "is distributed _in the hope that it will be useful_, but _WITHOUT ANY WARRANTY_; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE."

That being said, we will try to rock the boat as little as possible as we move forward.
