
import requests
from urllib.parse import *


class HeadersValueError(ValueError):
    def __init__(self, *args: object) -> None:
        ValueError.__init__(self, *args)

class HeadersTypeError(TypeError):
    def __init__(self, *args: object) -> None:
        TypeError.__init__(self, *args)


class Headers:

    class Parser:

        @classmethod
        def toDict(cls, rawHeaders):
            if isinstance(rawHeaders, str):
                headers = {}
                unparsed = rawHeaders.split(";;") if ';;' in rawHeaders else [rawHeaders]
                
                for header in unparsed:
                    if ':' not in header:
                        raise HeadersValueError("headers flag not formatted properly (no colon to separate header and value)")

                    delimiter = ': ' if ': ' in header else ':' 
                    headerName, headerValue = header.split(delimiter)
                    headers[headerName] = headerValue


                return headers

            raise HeadersTypeError(f"{type(rawHeaders)} not expected, pass string seperated by two semi-colons")

        @classmethod
        def toRaw(cls, headers):
            if isinstance(headers, dict):
                rawHeaders = str()

                for key , value in headers.items():
                    rawHeaders += key + ': ' + value + ';;'

                return rawHeaders

            raise HeadersTypeError(f"{type(headers)} not expected, pass a dict")


    def __init__(self, headers = {}) -> None:
        self.headers = headers

    def add(self, headname, headval):
        if not self.ishead(headname):
            self.headers[headname] = headval

    def update(self, headname, headval):
        self.headers[headname] = headval

    def remove(self, headname):
        if self.ishead(headname):
            del self.headers[headname]

    def ishead(self, headname):
        return headname in self.headers.keys()

    def GetAll(self):

        self.add('User-Agent', 
                        'Mozilla/5.0 (Windows NT 10.0; rv:54.0) Gecko/20100101 Firefox/54.0'
        )

        self.add('Accept',
                        'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        )

        self.add('Accept-Encoding', 'gzip, deflate')
        self.add('Accept-Language', 'en-US,en;q=0.5')
        self.add('Upgrade-Insecure-Requests', '1')
        self.add('Connection', 'keep-alive')

        return self.headers


class Request:

    def __init__(self, url, params = {}, headers: Headers = Headers()) -> None:
        self.url                = url
        self.uri                = urlparse(self.url)
        self.params             = params                    # Body parameters
        self.urlparams          = parse_qs(self.uri.query)  # Url parameters
        self.hostname           = self.uri.hostname
        self.headers            = headers
        self.session            = self.GetReqSession()

    def GetReqSession(self) -> requests.Session:
        return requests.Session()

    def Send(self, timeout = 10) -> requests.Response or None:
        pass

    def GetUrl(self):
        return f"{self.uri.scheme}://{self.uri.netloc}{self.uri.path}" + (f"?{urlencode(self.urlparams)}" if self.urlparams else str())

    def SetParams(self, params: dict):
        # Set Body parameters
        self.params = params

    def GetParams(self):
        return self.params

    def SetUrlParams(self, urlparams):
        self.urlparams = urlparams

    def GetUrlParams(self):
        return self.urlparams

    def get(self, timeout = 10):
        return self.SendReq(self.session.get, timeout)

    def post(self, timeout = 10):
        return self.SendReq(self.session.post, timeout)

    def SendReq(self, reqMethod, timeout = 10):
        return reqMethod(self.GetUrl(), data=self.params, headers=self.headers.GetAll(), timeout=timeout)


class Get(Request):
    def __init__(self, url, params = {}, headers: Headers = Headers()) -> None:
        Request.__init__(self, url, params, headers)

    def Send(self, timeout = 10) -> requests.Response or None:
        return Request.get(self, timeout)

    def SetParams(self, urlparams: dict):
        # In Get request paramters is urlparams attr not params
        self.SetUrlParams(urlparams)
    
    def GetParams(self) -> dict:
        return self.GetUrlParams()


class Post(Request):
    def __init__(self, url, params = {}, headers: Headers = Headers()) -> None:
        Request.__init__(self, url, params, headers)

    def Send(self, timeout = 10) -> requests.Response or None:
        return Request.post(self, timeout)