# Request-Handler-Python
A python helper class for making HTTP requests (mainly just a wrapper around the [Requests Module](https://pypi.org/project/requests/))<br>
Only supports **get** and **post** requests.

# Requirements
- [Requests Module](https://pypi.org/project/requests/) - install with `pip install requests`
- [Colorama Module](https://pypi.org/project/colorama/) - install with `pip install colorama`
- [Logger included in project](https://github.com/HorridModz/Request-Handler-Python/blob/main/logger.py)

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
This class only supports **get** and **post** requests for now.
Use `RequestHandler.get()` and `RequestHandler.post()` respectively.

**Example**:
```
response = RequestHandler.get("https://www.wikipedia.org")
print(response.text)
```
