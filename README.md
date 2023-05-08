# Request-Handler-Python
A python helper class for making HTTP requests<br>
Only supports **get** and **post** requests.

# Requirements
- [Requests Module](https://pypi.org/project/requests/) - install with `pip install requests`
- [Logger included in project](https://github.com/HorridModz/Request-Handler-Python/blob/main/logger.py)
- [Colorama Module](https://pypi.org/project/colorama/) - install with `pip install colorama`

# Usage
Add both [logger.py]((https://github.com/HorridModz/Request-Handler-Python/blob/main/logger.py) and [requesthandler.py]((https://github.com/HorridModz/Request-Handler-Python/blob/main/requesthandler.py) to your project, then import `requesthandler`:
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
