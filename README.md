# Request-Handler-Python
A python helper class for making HTTP requests<br>
Only supports **get** and **post** requests.

# Requirements
- [Requests Module](https://pypi.org/project/requests/) - install with `pip install requests`

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
