"""
Helper class for making HTTP requests
Only supports get and post requests
"""

from typing import Set, Dict, Any, Union, Optional, Sequence
from collections import OrderedDict
import requests

# Don't import logging; we make our own instance
from src.logger import Logging, LoggingLevel

__all__ = ["RequestHandler", "HTTPError", "NoInternetError", "Logging", "logging", "enable_logging", "disable_logging"]


def _list_items(items: Union[Sequence[str], Set[str]]) -> str:
    """
    Helper function to convert a list of items to a grammatically correct string
    """
    if not isinstance(items, Union[tuple, list]):
        logging.log(f"_list_items() function called on object of type {type(items).__class__.__name__}"
                    f", which is unordered. Converting to a tuple to make it ordered.",
                    LoggingLevel.Debug)
        items = tuple(items)
    if len(items) == 1:
        return str(items[0])
    elif len(items) == 2:
        return str(items[0]) + " and " + str(items[1])
    else:
        result = ""
        for i in range(len(items) - 1):
            result += str(items[i]) + ", "
        result += "and " + str(items[-1])
        return result


def _truncatestring(s: str, maxlength: Optional[int] = 1000, maxlines: Optional[int] = 20) -> str:
    """
    Helper function to truncate a string to a given length

    :param s: The initial string
    :param maxlength: The amount of characters to truncate at. Takes precedence over maxlines.
    :param maxlines: The amount of lines to truncate at. Lower precedence than maxlength.
    :return: If the string did not exceed either of the limits - the unmodified initial string
             If the string exceeded the length limit - the string truncated to the length limit with
             "...[Truncated]" added to the end
             If the string exceeded the line limit but not the length limit - the string truncated to the
             line limit with "...[Truncated]" added to the end
    """
    if maxlength and len(s) > maxlength:
        return s[0:maxlength - 1] + "...[Truncated]"
    lines = s.splitlines()
    if maxlines and len(lines) > maxlines:
        return "\n".join(lines[0:maxlines - 1]) + "...[Truncated]"
    return s


def _truncatedict(d: Union[Dict, OrderedDict], maxitems: Optional[int] = 10,
                  maxlengthperitem: Optional[int] = 50, maxlinesperitem: Optional[int] = 1) -> str:
    """
    Helper function to truncate a dictionary to a given length
    Converts all the items to strings in "key: value" format, truncates each item
    truncates items to maxitems, then constructs string representation of dictionary from new items

    Warning: Python does not guarantee the order of dictionaries, so if you want some keys to be
        less likely to be truncated than others, use an OrderedDict rather than a standard dictionary
        and make sure you keep the items in order of importance.

    :param d: The initial dictionary
    :param maxitems: The maximum amount of items to include in the final string. Any items beyond this
        limit will be truncated.
    :param maxlengthperitem: The amount of characters to truncate each item at,
        including both the key and value. Takes precedence over maxlines.
    :param maxlinesperitem: The amount of lines to truncate each item at,
        including both the key and value. Lower precedence than maxlength.
    :return: For each item:
                Converts item to string in "key: value" format
                If the item string exceeds the per item length limit - the item string truncated to the
                length limit with "...[Truncated]" added to the end
                If the item string exceeds the per item line limit but not the per item length limit -
                the item string truncated to the line limit with "...[Truncated]" added to the end
            Removes any items beyond maxitems.
            Constructs string representation of dictionary from new items
            If maxitems was exceeded and some items were removed, adds "...[Truncated Items]" to the end
            of the string representation
    """
    items = [_truncatestring(f"{key}: {value}", maxlengthperitem, maxlinesperitem) for key, value in d.items()]
    hastruncateditems = False
    if maxitems and len(items) > maxitems:
        hastruncateditems = True
        items = items[:maxitems]
    dictstring = "{" + " ".join([f"{item}," if i < len(items) - 1 else item for i, item in enumerate(items)]) + "}"
    if hastruncateditems:
        dictstring += "...[Truncated Items]"
    return dictstring


class HTTPError(Exception):
    """
    Exception raised for errors related to HTTP requests
    """
    pass


class NoInternetError(HTTPError):
    """
    Exception raised if there is no internet connection
    """
    pass


