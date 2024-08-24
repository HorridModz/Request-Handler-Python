# Request-Handler-Python
A python helper class for making HTTP requests (mainly just a wrapper around the [requests](https://pypi.org/project/requests/) module)

Only supports **get** and **post** requests.

# Requirements
- [Requests Module](https://pypi.org/project/requests/) - install with `pip install requests`
- [Colorama Module](https://pypi.org/project/colorama/) - install with `pip install colorama`
- [logger.py file included in repository](https://github.com/HorridModz/Request-Handler-Python/blob/main/logger.py)

# Usage
Make sure you have all the requirements in [requirements.txt](https://github.com/HorridModz/Request-Handler-Python/blob/main/requirements.txt) installed.
Add both [logger.py](https://github.com/HorridModz/Request-Handler-Python/blob/main/logger.py) and [requesthandler.py](https://github.com/HorridModz/Request-Handler-Python/blob/main/requesthandler.py) to your project, then import `requesthandler`:
```py
import src.requesthandler
```

Everything you need is in the `RequestHandler` class:

```
from src.requesthandler import RequestHandler
```

This is a static class, so you do not need to create an instance of it. Instead, call its members directly:

```
RequestHandler.get("https://example.com")
```

# Logging
Logging to console is disabled by default. To enable it, use `enable_logging()`:
```py
from src.requesthandler import enable_logging()
enable_logging()
```

To disable it again, use `disable_logging()`:
```py
from src.requesthandler import disable_logging()
disable_logging()
```

To access the log, use the Log field of the logging class:

```py
from src.requesthandler import logging
print(logging.Log)
```

Remember that the log class provides a dedicated method (`printlog()`) so in the real world, use that instead of `print(logging.Log)`. The above code snippet is only for example's sake.

You can also change the logging settings by replacing `logging` with your own instance of the logging class. For example, to disable colorized logging:
```py
from src.requesthandler import logging, Logging
logging = Logging(usedefaults=False, colorized=False)
```
```
:param usedefaults: Whether to use the default logging settings.
:param synclog: Whether to sync the Log list with other instances of this class
:param kwargs: If usedefaults is False, supply your own logging settings here:
    colorized=True
    printwarnings=True
    printdebug=False
    printinfo=True
    printimportant=True
    printveryimportant=True
    printsuperimportant=True
    printspecial=True
    donotprintspecial=False
    donotprintsuccessinfo=False
    allowoverride=True
    printall=True
    printnone=False
```

Note that this will clear the existing log (`logging.Log`).

# Checking for Internet
To assert that an internet connection is available and raise an error if it is not, use **assert_internet()**:
```py
RequestHandler.assert_internet()
```

To check for an internet connection and handle it yourself, use **check_internet()**:
```py
if RequestHandler.check_internet():
  print("Online!")
else:
  print("Offline!")
```

# Performing Requests
This module only supports **get** and **post** requests for now.
Use `RequestHandler.get()` and `RequestHandler.post()` respectively.

**Example**:
```
response = RequestHandler.get("https://www.wikipedia.org")
print(response.text)
```

# API Reference
Wow I actually wrote it!

#### RequestHandler.get()
```py
 def get(link: str, params: Dict = None, auth: Any = None, cache: bool = True,
         headers: Dict = None, timeout: float = 5, errormessage: str = None,
         exceptionifbadstatuscode: bool = True) -> requests.Response:
```

```py
"""
Helper function to make http get request
If request fails, returns (None, None) or raises exception

:param link: Link to make get request to
:param params: Parameters to include in get request
:param cache: Whether to allow requests to be cached.
              If cache is False, the header {'Cache-Control': 'no-cache'}
              will be included in the request to disable caching.
              If cache is True, the Cache-Control header will not be included at all.
              Warning: If cache is True, it is not guaranteed that the request will be cached,
              but it should be.
              This will not override the headers parameter if it contains a 'Cache-Control' header.
:param auth: Authorization to include in the request.
             This will not override the headers parameter if it contains an 'Authorization' header.
:param headers: Headers to include in get request
:param timeout: How many seconds to wait until timing out the request
:param errormessage: Error message to raise if request fails or returns a
                     non-200 HTTP status code.
                     This will be bolted on to the beginning of the original error message.
:param exceptionifbadstatuscode: Whether to raise an exception if the request returns a non-200
                                 status code
:return: response

:raises NoInternetError: No internet connection
:raises HttpError: Request failed
:raise HttpError: Request returned a non-200 HTTP status code and exceptionifbadstatuscode was True
"""
```

#### RequestHandler.post()
```py
def post(link: str, data: Any = None, contenttype: str = None, json: Dict = None,
         auth: Any = None, headers: Dict = None, timeout: float = 5, errormessage: str = None,
         exceptionifbadstatuscode: bool = True) -> requests.Response:
```

```py
"""
Helper function to make http post request
If request fails, returns (None, None) or raises exception

:param link: Link to make post request to
:param data: Body of post request. For an empty body, set it to None or don't supply anything for it.
             Make sure contenttype matches the type of this data.
:param contenttype: The content type of the data, like 'text/plain' or 'application/json'.
                    Automatically detects json and string. If body is empty, contenttype will not be used.
                    This will not override the headers parameter if it contains a 'Content-Type' header.
:param json: Json data to include in the post request.
:param auth: Authorization to include in the request.
             This will not override the headers parameter if it contains an 'Authorization' header.
:param headers: Headers to include in post request.
:param timeout: How many seconds to wait until timing out the request
:param errormessage: Error message to raise if request fails or returns a
                     non-200 HTTP status code.
                     This will be bolted on to the beginning of the original error message.
:param exceptionifbadstatuscode: Whether to raise an exception if the request returns a non-200
                                 status code
:return: response

:raises ValueError: contenttype parameter was not supplied, 'Content-Type' header was not supplied,
    and content type could not be automatically detected.
:raises NoInternetError: No internet connection
:raises HttpError: Request failed
:raise HttpError: Request returned a non-200 HTTP status code and exceptionifbadstatuscode was True
"""
```

#### HTTPError
Exception raised for errors related to HTTP requests

#### NoInternetError
Exception raised if there is no internet connection

## Logging Stuff
There's also logging-related members:

#### Logging
The class for the logger.
```py
"""
:param usedefaults: Whether to use the default logging settings
:param synclog: Whether to sync the Log list with other instances of this class
:param kwargs: If usedefaults is False, supply your own logging settings here:
    colorized=True
    printwarnings=True
    printdebug=False
    printinfo=True
    printimportant=True
    printveryimportant=True
    printsuperimportant=True
    printspecial=True
    donotprintspecial=False
    donotprintsuccessinfo=False
    allowoverride=True
    printall=True
    printnone=False
"""
```
This is included so you can create a new instance to replace the module's built-in one, like so:
```py
from src.requesthandler import logging, Logging
logging = Logging(usedefaults=False, colorized=False)
```

#### logging
The instance of the `Logging` class used by the module. Again, you can replace this with your own instance of the class, as shown in the documentation for [Logging](#Logging).

#### enable_logging
Enables logging to console with print statements. It is off by default.

#### disable_logging
Re-disables logging to console with print statements, in the event that you enable it but want to later disable it.