class RequestHandler:
    """
    Helper class for making http requests
    """

    @classmethod
    def get(cls, link: str, params: Dict = None, auth: Any = None, cache: bool = True,
            headers: Dict = None, timeout: float = 5, errormessage: str = None,
            exceptionifbadstatuscode: bool = True) -> requests.Response:
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
        if timeout <= 0:
            timeout = None
        if headers is None:
            headers = {}
        if auth and 'Authorization' not in headers:
            headers['Authorization'] = auth
        if not cache and 'Cache-Control' not in headers:
            headers['Cache-Control'] = 'no-cache'
        logmessage = f"Making HTTP get request to {link}"
        requestdatamessage = []
        if params:
            requestdatamessage.append("params"
                                      f" {_truncatedict(params, maxitems=3, maxlengthperitem=45, maxlinesperitem=1)}")
        if headers:
            requestdatamessage.append(
                f"headers {_truncatedict(headers, maxitems=3, maxlengthperitem=45, maxlinesperitem=1)}")
        if requestdatamessage:
            logmessage += f" with {_list_items(requestdatamessage)}"
        if timeout:
            logmessage += f" with timeout of {timeout} seconds..."
        logging.log(logmessage, LoggingLevel.Info)
        try:
            response = requests.get(link, params=params, headers=headers, timeout=timeout)
        except requests.ConnectionError as e:
            # noinspection IncorrectFormatting
            if "An existing connection was forcibly closed by the remote host" in str(e):
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP get request to {link} failed - Connection forcibly closed"
                                    f" by remote host") from None
                else:
                    raise HTTPError(f"HTTP get request to {link} failed - Connection forcibly closed"
                                    f" by remote host") from None
            elif "Failed to establish a new connection:" in str(e) and "Max retries exceeded with url:" in str(e) \
                    and "Caused by NewConnectionError" in str(e):
                if errormessage:
                    raise NoInternetError(f"{errormessage}: HTTP get request to {link} failed"
                                          " - No internet connection") from None
                else:
                    raise NoInternetError(f"HTTP get request to {link} failed"
                                          " - No internet connection") from None
            else:
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP get request to {link} failed - {e}") from None
                else:
                    raise HTTPError(f"HTTP get request to {link} failed - {e}") from None
        except Exception as e:
            if errormessage:
                raise HTTPError(f"{errormessage}: HTTP get request to {link} failed - {e}") from None
            else:
                raise HTTPError(f"HTTP get request to {link} failed - {e}") from None
        if response.status_code == 200:
            logging.log(f"Successfully made HTTP get request to {link}", LoggingLevel.Info, successinfo=True)
        else:
            if exceptionifbadstatuscode:
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP get request to {link} failed"
                                    f" - returned non-200 http status code ({response.status_code})")
                else:
                    raise HTTPError(f"HTTP get request to {link} failed"
                                    f" - returned non-200 http status code ({response.status_code})")
            else:
                logging.log(f"HTTP get request to {link} failed"
                            f" - returned non-200 http status code ({response.status_code})",
                            LoggingLevel.Info, successinfo=True)
        return response

    @classmethod
    def post(cls, link: str, data: Any = None, contenttype: str = None, json: Dict = None,
             auth: Any = None, headers: Dict = None, timeout: float = 5, errormessage: str = None,
             exceptionifbadstatuscode: bool = True) -> requests.Response:
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
        if timeout <= 0:
            timeout = None
        if headers is None:
            headers = {}
        if data is not None and 'Content-Type' not in headers:
            if not contenttype:
                if isinstance(data, str):
                    contenttype = "text/plain"
                elif isinstance(data, dict):
                    contenttype = "application/json"
                else:
                    raise ValueError(f"Failed to make http post request to {link}: Could not determine content type of"
                                     f" data, which is of type {type(data).__class__.__name__}. Please manually"
                                     f" supply the content type using the contenttype parameter.")
                logging.log("Automatically detected content type of data"
                            f" \"{_truncatestring(str(data), maxlength=100, maxlines=1)}\": {contenttype}")
            headers["Content-Type"] = contenttype
        if auth and 'Authorization' not in headers:
            headers['Authorization'] = auth
        logmessage = f"Making HTTP post request to {link}"
        requestdatamessage = []
        if data:
            requestdatamessage.append(f"data \"{_truncatestring(str(data), maxlength=100, maxlines=1)}\""
                                      f" of content type {headers['Content-Type']}")
        else:
            requestdatamessage.append("empty body")
        if json:
            requestdatamessage.append(f"json {_truncatedict(json, maxitems=3, maxlengthperitem=45, maxlinesperitem=1)}")
        if headers:
            requestdatamessage.append(
                f"headers {_truncatedict(headers, maxitems=3, maxlengthperitem=45, maxlinesperitem=1)}")
        if requestdatamessage:
            logmessage += f" with {_list_items(requestdatamessage)}"
        if timeout:
            logmessage += f" with timeout of {timeout} seconds..."
        logging.log(logmessage, LoggingLevel.Info)
        try:
            response = requests.post(link, json=json, headers=headers, timeout=timeout)
        except requests.ConnectionError as e:
            # noinspection IncorrectFormatting
            if "An existing connection was forcibly closed by the remote host" in str(e):
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP get request to {link} failed - Connection forcibly closed"
                                    f" by remote host") from None
                else:
                    raise HTTPError(f"HTTP get request to {link} failed - Connection forcibly closed"
                                    f" by remote host") from None
            elif "Failed to establish a new connection:" in str(e) and "Max retries exceeded with url:" in str(e) \
                    and "Caused by NewConnectionError" in str(e):
                if errormessage:
                    raise NoInternetError(f"{errormessage}: HTTP post request to {link} failed"
                                          " - No internet connection") from None
                else:
                    raise NoInternetError(f"HTTP post request to {link} failed"
                                          " - No internet connection") from None
            else:
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP post request to {link} failed - {e}") from None
                else:
                    raise HTTPError(f"HTTP post request to {link} failed - {e}") from None
        except Exception as e:
            if errormessage:
                raise HTTPError(f"{errormessage}: HTTP post request to {link} failed - {e}") from None
            else:
                raise HTTPError(f"HTTP post request to {link} failed - {e}") from None
        if response.status_code == 200:
            logging.log(f"Successfully made HTTP post request to {link}", LoggingLevel.Info, successinfo=True)
        else:
            if exceptionifbadstatuscode:
                if errormessage:
                    raise HTTPError(f"{errormessage}: HTTP get request to {link} failed"
                                    f" - returned non-200 http status code ({response.status_code})")
                else:
                    raise HTTPError(f"HTTP post request to {link} failed"
                                    f" - returned non-200 http status code ({response.status_code})")
            else:
                logging.log(f"HTTP post request to {link} failed"
                            f" - returned non-200 http status code ({response.status_code})",
                            LoggingLevel.Info, successinfo=True)
        return response

    @staticmethod
    def check_internet(testurl: str = "https://www.example.com", timeout: float = 5) -> bool:
        """
        Checks that there is an internet connection.

        :param testurl: URL to make request to
        :param timeout: Timeout for request. If the timeout is exceeded, the internet connection check will fail.
        :return: Whether there is an internet connection
        """
        if timeout:
            logging.log(f"Checking for internet connection with timeout of {timeout} seconds...",
                        LoggingLevel.Info)
        else:
            logging.log("Checking for internet connection...", LoggingLevel.Info)
        logging.log(f"Using {testurl} to check for internet connection", LoggingLevel.Debug)
        try:
            RequestHandler.get(testurl, timeout=timeout, errormessage="Failed to check for internet connection")
        except NoInternetError:
            return False
        else:
            logging.log(f"Successfully confirmed internet connection!", LoggingLevel.Info, successinfo=True)
            return True

    @classmethod
    def assert_internet(cls, testurl: str = "https://www.example.com", timeout: float = 5) -> None:
        """
        Asserts that there is an internet connection.

        :param testurl: URL to make request to
        :param timeout: Timeout for request. If the timeout is exceeded, the internet connection check will fail.

        :raises NoInternetError: No internet connection
        """
        if not cls.check_internet(testurl, timeout):
            raise NoInternetError("No internet connection")


# Make our own instance of logging
logging = Logging(usedefaults=True)


def enable_logging():
    """
    Enables logging to the console with print statements
    """
    logging.enable()


def disable_logging():
    """
    Enables logging to the console with print statements
    """
    logging.disable()


disable_logging()
